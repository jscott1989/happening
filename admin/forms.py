"""Admin forms."""
from django import forms
from payments.models import PaymentHandler


class ConfigurationForm(forms.Form):

    """A form to attach custom configuration variables to."""

    pass


class PaymentHandlerForm(forms.ModelForm):

    """Form for creating/modifying payment handlers."""

    class Meta:
        model = PaymentHandler
        fields = ['description', 'public_key', 'secret_key']
