#
#
#
#
from django.contrib import admin
from django.utils.html import format_html

from appliance.models import (
  Appliance,
  Property,
  PropertyAppliance,
  Schedule,
  User,
  UserProperty,
)

# Admin configuration
#
#
#
admin.site.site_header = "Appliance Administration"
admin.site.site_title = "Appliance Administration"
admin.site.index_title = "Admin"


# User Admin
#
#
#
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "email", "first_name", "last_name", "title", "is_staff")
  search_fields = ("username", "email", "first_name", "last_name")
  list_filter = ("is_staff", "is_active")

  fieldsets = (
    (None, {"fields": ("username", "password")}),
    (
      "Personal info",
      {"fields": ("first_name", "last_name", "email", "title", "profile_pic")},
    ),
    (
      "Permissions",
      {
        "fields": (
          "is_active",
          "is_staff",
          "is_superuser",
          "groups",
          "user_permissions",
        )
      },
    ),
    ("Important dates", {"fields": ("last_login", "date_joined")}),
  )


# Property Admin
#
#
#
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
  list_display = ("name", "address", "appliance_count")
  search_fields = ("name", "address")

  def appliance_count(self, obj):
    return obj.property_appliances.count()

  appliance_count.short_description = "Appliances"


# Appliance Admin
#
#
#
@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
  list_display = (
    "brand",
    "model",
    "appliance_type",
    "cost",
    "matching_score",
    "efficiency_rating",
    "display_image",
  )
  list_filter = ("appliance_type", "efficiency_rating", "brand")
  search_fields = ("brand", "model")

  def display_image(self, obj):
    if obj.image:
      return format_html('<img src="{}" height="50" />', obj.image.url)
    return "No Image"

  display_image.short_description = "Image"


# UserProperty Admin (Fact Table)
#
#
#
@admin.register(UserProperty)
class UserPropertyAdmin(admin.ModelAdmin):
  list_display = ("username", "property_id", "property_name", "assignment_date")
  list_filter = ("assignment_date",)
  search_fields = ("user__username", "property__name")
  raw_id_fields = ("user", "property")
  date_hierarchy = "assignment_date"

  def username(self, obj):
    return obj.user.username

  username.short_description = "Username"

  def property_id(self, obj):
    return obj.property.id

  property_id.short_description = "Property ID"

  def property_name(self, obj):
    return obj.property.name

  property_name.short_description = "Property Name"


# PropertyAppliance Admin (Fact Table)
#
#
#
@admin.register(PropertyAppliance)
class PropertyApplianceAdmin(admin.ModelAdmin):
  list_display = (
    "property_id",
    "property_name",
    "appliance_id",
    "appliance_name",
    "purchase_date",
    "display_cost",
    "usage",
    "is_within_warranty",
  )
  list_filter = ("usage", "purchase_date")
  search_fields = ("property__name", "appliance__brand", "appliance__model")
  raw_id_fields = ("property", "appliance")
  date_hierarchy = "purchase_date"

  def property_id(self, obj):
    return obj.property.id

  property_id.short_description = "Property ID"

  def property_name(self, obj):
    return obj.property.name

  property_name.short_description = "Property Name"

  def appliance_id(self, obj):
    return obj.appliance.id

  appliance_id.short_description = "Appliance ID"

  def appliance_name(self, obj):
    return str(obj.appliance)

  appliance_name.short_description = "Appliance"

  def display_cost(self, obj):
    return obj.get_cost()

  display_cost.short_description = "Cost"


# Schedule Admin
#
#
#
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
  list_display = (
    "property_appliance",
    "formatted_date_time",
    "notifications_enabled",
    "tenant_email",
  )
  list_filter = ("date", "notifications_enabled")
  search_fields = (
    "property_appliance__property__name",
    "property_appliance__appliance__brand",
    "tenant_email",
  )
  date_hierarchy = "date"

  def formatted_date_time(self, obj):
    return f"{obj.date} at {obj.hour:02d}:{obj.minute:02d}"

  formatted_date_time.short_description = "Date & Time"
