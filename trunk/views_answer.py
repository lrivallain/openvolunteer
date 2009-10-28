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
from forms import *

@login_required(redirect_field_name='next')
def answer_index(request):
    """
    Display answers search form or results
    """
    try:
        query_volunteer = request.GET["v"]
        query_event = request.GET["e"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query_event == "" or query_event == " ":
            events = Event.objects.all()
            return render_to_response('openvolunteer/answer_index.html',
                                      {'results': [],'events': events, 'terms': ""},
                                      context_instance=RequestContext(request))
        event = Event.objects.get(id=query_event)
        answers = Answer.objects.filter(event=event).all()

        # if volunteer fied is not empty, filter the result to get
        #   only correspondant volunteers.
        if query_volunteer != "" and query_volunteer != " ":
            # to do... so do nothing for the moment
            query_volunteer = ""

    # If there is no 'v' or 'e' value, return empty results
    except:
        event = ""
        answers = []
        query_volunteer = ""
    events = Event.objects.all()
    return render_to_response('openvolunteer/answer_index.html',
                              {'results': answers,'events': events, 'event': event, 'terms': query_volunteer},
                              context_instance=RequestContext(request))
