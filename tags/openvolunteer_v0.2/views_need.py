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

import datetime


@login_required(redirect_field_name='next')
def event_need_add(request, event_id):
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
def event_need_delete(request, need_id):
    """
    Delete a need
    """
    need = get_object_or_404(Need, id=need_id)
    url = need.event.get_absolute_url()
    need.delete()
    return redirect(url)


@login_required(redirect_field_name='next')
def event_need_edit(request, need_id):
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
