#
#
#
#
from datetime import datetime

from django import template

register = template.Library()


#
#
#
#
@register.filter
def format_snake_case(value):
  return value.replace("_", " ").title()


#
#
#
#
@register.filter
def multiply(value, arg):
  try:
    return float(value) * float(arg)
  except (ValueError, TypeError):
    return ""


#
#
#
#
@register.filter
def next_available_dates(dates, count=3):
  if dates is None:
    return []
  available_dates = [date for date in dates if date["is_available"]]
  return available_dates[:count]


#
#
#
#
@register.filter
def get(value, arg):
  if isinstance(value, dict):
    return value.get(arg, "")
  return value


#
#
#
#
@register.filter
def parse_date(value):
  try:
    return datetime.strptime(value, "%Y-%m-%d")
  except (ValueError, TypeError):
    return None
