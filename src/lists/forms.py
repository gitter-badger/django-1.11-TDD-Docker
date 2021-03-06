"""
    DOC STRING
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item


# class ItemForm(forms.Form):
#     """
#     DOC  DOC  DOC
#     """
#     item_text = forms.CharField(
#             widget=forms.fields.TextInput(attrs={
#                 'placeholder': 'Enter a to-do item',
#                 'class': 'form-control input-lg',
#         }),
#     )

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):
    """
    DOC  DOC  DOC
    """
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
                'text': forms.fields.TextInput(attrs={
                    'placeholder': 'Enter a to-do item',
                    'class' : 'form-control input-lg',
                }),
        }
        error_messages = {
                'text': {'required': EMPTY_ITEM_ERROR}
        }

    
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    """
    DOC  DOC  DOC
    """
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validation_unique(self):
        try:
            self.instance.validation_unique()
        except ValidationError as e:
            e.error_dict = {'text': [ DUPLICATE_ITEM_ERROR ]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)
