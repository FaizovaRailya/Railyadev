"""Формы ядра."""

from django import forms
from django.core.exceptions import ValidationError

from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """
    Форма заявки с honeypot-полем.

    Honeypot: скрытое поле `website`, которое человек не видит,
    но боты автозаполнения заполняют. Если оно не пустое — это спам.
    """

    # Honeypot-поле. Не входит в модель ContactRequest.
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="",
    )

    class Meta:
        model = ContactRequest
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 ..."}),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Расскажите о проекте",
                    "rows": 5,
                }
            ),
        }

    def clean_message(self):
        message = self.cleaned_data["message"]
        if not 10 <= len(message) <= 2000:
            raise ValidationError("Сообщение должно быть от 10 до 2000 символов.")
        return message

    def clean_website(self):
        # Поле скрыто от пользователя. Если оно заполнено — это бот.
        value = self.cleaned_data.get("website", "")
        if value:
            raise ValidationError("Спам.")
        return ""
