#
#
#
#
from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from appliance.models import (
  Appliance,
  ApplianceType,
  EfficiencyRating,
  Property,
  PropertyAppliance,
  Schedule,
  Usage,
  User,
  UserProperty,
)


class ViewTests(TestCase):
  def setUp(self):
    # Create test user
    self.user = User.objects.create_user(
      username="testuser", password="testpass123", email="test@example.com"
    )
    self.client = Client()
    self.client.login(username="testuser", password="testpass123")

    # Create test property
    self.property = Property.objects.create(name="Test Property", address="123 Test St")

    # Create test user property
    self.user_property = UserProperty.objects.create(
      user=self.user, property=self.property
    )

    # Create test appliance
    self.appliance = Appliance.objects.create(
      appliance_type=ApplianceType.REFRIGERATOR.name,
      brand="Test Brand",
      model="Test Model",
      cost=1000,
      efficiency_rating=EfficiencyRating.GOOD.value,
      matching_score=0.8,
    )

    # Create test property appliance
    self.property_appliance = PropertyAppliance.objects.create(
      property=self.property, appliance=self.appliance, usage=Usage.MEDIUM.value
    )

  def test_home_view(self):
    response = self.client.get(reverse("home"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/home/index.html")
    self.assertIn("user_properties", response.context)

  def test_property_view(self):
    response = self.client.get(reverse("property_view", args=[self.user_property.id]))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/property_view/index.html")
    self.assertIn("user_property", response.context)

  def test_explore_view(self):
    response = self.client.get(reverse("explore"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/explore/index.html")
    self.assertIn("appliances", response.context)

  def test_profile_view(self):
    response = self.client.get(reverse("profile"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/profile/index.html")
    self.assertIn("user", response.context)

  def test_property_appliance_view(self):
    response = self.client.get(
      reverse("property_appliance_view", args=[self.property.id, self.appliance.id])
    )
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/property_appliances/index.html")
    self.assertIn("current_appliance", response.context)

  def test_appliance_replacement_modal(self):
    response = self.client.post(
      reverse(
        "appliance_replacement_modal", args=[self.property.id, self.appliance.id]
      ),
      {"appliance_id": self.appliance.id},
    )
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/property_appliances/modal/index.html")
    self.assertIn("appliance", response.context)

  def test_add_property_appliance(self):
    response = self.client.post(
      reverse("add_property_appliance", args=[self.user_property.id])
    )
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "partial/property_view/appliance_add_modal.html")
    self.assertIn("appliances", response.context)

  def test_get_month_dates(self):
    today = timezone.now().date()
    response = self.client.get(
      reverse("get_month_dates"), {"year": today.year, "month": today.month}
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn("dates", response.json())

  def test_delete_schedule(self):
    # Create a test schedule
    schedule = Schedule.objects.create(
      property_appliance=self.property_appliance,
      replacement_appliance=self.appliance,
      date=date.today() + timedelta(days=1),
      hour=10,
      minute=30,
    )
    response = self.client.post(reverse("delete_schedule", args=[schedule.id]))
    self.assertEqual(response.status_code, 200)
    self.assertFalse(Schedule.objects.filter(id=schedule.id).exists())

  def test_delete_property_appliance(self):
    response = self.client.post(
      reverse("delete_property_appliance", args=[self.property_appliance.id])
    )
    self.assertEqual(response.status_code, 200)
    self.assertFalse(
      PropertyAppliance.objects.filter(id=self.property_appliance.id).exists()
    )

  def test_logout_view(self):
    response = self.client.get(reverse("logout_view"))
    self.assertEqual(response.status_code, 302)  # Redirect to login page
    self.assertEqual(response.url, "/admin/login/")

  def test_unauthorized_access(self):
    # Logout the user
    self.client.logout()

    # Try to access a protected view
    response = self.client.get(reverse("home"))
    self.assertEqual(response.status_code, 302)  # Should redirect to login
    self.assertTrue(response.url.startswith("/admin/login/"))

  def test_property_appliance_warranty(self):
    # Test warranty period
    self.assertTrue(self.property_appliance.is_within_warranty())

    # Test cost methods
    self.assertEqual(self.property_appliance.get_cost(), self.appliance.cost)

    # Test usage color
    self.assertEqual(
      self.property_appliance.get_usage_color(), "text-warning"
    )  # For MEDIUM usage
