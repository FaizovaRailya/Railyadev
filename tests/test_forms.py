"""Тесты формы контактов."""

import pytest

from apps.core.forms import ContactForm


@pytest.mark.django_db
class TestContactForm:
    def test_valid_data(self):
        form = ContactForm(
            data={
                "name": "Иван",
                "email": "ivan@example.com",
                "phone": "",
                "message": "Нужен сайт на Django, подробности в письме.",
                "website": "",
            }
        )
        assert form.is_valid(), form.errors

    def test_message_too_short(self):
        form = ContactForm(
            data={
                "name": "Иван",
                "email": "ivan@example.com",
                "message": "Коротко",
                "website": "",
            }
        )
        assert not form.is_valid()
        assert "message" in form.errors

    def test_message_too_long(self):
        form = ContactForm(
            data={
                "name": "Иван",
                "email": "ivan@example.com",
                "message": "x" * 2001,
                "website": "",
            }
        )
        assert not form.is_valid()
        assert "message" in form.errors

    def test_honeypot_filled(self):
        """Если honeypot заполнен — это спам, форма невалидна."""
        form = ContactForm(
            data={
                "name": "Бот",
                "email": "bot@example.com",
                "message": "Спам-сообщение длиной больше 10",
                "website": "http://spam.com",
            }
        )
        assert not form.is_valid()
        assert "website" in form.errors

    def test_invalid_email(self):
        form = ContactForm(
            data={
                "name": "Иван",
                "email": "not-an-email",
                "message": "Достаточно длинное сообщение",
                "website": "",
            }
        )
        assert not form.is_valid()
        assert "email" in form.errors
