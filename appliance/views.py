#
#
#
#
from calendar import monthrange
from datetime import date, timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from appliance.forms import PropertyApplianceForm, ScheduleForm
from appliance.models import (
  Appliance,
  Property,
  PropertyAppliance,
  Schedule,
  UserProperty,
)

# ============================================================================
# Helper Functions
# ============================================================================

def get_availability_context(month=None, year=None):
  today = timezone.now().date()
  current_year = today.year
  current_month = today.month

  if month and year:
    current_year = int(year)
    current_month = int(month)

  first_day = date(current_year, current_month, 1)
  last_day = date(
    current_year, current_month, monthrange(current_year, current_month)[1]
  )

  dates = []

  first_weekday = (first_day.weekday() + 1) % 7
  for _ in range(first_weekday):
    dates.append(
      {
        "date": "",
        "day": "",
        "is_available": False,
        "available_hours": [],
        "available_minutes": [],
      }
    )

  current_date = first_day
  while current_date <= last_day:
    weekday = (current_date.weekday() + 1) % 7
    is_available = current_date > today and weekday not in [0, 6]
    dates.append(
      {
        "date": current_date.strftime("%Y-%m-%d"),
        "day": current_date.day,
        "is_available": is_available,
        "available_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        if is_available
        else [],
        "available_minutes": [0, 15, 30, 45] if is_available else [],
      }
    )
    current_date += timedelta(days=1)

  last_weekday = (last_day.weekday() + 1) % 7
  for _ in range(6 - last_weekday):
    dates.append(
      {
        "date": "",
        "day": "",
        "is_available": False,
        "available_hours": [],
        "available_minutes": [],
      }
    )

  return {
    "dates": dates,
    "current_month": first_day,
    "month_name": first_day.strftime("%B %Y"),
    "prev_month": (first_day - timedelta(days=1)).strftime("%Y-%m"),
    "next_month": (last_day + timedelta(days=1)).strftime("%Y-%m"),
  }


# ============================================================================
# Main Views
# ============================================================================


@login_required
def home(request):
  user_properties = UserProperty.objects.filter(user=request.user)
  context = {
    "user": request.user,
    "user_properties": user_properties,
  }
  return render(request, "partial/home/index.html", context)


# Property view
#
#
#
@login_required
def property_view(request, user_property_id=1):
  user_property = get_object_or_404(UserProperty, id=user_property_id)
  context = {
    "user": request.user,
    "user_property": user_property,
  }
  return render(request, "partial/property_view/index.html", context)


# Explore appliances
#
#
#
@login_required
def explore(request):
  appliances = Appliance.objects.all()
  context = {
    "user": request.user,
    "appliances": appliances,
  }
  return render(request, "partial/explore/index.html", context)


# Explore appliances
#
#
#
@login_required
def profile(request):
  context = {
    "user": request.user,
  }
  return render(request, "partial/profile/index.html", context)


# Property appliance view
#
#
#
@login_required
def property_appliance_view(request, property_id=1, appliance_id=1):
  property = get_object_or_404(Property, id=property_id)
  appliance = get_object_or_404(Appliance, id=appliance_id)
  property_appliance = get_object_or_404(
    PropertyAppliance, property=property, appliance=appliance
  )
  print("############# ID", property_appliance.id)
  appliances = Appliance.objects.filter(appliance_type=appliance.appliance_type)
  context = {
    "user": request.user,
    "property": property,
    "current_appliance": property_appliance,
    "appliances": appliances,
    "property_appliance_id": property_appliance.id,
  }
  return render(request, "partial/property_appliances/index.html", context)


# ============================================================================
# Schedule Modal Views
# ============================================================================


# Appliance modal
#
#
#
@login_required
@require_http_methods("POST")
def appliance_replacement_modal(request, property_id, appliance_id):
  current_property_appliance = get_object_or_404(
    PropertyAppliance, property_id=property_id, appliance_id=appliance_id
  )

  replacement_appliance_id = request.POST.get("appliance_id")
  replacement_appliance = get_object_or_404(Appliance, id=replacement_appliance_id)

  availability_context = get_availability_context()

  context = {
    "appliance": replacement_appliance,
    "property": current_property_appliance.property,
    "property_appliance_id": current_property_appliance.id,
    **availability_context,
  }

  response = render(
    request,
    "partial/property_appliances/modal/index.html",
    context,
  )

  response["HX-Target"] = "#scheduleModal"
  response["HX-Swap"] = "outerHTML"
  response["HX-Trigger-After-Swap"] = "showModal"

  return response


# Schedule replacement
#
#
#
@login_required
@require_http_methods("POST")
def appliance_replacement_modal_submit(request):
  form = ScheduleForm(request.POST)

  if form.is_valid():
    form.save()
    return HttpResponse(
      '<div class="alert alert-success">Schedule created successfully!</div>'
    )
  else:
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ============================================================================
# Add Appliance Modal Views
# ============================================================================


# Add appliance modal
#
#
#
@login_required
@require_http_methods("POST")
def add_property_appliance(request, property_id):
  appliances = Appliance.objects.all()
  user_property = get_object_or_404(UserProperty, id=property_id)

  context = {
    "appliances": appliances,
    "user_property": user_property,
  }

  response = render(
    request,
    "partial/property_view/appliance_add_modal.html",
    context,
  )

  response["HX-Target"] = "#applianceAddModal"
  response["HX-Swap"] = "outerHTML"
  response["HX-Trigger-After-Swap"] = "showAddApplianceModal"

  return response


# Add appliance submit
#
#
#
@login_required
@require_http_methods("POST")
def add_property_appliance_submit(request):
  form = PropertyApplianceForm(request.POST, property_id=request.POST.get("property"))
  if form.is_valid():
    property_appliance = form.save()
    property_appliance.save()
    user_property = get_object_or_404(UserProperty, id=request.POST.get("property"))
    context = {
      "property_appliance": property_appliance,
      "user_property": user_property,
    }
    response = render(
      request,
      "partial/property_view/appliance_row.html",
      context,
    )
    response["HX-Trigger"] = "refreshApplianceList"
    return response
  else:
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ============================================================================
# API Views
# ============================================================================


# Get month dates
#
#
#
@login_required
@require_http_methods(["GET"])
def get_month_dates(request):
  year = request.GET.get("year")
  month = request.GET.get("month")

  try:
    year = int(year) if year and year != "undefined" else None
    month = int(month) if month and month != "undefined" else None
  except (ValueError, TypeError):
    year = None
    month = None

  context = get_availability_context(month, year)
  return JsonResponse(context)


# Delete schedule
#
#
#
#
@login_required
@require_http_methods("POST")
def delete_schedule(request, schedule_id):
  schedule = get_object_or_404(Schedule, id=schedule_id)
  schedule.delete()
  return HttpResponse(
    '<div class="alert alert-success">Schedule deleted successfully!</div>'
  )


# Delete property appliance
#
#
#
#
@login_required
@require_http_methods("POST")
def delete_property_appliance(request, property_appliance_id):
  property_appliance = get_object_or_404(PropertyAppliance, id=property_appliance_id)
  property_appliance.delete()
  return HttpResponse(
    '<div class="alert alert-success">Property appliance deleted successfully!</div>'
  )


# ============================================================================
# Logout
# ============================================================================


# Logout
#
#
#
@login_required
@require_http_methods("GET")
def logout_view(request):
  logout(request)
  return redirect("/admin/login/")
