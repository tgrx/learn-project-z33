from django import forms


def validate_name(value: str) -> None:
    if not value:
        raise forms.ValidationError("MUST NOT be empty")

    if not value.isalnum() or value.isdigit():
        raise forms.ValidationError("MUST contain letters")
