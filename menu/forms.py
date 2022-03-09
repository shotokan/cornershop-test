from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Field, Fieldset, Layout, Row, Submit

from menu.models import Menu, MenuItem

from .item_layout_object import Formset

CREATE_MENU_OPTION_FIELDS = ["option1", "option2", "option3", "option4"]


class CreateMenuForm(forms.ModelForm):
    """Form to create new menu and its items"""

    class Meta:
        model = Menu
        fields = ["date"]

    date = forms.DateField(widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        super(CreateMenuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_show_errors = False
        self.helper.form_class = ""
        self.helper.label_class = "mb-8"
        self.helper.field_class = "mb-9"
        self.helper.layout = Layout(
            Row(Field("date", css_class="mb-8")),
            HTML("<hr>"),
            Row(
                Fieldset("Add Items", Formset("description")),
                HTML("<hr>"),
                css_class="d-block text-center",
            ),
            ButtonHolder(Submit("submit", "save"), css_class="d-block btn-block"),
        )


class ItemForm(forms.ModelForm):
    """Inline form for items elements that are related to de menu"""

    class Meta:
        model = MenuItem
        fields = ["description"]

    description = forms.CharField(widget=forms.Textarea)


OPTION_FORM_SET = inlineformset_factory(
    Menu, MenuItem, form=ItemForm, fields=["description"], extra=4, can_delete=True
)

OPTION_FORM_SET_UPDATE = inlineformset_factory(
    Menu, MenuItem, form=ItemForm, fields=["description"], extra=0, can_delete=True
)
