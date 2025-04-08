class ApplianceTypeConverter:
  regex = "washing_machine|dryer"

  def to_python(self, value):
    return str(value)

  def to_url(self, value):
    return value
