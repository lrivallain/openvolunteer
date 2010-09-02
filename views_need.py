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
from models import *
from errors import *

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

import datetime


@csrf_protect
@login_required(redirect_field_name='next')
def need_add(request, event_id):
    """
    Add a need for current event
    """
    need = Need()
    need.event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        try:
            need = need_add_or_edit(request, need, True)
        except:
            message = "L'ajout a échoué ! (error code: %d)" % ERROR_NEED_ADD_SAVING
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status,
                                       'message': message},
                                      context_instance=RequestContext(request))
    else:
        jobs = Job.objects.all()
        sel_opts = ''
        for job in jobs:
            sel_opts += "<option value='%d'>%s</option>\n" % (job.id, job.title)
        return render_to_response('openvolunteer/need_edit.html',
                                  {'need': need, 'sel_opts': sel_opts},
                                  context_instance=RequestContext(request))
    return redirect(need.event)


@login_required(redirect_field_name='next')
def need_delete(request, need_id):
    """
    Delete a need
    """
    need = get_object_or_404(Need, id=need_id)
    url = need.event.get_absolute_url()
    need.delete()
    return redirect(url)


@csrf_protect
@login_required(redirect_field_name='next')
def need_edit(request, need_id):
    """
    Update need informations
    """
    need = get_object_or_404(Need, id=need_id)
    if request.method == 'POST':
        try:
            need = need_add_or_edit(request, need, True)
        except:
            message = "L'ajout a échoué ! (error code: %d)" % ERROR_NEED_EDIT_SAVING
            status = "error"
            return render_to_response('openvolunteer/operation_result.html',
                                      {'status': status,
                                       'message': message},
                                      context_instance=RequestContext(request))
    else:
        jobs = Job.objects.all()
        sel_opts = ''
        for job in jobs:
            sel_opts += "<option value='%d'" % job.id
            if job == need.job :
                sel_opts += "selected='selected'"
            sel_opts += ">%s</option>\n" % (job.title)
        return render_to_response('openvolunteer/need_edit.html',
                                  {'need': need, 'sel_opts': sel_opts},
                                  context_instance=RequestContext(request))
    return redirect(need.event)


def need_add_or_edit(request, need, add=False):
    """
    Add or update need infos
    """
    need.number = int(request.REQUEST['number'])
    need.job = Job.objects.get(id=request.REQUEST['job'])
    need.save()
    return need


def need_planning(request, need_id):
    """
    Build a planning for an event and a job
    """
    # get answers for this job and this event if the both exist
    need = get_object_or_404(Need, id=need_id)
    answers = need.get_positives_answers()

    # found base values for timeline
    starts = []
    ends = []
    for answer in answers:
        for schedule in answer.get_all_schedules():
            if schedule.next_day:
                starts.append(schedule.start.hour+24)
                ends.append(schedule.end.hour+24)
            elif (schedule.end.hour == 0):
                starts.append(schedule.start.hour)
                ends.append(schedule.end.hour+24)
            else:
                starts.append(schedule.start.hour)
                ends.append(schedule.end.hour)

    min_h=min(starts)
    max_h=max(ends)+1
    nb_hours=max_h-min_h

    # arbitrary settings
    offset_x=50
    offset_y=70
    name_width=300
    line_offset=30

    # global svg item settings
    svg = {'width': offset_x+(100*nb_hours)+name_width,
           'height': offset_y+10+(30*answers.count()),
           'offset_x':offset_x, 'offset_y':offset_y}

    # timeline settings
    x2=offset_x+(100*nb_hours)
    d="M %d %d L %d %d L %d %d" % (x2-10, offset_y-5, x2,
                                   offset_y, x2-10, offset_y+5)
    timeline = {'x2': x2, 'd': d}

    # build a legend for timeline
    i=0
    current_legend=min_h
    legend=[]
    while(i<=nb_hours):
        if current_legend == 24:
            current_legend=0
        t = "%0*dh00" % (2, current_legend)
        t_legend = {'x': offset_x+(i*100),
                    'y': 50,
                    'text': t}
        legend.append(t_legend)
        current_legend = current_legend+1
        i = i+1

    # build lines to display answer and schedules
    answers_ = []
    i=0
    for answer in answers:
        schedules_ = []
        schedules = answer.get_all_schedules()
        # if no schedules, draw a line with != color on 100%
        if not schedules:
            start_hour = schedule.start.hour
            end_hour = schedule.end.hour
            schedules_.append({
                'x1': offset_x,
                'x2': offset_x+((nb_hours-1)*100),
                'color': '#fffa8f'
            })
        # if schedules, draw line segment for each one
        else:
            for schedule in schedules:
                start_minutes = schedule.start.minute/60.0
                end_minutes = schedule.end.minute/60.0
                if schedule.next_day:
                    start_hour = schedule.start.hour + 24 + start_minutes
                    end_hour = schedule.end.hour + 24 + end_minutes
                elif (schedule.end.hour == 0) or (schedule.end.hour < schedule.start.hour):
                    start_hour = schedule.start.hour + start_minutes
                    end_hour = schedule.end.hour + 24 + end_minutes
                else:
                    start_hour = schedule.start.hour + start_minutes
                    end_hour = schedule.end.hour + end_minutes
                schedules_.append({
                    'x1': offset_x+((start_hour-min_h)*100),
                    'x2': offset_x+((end_hour-min_h)*100),
                    'color': '#00ff00'
                })
        answers_.append({
            'volunteer': answer.volunteer,
            'x': offset_x+(100*nb_hours)+15,
            'y': offset_y+20+(line_offset*i),
            'schedules': schedules_,
            'answer':answer
        })
        # line count
        i = i+1

    # render svg from template with specific mimetype
    return render_to_response('openvolunteer/need_planning.svg',
                              {'svg': svg, 'timeline': timeline,
                               'legend': legend, 'answers':answers_,
                               'need': need},
                              context_instance=RequestContext(request),
                              mimetype="image/svg+xml")
