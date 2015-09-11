"""Happening custom form elements."""
from django import forms
from django.template.loader import render_to_string
from happening.utils import convert_to_underscore
import json
from django.core.files import File
from happening.storage import storage
from events.models import Event


class PropertiesWidget(forms.Widget):

    """A widget that allows for configuring a list of property types."""

    def __init__(self, *args, **kwargs):
        """Create a properties widget."""
        if 'property_types' in kwargs:
            self.property_types = kwargs.pop('property_types')
        else:
            # TODO: Don't  hardcode these types
            self.property_types = (
                ("CharField", "Text"),
                ("EmailField", "Email"),
                ("IntegerField", "Number"),
                ("URLField", "URL"),
                ("BooleanField", "Boolean")
            )
        super(PropertiesWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        return render_to_string("forms/widgets/properties_widget.html", {
            "name": name,
            "value": json.dumps(value),
            "property_types": self.property_types
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        return data[name]


class PropertiesField(forms.CharField):

    """A field that allows for configuring a list of property types."""

    widget = PropertiesWidget

    def clean(self, value):
        """Turn the JSON into a Python list."""
        return json.loads(value)


class CustomPropertiesWidget(forms.Widget):

    """A widget that allows for inputting a list of properties."""

    def __init__(self, *args, **kwargs):
        """Create a properties widget."""
        self.fields = kwargs.pop("fields")
        super(CustomPropertiesWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        # Create a form representing the fields
        if not value:
            value = {}
        if type(value) == str:
            # When the form reloads we need to turn it back into a dict
            value = json.loads(value)
        form = forms.Form()
        for field in self.fields:
            n = convert_to_underscore(field['name'])
            form.fields[name + "_" + n] = getattr(forms, field['type'])(
                label=field['name'], initial=value.get(n))

        return render_to_string(
            "forms/widgets/custom_properties_widget.html",
            {"form": form})

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        store_data = {}
        for k in data.keys():
            if k.startswith(name + "_"):
                store_data[k[len(name) + 1:]] = data[k]
        return json.dumps(store_data)


class CustomPropertiesField(forms.CharField):

    """A field that allows for inputting multiple custom properties."""

    widget = CustomPropertiesWidget

    def __init__(self, *args, **kwargs):
        """Create the Custom Properties Field."""
        # Remove the overall label, as we want the inputs to look native
        kwargs['label'] = ''
        kwargs['widget'] = self.widget(fields=kwargs.pop('fields'))
        super(CustomPropertiesField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Turn the JSON into a Python list."""
        return json.loads(value)


class MarkdownWidget(forms.Textarea):

    """A widget that uses EpicEditor."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'markdown-widget ' + attrs.get('class', '')
        return super(MarkdownWidget, self).render(name, value, attrs)


class MarkdownField(forms.CharField):

    """A field that uses an EpicEditor markdown editor."""

    widget = MarkdownWidget


class DateTimeWidget(forms.TextInput):

    """A widget that adds a DateTime Picker."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'datetime-widget ' + attrs.get('class', '')
        attrs['data-datetime-format'] = 'Y-m-d H:i:00'
        return super(DateTimeWidget, self).render(name, value, attrs)


class DateWidget(forms.TextInput):

    """A widget that adds a Date Picker."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'date-widget ' + attrs.get('class', '')
        attrs['data-date-format'] = 'Y-m-d'
        return super(DateWidget, self).render(name, value, attrs)


class TimeWidget(forms.TextInput):

    """A widget that adds a time Picker."""

    def render(self, name, value, attrs):
        """Render the widget."""
        attrs['class'] = 'time-widget ' + attrs.get('class', '')
        attrs['data-time-format'] = 'H:i'
        return super(DateWidget, self).render(name, value, attrs)


class ImageWidget(forms.TextInput):

    """A widget that adds an ajax image uploader."""

    def render(self, name, value, attrs):
        """Render the widget."""
        return render_to_string("forms/widgets/image_widget.html", {
            "name": name,
            "value": value
        })


class ImageField(forms.ImageField):

    """An input for an image file."""

    widget = ImageWidget

    def to_python(self, value):
        """Get the image selected."""
        # This just needs to return a File

        # We force this here so that a "None" value isn't an error
        self.required = False

        if not value:
            return None

        is_temp = False
        if value.startswith("tmp"):
            is_temp = True

        # TODO: What happens if they use ../../ etc.
        # Can they mess with stuff they shouldn't?

        # TODO: Rename the file to remove the prefix
        filename = value.rsplit("/", 1)[-1]
        if is_temp:
            filename = filename.split("_", 1)[1]

        return File(storage.open(value))


class EmailsWidget(forms.Widget):

    """A widget that allows for configuring emails."""

    def __init__(self, *args, **kwargs):
        """Create an emails widget."""
        super(EmailsWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        if not value:
            value = []
        if not isinstance(value, basestring):
            value = json.dumps(value)
        return render_to_string("forms/widgets/emails_widget.html", {
            "name": name,
            "value": value,
            "events": Event.objects.all()
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a string."""
        if name in data:
            return data[name]
        return ''


class EmailsField(forms.CharField):

    """A field that allows for configuring emails."""

    widget = EmailsWidget

    def clean(self, value):
        """Turn the JSON into a Python list."""
        try:
            return json.loads(value)
        except ValueError:
            return []


class CheckboxInput(forms.widgets.CheckboxInput):

    """A checkbox which wraps the label."""

    def __init__(self, *args, **kwargs):
        """Create a CheckboxInput."""
        self.label = kwargs.pop('label')
        super(CheckboxInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        """Render the CheckboxInput."""
        return "<label>%s %s</label>" % (
            super(CheckboxInput, self).render(name, value, attrs),
            self.label)


class BooleanField(forms.BooleanField):

    """BooleanField with correct widget for Happening."""

    widget = CheckboxInput

    def __init__(self, *args, **kwargs):
        """Create the Boolean Field."""
        # Remove the overall label, as we want the inputs to look native
        kwargs['widget'] = self.widget(label=kwargs.get('label', ''))
        kwargs['label'] = ''
        super(BooleanField, self).__init__(*args, **kwargs)


class AddressWidget(forms.Widget):

    """A widget that allows for inputting an address."""

    def __init__(self, *args, **kwargs):
        """Create an address widget."""
        super(AddressWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs):
        """Render the widget."""
        if not value:
            value = []
        if isinstance(value, basestring):
            value = json.loads(value)
        return render_to_string("forms/widgets/address_widget.html", {
            "name": name,
            "value": value
        })

    def value_from_datadict(self, data, files, name):
        """Get the value as a dict."""
        line_1 = data.get(name + '_line_1')
        line_2 = data.get(name + '_line_2')
        line_3 = data.get(name + '_line_3')
        city = data.get(name + '_city')
        state = data.get(name + '_state')
        country = data.get(name + '_country')
        postcode = data.get(name + '_postcode')
        longitude = data.get(name + '_longitude')
        latitude = data.get(name + '_latitude')

        return {
            "line_1": line_1,
            "line_2": line_2,
            "line_3": line_3,
            "city": city,
            "state": state,
            "country": country,
            "postcode": postcode,
            "longitude": longitude,
            "latitude": latitude
        }


class AddressField(forms.CharField):

    """A field for inputting an address."""

    widget = AddressWidget

    def to_python(self, value):
        """Get the address as dict."""
        # This just needs to return the value
        return value
