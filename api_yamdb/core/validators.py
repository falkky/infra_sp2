from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class validate_range(object):
    """Валидация значения в диапазоне"""
    def compare(self, a, b, c):
        return a >= c and a <= b

    def clean(self, x):
        return x

    message = ('Убедитесь, что введенное значение в диапазоне между'
               ' %(limit_min)s и %(limit_max)s (значение %(show_value)s).')
    code = 'limit_value'

    def __init__(self, limit_min, limit_max):
        self.limit_min = limit_min
        self.limit_max = limit_max

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {'limit_min': self.limit_min, 'limit_max': self.limit_max,
                  'show_value': cleaned}
        if self.compare(cleaned, self.limit_min, self.limit_max):
            raise ValidationError(self.message, code=self.code, params=params)
