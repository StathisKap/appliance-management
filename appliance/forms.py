#
#
#
#
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from .models import Appliance, PropertyAppliance, Schedule, Usage


#
#
#
#
class ScheduleForm(forms.ModelForm):
  property_appliance_id = forms.IntegerField(widget=forms.HiddenInput())
  replacement_appliance_id = forms.IntegerField(widget=forms.HiddenInput())

  date = forms.DateField(
    widget=forms.DateInput(
      attrs={"class": "input input-bordered w-full", "placeholder": "Date"}
    )
  )

  #
  #
  #
  #
  hour = forms.IntegerField(
    widget=forms.NumberInput(
      attrs={
        "class": "input input-bordered w-full",
        "placeholder": "Hour (0-23)",
        "min": "0",
        "max": "23",
      }
    ),
    validators=[MinValueValidator(0), MaxValueValidator(23)],
  )

  #
  #
  #
  #
  minute = forms.IntegerField(
    widget=forms.NumberInput(
      attrs={
        "class": "input input-bordered w-full",
        "placeholder": "Minute (0-59)",
        "min": "0",
        "max": "59",
      }
    ),
    validators=[MinValueValidator(0), MaxValueValidator(59)],
  )

  #
  #
  #
  #
  notifications_enabled = forms.BooleanField(
    required=False, widget=forms.CheckboxInput(attrs={"class": "checkbox"})
  )

  #
  #
  #
  #
  tenant_email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={"class": "input input-bordered w-full", "placeholder": "Email"}
    ),
    required=False,
  )

  #
  #
  #
  #
  tenant_phone = forms.CharField(
    widget=forms.TextInput(
      attrs={"class": "input input-bordered w-full", "placeholder": "Phone"}
    ),
    required=False,
  )

  #
  #
  #
  #
  def clean_property_appliance_id(self):
    property_appliance_id = self.cleaned_data.get("property_appliance_id")
    try:
      property_appliance = PropertyAppliance.objects.get(id=property_appliance_id)
      return property_appliance
    except PropertyAppliance.DoesNotExist:
      raise ValidationError("Invalid property appliance") from None

  def clean_replacement_appliance_id(self):
    replacement_appliance_id = self.cleaned_data.get("replacement_appliance_id")
    try:
      replacement_appliance = Appliance.objects.get(id=replacement_appliance_id)
      return replacement_appliance
    except Appliance.DoesNotExist:
      raise ValidationError("Invalid replacement appliance") from None

  #
  #
  #
  #
  def clean_date(self):
    date = self.cleaned_data["date"]
    if date < timezone.now().date():
      raise ValidationError("Cannot schedule for past dates")
    return date

  #
  #
  #
  #
  def clean_tenant_phone(self):
    phone = self.cleaned_data.get("tenant_phone")
    if phone:
      # Remove any non-digit characters and leading/trailing whitespace
      phone = "".join(filter(str.isdigit, phone.strip()))
      if len(phone) < 10:
        raise ValidationError("Phone number must be at least 10 digits")
    return phone

  #
  #
  #
  #
  class Meta:
    model = Schedule
    fields = (
      "property_appliance_id",
      "replacement_appliance_id",
      "date",
      "hour",
      "minute",
      "notifications_enabled",
      "tenant_email",
      "tenant_phone",
    )

  #
  #
  #
  #
  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.property_appliance = self.cleaned_data["property_appliance_id"]
    instance.replacement_appliance = self.cleaned_data["replacement_appliance_id"]
    if commit:
      instance.save()
    return instance


#
#
#
#
class PropertyApplianceForm(forms.ModelForm):
  appliance = forms.IntegerField()
  actual_cost = forms.IntegerField(required=False)
  actual_warranty_period = forms.DurationField(required=False)
  usage = forms.ChoiceField(choices=[(u.value, u.name) for u in Usage])

  class Meta:
    model = PropertyAppliance
    fields = [
      "appliance",
      "actual_cost",
      "actual_warranty_period",
      "usage",
    ]

  def __init__(self, *args, **kwargs):
    self.property_id = kwargs.pop("property_id", None)
    super().__init__(*args, **kwargs)

  def clean_appliance(self):
    appliance_id = self.cleaned_data.get("appliance")
    try:
      return Appliance.objects.get(id=appliance_id)
    except Appliance.DoesNotExist:
      raise ValidationError("Invalid appliance") from None

  def clean_actual_cost(self):
    actual_cost = self.cleaned_data.get("actual_cost")
    if actual_cost is not None and actual_cost < 0:
      raise ValidationError("Cost cannot be negative")
    return actual_cost

  def clean_actual_warranty_period(self):
    warranty_period = self.cleaned_data.get("actual_warranty_period")
    if warranty_period is not None and warranty_period.days < 0:
      raise ValidationError("Warranty period cannot be negative")
    return warranty_period

  def clean_usage(self):
    usage = self.cleaned_data.get("usage")
    if usage not in [u.value for u in Usage]:
      raise ValidationError("Invalid usage level")
    return usage

  def clean(self):
    cleaned_data = super().clean()
    if not self.property_id:
      raise ValidationError("Property ID is required")
    return cleaned_data

  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.property_id = self.property_id
    if commit:
      instance.save()
    return instance
