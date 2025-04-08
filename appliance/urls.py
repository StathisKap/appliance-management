#
#
#
#
from django.urls import path, register_converter

from . import views
from .converters import ApplianceTypeConverter

#
#
#
#
register_converter(ApplianceTypeConverter, "appliance_type")

# ============================================================================
# Main Page URLs
# ============================================================================

urlpatterns = [
  #
  #
  #
  #
  path("", views.home, name="home"),
  #
  #
  #
  #
  path("<int:user_property_id>", views.property_view, name="property_view"),
  #
  #
  #
  #
  path(
    "<int:property_id>/<int:appliance_id>/",
    views.property_appliance_view,
    name="property_appliance_view",
  ),
  #
  #
  #
  #
  path("explore/", views.explore, name="explore"),
  #
  #
  #
  #
  path("profile/", views.profile, name="profile"),
]

# ============================================================================
# Schedule Modal
# ============================================================================

urlpatterns += [
  #
  #
  #
  #
  path(
    "<int:property_id>/<int:appliance_id>/modal/",
    views.appliance_replacement_modal,
    name="appliance_replacement_modal",
  ),
  #
  #
  #
  #
  path(
    "appliance_replacement_modal_submit/",
    views.appliance_replacement_modal_submit,
    name="appliance_replacement_modal_submit",
  ),
]

# ============================================================================
# Add Appliance Modal
# ============================================================================

urlpatterns += [
  #
  #
  #
  #
  path(
    "add-appliance-submit/",
    views.add_property_appliance_submit,
    name="add_property_appliance_submit",
  ),
  #
  #
  #
  #
  path(
    "<int:property_id>/add-appliance/",
    views.add_property_appliance,
    name="add_property_appliance",
  ),
]

# ============================================================================
# API URLs
# ============================================================================

urlpatterns += [
  #
  #
  #
  #
  path("get-month-dates/", views.get_month_dates, name="get_month_dates"),
  #
  #
  #
  #
  path(
    "delete-schedule/<int:schedule_id>/", views.delete_schedule, name="delete_schedule"
  ),
  #
  #
  #
  #
  path(
    "delete-property-appliance/<int:property_appliance_id>/",
    views.delete_property_appliance,
    name="delete_property_appliance",
  ),
  #
  #
  #
  #
  path("logout/", views.logout_view, name="logout"),
]
