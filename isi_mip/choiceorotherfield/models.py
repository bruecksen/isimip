from django.core import exceptions
from django.db import models

from .fields import MyTypedChoiceField


class ChoiceOrOtherField(models.CharField):
    def formfield(self, **kwargs):
        field = MyTypedChoiceField
        defaults = {'choices_form_class': field}
        defaults.update(kwargs)
        return super(ChoiceOrOtherField, self).formfield(**defaults)

    def validate(self, value, model_instance):
        """
        Validates value and throws ValidationError. Subclasses should override
        this to provide validation logic.
        """
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')