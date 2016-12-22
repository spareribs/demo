# coding: utf-8
# author: spareribs

from django import forms

class TodolistaddForm(forms.Form):
    body = forms.CharField()