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
from demo.openvolunteer.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime

from views_volunteer import *
from views_event import *
from views_answer import *
from views_job import *

@login_required(redirect_field_name='next')
def index(request):
    """
    Open volunteers home page - Display links to main parts
    of interface
    """
    return render_to_response('openvolunteer/index.html',{},
                               context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def list_volunteer_index(request):
    """
    Display a form to generate a filtered list of volunteers
    """
    if request.method == 'GET':
        return render_to_response('openvolunteer/list_volunteer_form.html',{},context_instance=RequestContext(request))
    elif request.method == 'POST':
        volunteers = Volunteer.objects.all()
        try:
            filter = request.REQUEST["filter_address"]
            volunteers = volunteers.exclude(address="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_phone"]
            volunteers = volunteers.exclude(phone_home="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_mobile"]
            volunteers = volunteers.exclude(phone_mobile="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_email"]
            volunteers = volunteers.exclude(email="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_ca"]
            volunteers = volunteers.exclude(ca_member="")
        except:
            pass
        try:
            filter = request.REQUEST["filter_old"]
            print filter
            if (filter == 'on'):
                limit = datetime.date.today()
                limit = limit.replace(limit.year-18)
                volunteers = volunteers.exclude(birthday__gt=limit)
        except:
            pass
        try:
            filter = request.REQUEST["filter_name"]
            search_terms=filter.split(' ')
            print search_terms
            for term in search_terms:
                print term
                # search volunteers corresponding to search term
                volunteers = volunteers.filter(Q(name__icontains = term)|
                                               Q(firstname__icontains = term)).all()
        except:
            pass
        return render_to_response('openvolunteer/list_volunteer_form.html',
                              {'volunteers': volunteers},
                              context_instance=RequestContext(request))
