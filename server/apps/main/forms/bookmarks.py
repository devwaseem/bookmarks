from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from server.apps.main.constants import REGEX_URL
from server.apps.main.helpers.url import is_valid_url

from server.apps.main.models.bookmark import LinkType
from server.apps.main.services.url import is_url_active


class MultiCollectionsField(forms.Field):
    def to_python(self, value: str | None) -> list[str] | None:
        if value:
            return value.split(",")
        return None


class AddBookmarkWidgetForm(forms.Form):
    link = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "placeholder": "https://example.com",
                # "x-model": "link",
                # "x-ref": "link",
            }
        ),
        validators=[RegexValidator(regex=REGEX_URL)],
    )
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Quick fox jump over the fence",
                # "x-model": "title",
                # "x-ref": "title",
            }
        ),
    )
    # description = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": "3", "cols": "5"}))
    link_type = forms.ChoiceField(
        choices=LinkType.choices,
        initial=LinkType.LINK,
        label="Type",
    )
    add_to_reading_list = forms.BooleanField(initial=False, required=False)
    collections = MultiCollectionsField(widget=forms.HiddenInput(), required=False)

    def clean_link(self):
        link = self.cleaned_data["link"]
        if not is_valid_url(link):
            raise ValidationError("Invalid Link")
        if not is_url_active(link):
            raise ValidationError("Link doesn't seem to exists")
        return link

    def clean_collections(self):
        collections = self.cleaned_data["collections"]
        if not collections:
            raise ValidationError("One or more collections required")
        return collections


class ArchiveBookmarkWidgetForm(forms.Form):
    archive_bookmark = forms.BooleanField(required=False)
