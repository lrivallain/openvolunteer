#-*- coding: utf-8 -*-
"""
    ---------------------------------------------------------------------------

                               OpenVolunteer
                     Copyright 2009, Ludovic Rivallain

    ---------------------------------------------------------------------------
    This file is part of OpenVolunteer.

    OpenVolunteer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenVolunteer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with OpenVolunteer.  If not, see <http://www.gnu.org/licenses/>.
    ---------------------------------------------------------------------------
"""
from django import forms
from models import *

class VolunteerForm(forms.Form):
    name = forms.CharField(max_length=100)
    firstname = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    phone_home = forms.CharField(required=False, max_length=20)
    phone_mobile = forms.CharField(required=False, max_length=20)
    address = forms.CharField(required=False, widget=forms.Textarea)
    birth_place = forms.CharField(required=False, max_length=100)
    ca_member = forms.BooleanField(required=False)
    comments = forms.CharField(required=False, widget=forms.Textarea)
    avatar = forms.ImageField(required=False)
    delete_avatar = forms.BooleanField(required=False)

class EventForm(forms.Form):
    title = forms.CharField(max_length=100)
    place = forms.CharField(required=False, max_length=100)
    affiche = forms.ImageField(required=False)
    delete_affiche = forms.BooleanField(required=False)

class JobForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(required=False, widget=forms.Textarea)

class AnswerForm(forms.Form):
    presence = forms.ChoiceField(choices=PRESENCE_CHOICES)
    comments = forms.CharField(required=False, widget=forms.Textarea)
