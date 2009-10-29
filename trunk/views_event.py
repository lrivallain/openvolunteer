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
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime
from forms import *

@login_required(redirect_field_name='next')
def event_index(request):
    """
    Display a search form (and a list of events)
    """
    events = []
    try:
        query = request.GET["q"]
        # if search request is empty or only contains a space, return
        #   specific error
        if query == "" or query == " ":
            events = Event.objects.all().order_by('-date')[:10]
            return render_to_response('openvolunteer/event_index.html',
                                      {'events': events, 'results': results, 'terms': ""},
                                      context_instance=RequestContext(request))
        else:
            search_terms=query.split(' ')
            # get all events
            results = Event.objects.all()
            for term in search_terms:
                # search events corresponding to search term
                results = results.filter(Q(title__icontains = term)|
                                         #Q(date__icontains = term)|
                                         Q(place__icontains = term)).all().order_by('date')
    # If there is no 'q' value, return empty results
    except:
        events = Event.objects.all().order_by('-date')[:10]
        results = []
        query = ""
    return render_to_response('openvolunteer/event_index.html',
                              {'events': events, 'results': results, 'terms': query},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def event_details(request, event_id):
    """
    Display event details and link to modify them
    """
    event = get_object_or_404(Event, id=event_id)
    needs = Need.objects.filter(event=event).all()
    return render_to_response('openvolunteer/event_details.html',
                              {'event': event,
                               'needs': needs},
                              context_instance=RequestContext(request))


@login_required(redirect_field_name='next')
def event_delete(request, event_id):
    """
    Delete current event
    """
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect("/openvolunteer/event/")


@login_required(redirect_field_name='next')
def event_edit(request, event_id):
    """
    Update event infos
    """
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                event = event_add_or_edit(request, form, event)
            except:
                message = "L'ajout a échoué ! (error code: 108)"
                status = "error"
                return render_to_response('openvolunteer/operation_result.html',
                                          {'status': status,
                                           'message': message},
                                          context_instance=RequestContext(request))
            return redirect(event)
        else:
            message = "L'ajout a échoué ! (error code: 107)"
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status,
                                       'message': message},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('openvolunteer/event_edit.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))

@login_required(redirect_field_name='next')
def event_add(request):
    """
    Add or Update event infos
    """
    event = Event()
    form = EventForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                event = event_add_or_edit(request, form, event)
            except:
                message = "L'ajout a échoué ! (error code: 108)"
                status = "error"
                return render_to_response('openvolunteer/operation_result.html',
                                          {'status': status,
                                           'message': message},
                                          context_instance=RequestContext(request))
            return redirect(event)
        else:
            message = "L'ajout a échoué ! (error code: 107)"
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status,
                                       'message': message},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('openvolunteer/event_edit.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


from django.template import defaultfilters
def event_add_or_edit(request, form, event):
    """
    Add or update event infos
    """
    event.title = form.cleaned_data['title']
    event.stripped_title = defaultfilters.slugify(event.title)
    if (request.REQUEST['place'] != ''):
        event.place = form.cleaned_data['place']
    if ((request.REQUEST['date_year'] != '') and
        (request.REQUEST['date_month'] != '') and
        (request.REQUEST['date_day'] != '')):
        event.date = datetime.date(int(request.REQUEST['date_year']),
                                   int(request.REQUEST['date_month']),
                                   int(request.REQUEST['date_day']))
    else: event.date = None
    event.save()
    return event


import csv
@login_required(redirect_field_name='next')
def event_csv(request, event_id):
    """Export volunteers for an event into CSV file"""
    event = get_object_or_404(Event, id=event_id)
    answers = Answer.objects.filter(event=event,presence=True).all().order_by('job')

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % event.stripped_title

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prenom', 'Email', 'Numero de telephone',
                     'Numero de mobile', 'Date de Naissance', 'Poste'])

    for answer in answers :
        if answer.volunteer.birthday :
           birthday = "%d/%d/%d" % (answer.volunteer.birthday.day,
                                    answer.volunteer.birthday.month,
                                    answer.volunteer.birthday.year)
        else:
           birthday = ""
        writer.writerow([unicode(s).encode("cp1252") for s in (
                             answer.volunteer.name,
                             answer.volunteer.firstname,
                             answer.volunteer.email,
                             answer.volunteer.phone_home,
                             answer.volunteer.phone_mobile,
                             birthday,
                             answer.job)
                        ])
    return response
