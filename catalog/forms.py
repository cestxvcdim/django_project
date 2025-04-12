from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check_input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")

    def clean_name(self):
        name = self.cleaned_data.get("name")
        forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно",
                           "мошенничество", "полиция", "радар"]

        for word in forbidden_words:
            if word.lower() in name.lower():
                raise ValidationError(f"Слово '{word}' запрещено использовать в названии продукта. ")

        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно",
                           "мошенничество", "полиция", "радар"]

        for word in forbidden_words:
            if word.lower() in description.lower():
                raise ValidationError(f"Слово '{word}' запрещено использовать в описании продукта.")

        return description

class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
