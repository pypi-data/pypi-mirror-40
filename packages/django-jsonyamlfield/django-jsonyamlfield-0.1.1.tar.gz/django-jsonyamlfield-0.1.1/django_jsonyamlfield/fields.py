import yaml
from django.contrib.postgres import fields, forms
from django.utils.translation import gettext_lazy as _


class InvalidJSONYAMLInput(str):
    pass


class JSONYAMLString(str):
    pass


class JSONYAMLFormField(forms.JSONField):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid YAML."),
    }

    def to_python(self, value):
        if self.disabled:
            return value
        if value in self.empty_values:
            return None
        elif isinstance(value, (list, dict, int, float, JSONYAMLString)):
            return value
        try:
            converted = yaml.load(value)
        except yaml.YAMLError:
            raise forms.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
        if isinstance(converted, str):
            return JSONYAMLString(converted)
        else:
            return converted

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            return yaml.load(data)
        except yaml.YAMLError:
            return InvalidJSONYAMLInput(data)

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONYAMLInput):
            return value
        return yaml.dump(value, default_flow_style=False)

    def widget_attrs(self, widget):
        return {'class': 'vLargeTextField'}


class JSONYAMLField(fields.JSONField):
    def formfield(self, **kwargs):
        defaults = {'form_class': JSONYAMLFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
