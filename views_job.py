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
def job_index(request):
    """
    Display index for job informations
    """
    jobs = Job.objects.exclude(title="none").all()
    return render_to_response('openvolunteer/job_index.html',
                              {'jobs': jobs},
                              context_instance=RequestContext(request))

@login_required(redirect_field_name='next')
def job_delete(request, job_id):
    """
    Delete current job
    """
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect("/openvolunteer/job/")


@login_required(redirect_field_name='next')
def job_edit(request, job_id):
    """
    Update job infos
    """
    job = get_object_or_404(Job, id=job_id)
    form = JobForm(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                job = job_add_or_edit(request, form, job)
                message = "Modification effectuée !<br><a href='%s'" % job.get_absolute_url()
                message += "' title='Revenir à la liste des postes'>Retour</a>"
                status = "success"
            else:
                message = "La modification a échoué ! (error code: 113)"
                status = "error"
        except:
            message = "La modification a échoué ! (error code: 114)"
            status = "error"
    else:
        volunteers = Volunteer.objects.all()
        boss = job.boss.all()
        sel_opts = ''
        for vol in volunteers:
            sel_opts += "<option value='%d'" % vol.id
            if vol in boss:
                sel_opts += "selected='selected'"
            sel_opts += ">%s %s</option>\n" % (vol.name, vol.firstname)
        return render_to_response('openvolunteer/job_edit.html',
                              {'job': job, 'sel_opts': sel_opts, 'form': form},
                              context_instance=RequestContext(request))
    return render_to_response('openvolunteer/operation_result.html',
                              {'status': status,
                               'message': message},
                              context_instance=RequestContext(request))

@login_required(redirect_field_name='next')
def job_add(request):
    """
    Add job infos
    """
    job = Job()
    form = JobForm(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                job = job_add_or_edit(request, form, job, True)
                message = "L'ajout a été effectué !<br><a href='%s'" % job.get_absolute_url()
                message += "' title='Revenir à la liste des postes'>Retour</a>"
                status = "success"
            else:
                message = "L'ajout a échoué ! (error code: 115)"
                status = "error"
        except:
            message = "L'ajout a échoué ! (error code: 116)"
            status = "error"
    else:
        volunteers = Volunteer.objects.all()
        sel_opts = ''
        for vol in volunteers:
            sel_opts += "<option value='%d'>%s %s</option>\n" % (vol.id, vol.name, vol.firstname)
        return render_to_response('openvolunteer/job_edit.html',
                              {'sel_opts': sel_opts, 'form': form},
                              context_instance=RequestContext(request))
    return render_to_response('openvolunteer/operation_result.html',
                              {'status': status,
                               'message': message},
                              context_instance=RequestContext(request))


def job_add_or_edit(request, form, job, add=False):
    """
    Add or update job infos
    """
    job.title = form.cleaned_data['title']
    job.stripped_title = defaultfilters.slugify(job.title)
    if not add:
        job.boss = request.REQUEST.getlist('boss')
    if (request.REQUEST['description'] != ''):
        job.description = form.cleaned_data['description']
    else: job.description = ''
    job.save()
    # in 2 steps if not existing object to avoid error
    if add:
        job.boss = request.REQUEST.getlist('boss')
        job.save()
    return job
