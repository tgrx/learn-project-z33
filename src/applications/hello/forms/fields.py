from django.forms import CharField

from applications.hello.forms.validatiors import validate_name


class NameField(CharField):
    default_validators = [validate_name]

    def __init__(self, *args, **kwargs):
        kwargs_default = dict(
            min_length=3,
            max_length=1000,
        )
        kwargs.update(kwargs_default)
        super().__init__(*args, **kwargs)
