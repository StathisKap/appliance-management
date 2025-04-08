#
#
#
#
from datetime import timedelta
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
  FileExtensionValidator,
  MaxValueValidator,
  MinValueValidator,
)
from django.db import models
from django.utils import timezone


# Appliance types
#
#
#
class ApplianceType(Enum):
  WASHING_MACHINE = "Washing machine"
  DISHWASHER = "Dishwasher"
  DRYER = "Dryer"
  OVEN = "Oven"
  MICROWAVE = "Microwave"
  REFRIGERATOR = "Refrigerator"
  FREEZER = "Freezer"
  TOASTER = "Toaster"
  TOASTER_OVEN = "Toaster oven"

  @classmethod
  def choices(cls):
    return [(x.name, x.value) for x in cls]


# Efficiency ratings
#
#
#
class EfficiencyRating(Enum):
  VERY_LOW = "very_low"
  LOW = "low"
  BAD = "bad"
  MODERATE = "moderate"
  GOOD = "good"
  HIGH = "high"
  VERY_HIGH = "very_high"

  @classmethod
  def choices(cls):
    return [(x.value, x.name) for x in cls]


# Usage
#
#
#
class Usage(Enum):
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"
  VERY_HIGH = "very_high"

  @classmethod
  def choices(cls):
    return [(x.value, x.name) for x in cls]


# Users
#
#
#
class User(AbstractUser):
  profile_pic = models.FileField(
    upload_to="user_pictures/",
    validators=[
      FileExtensionValidator(
        ["jpg", "jpeg", "png", "gif", "webp", "avif", "heic", "heif", "tiff", "bmp"]
      )
    ],
    blank=True,
    null=True,
  )
  title = models.CharField(max_length=30, null=True)


# Properties
#
#
#
class Property(models.Model):
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=50)
  image = models.FileField(
    upload_to="property_pictures/",
    validators=[
      FileExtensionValidator(
        ["jpg", "jpeg", "png", "gif", "webp", "avif", "heic", "heif", "tiff", "bmp"]
      )
    ],
    blank=True,
    null=True,
  )

  def __str__(self):
    return self.name


# Appliances
#
#
#
class Appliance(models.Model):
  appliance_type = models.CharField(max_length=20, choices=ApplianceType.choices())
  brand = models.CharField(max_length=50)
  model = models.CharField(max_length=50)
  cost = models.IntegerField()
  matching_score = models.FloatField(
    validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
  )
  warranty_period = models.DurationField(
    help_text="Default duration of the warranty period", default=timedelta(days=365)
  )
  efficiency_rating = models.CharField(
    max_length=50, choices=EfficiencyRating.choices()
  )
  image = models.FileField(
    upload_to="appliance_pictures/",
    validators=[
      FileExtensionValidator(
        ["jpg", "jpeg", "png", "gif", "webp", "avif", "heic", "heif", "tiff", "bmp"]
      )
    ],
  )

  def __str__(self):
    return f"{self.brand} {self.model}"


# Properties Belonging to a User
#
#
#
class UserProperty(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
  property = models.ForeignKey(
    Property, on_delete=models.CASCADE, related_name="landlords"
  )
  assignment_date = models.DateField(default=timezone.now)

  class Meta:
    unique_together = [["user", "property"]]

  def __str__(self):
    return f"{self.user.username} - {self.property.name}"


# Property Appliances
#
#
#
class PropertyAppliance(models.Model):
  property = models.ForeignKey(
    Property, on_delete=models.CASCADE, related_name="property_appliances"
  )
  appliance = models.ForeignKey(
    Appliance, on_delete=models.CASCADE, related_name="appliance_properties"
  )

  purchase_date = models.DateField(default=timezone.now)
  actual_cost = models.IntegerField(null=True, blank=True)
  actual_warranty_period = models.DurationField(
    help_text="Actual warranty period for this specific purchase", null=True, blank=True
  )
  usage = models.CharField(max_length=50, choices=Usage.choices())

  def get_cost(self):
    """Returns the actual cost if set, otherwise the base appliance cost"""
    return self.actual_cost if self.actual_cost is not None else self.appliance.cost

  def get_warranty_period(self):
    """Returns the actual warranty period if set, otherwise the base warranty period"""
    return (
      self.actual_warranty_period
      if self.actual_warranty_period is not None
      else self.appliance.warranty_period
    )

  def is_within_warranty(self):
    warranty_period = self.get_warranty_period()
    warranty_end_date = self.purchase_date + warranty_period
    if isinstance(warranty_end_date, timedelta):
      warranty_end_date = self.purchase_date + warranty_end_date
    if hasattr(warranty_end_date, "date"):
      warranty_end_date = warranty_end_date.date()
    return timezone.now().date() <= warranty_end_date

  def get_usage_color(self):
    """Returns the appropriate color class based on usage level"""
    usage_colors = {
      "low": "text-success",
      "medium": "text-warning",
      "high": "text-danger",
      "very_high": "text-danger",
    }
    return usage_colors.get(self.usage, "text-muted")

  def __str__(self):
    return f"{self.appliance} at {self.property}"


# Schedules
#
#
#
class Schedule(models.Model):
  # The current PropertyAppliance that is being replaced
  property_appliance = models.ForeignKey(
    PropertyAppliance,
    on_delete=models.CASCADE,
    related_name="schedules",
  )

  # The new Appliance that will replace the current one
  replacement_appliance = models.ForeignKey(
    Appliance,
    on_delete=models.CASCADE,
    related_name="replacement_schedules",
  )

  date = models.DateField()
  hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
  minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
  notifications_enabled = models.BooleanField(default=False)
  tenant_email = models.EmailField(null=True, blank=True)
  tenant_phone = models.CharField(max_length=15, null=True, blank=True)

  def __str__(self):
    return f"{self.property_appliance} Replacement {self.date}::{self.hour:02d}:{self.minute:02d}"  # noqa: E501
