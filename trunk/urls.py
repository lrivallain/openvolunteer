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
from ovsettings import OPENVOLUNTEER_APP_PREFIX, OPENVOLUNTEER_SYSTEM_ROOT
from django.conf.urls.defaults import *
from django.contrib.comments import urls


urlpatterns = patterns(OPENVOLUNTEER_APP_PREFIX + 'views',
    # WELCOME view
    (r'^$', 'index'),

    # VOLUNTEERS
    # search
    (r'^volunteer/$','volunteer_index'),
    # view
    (r'^volunteer/(?P<volunteer_id>\d+)/$', 'volunteer_details'),
    # vcard generation
    (r'^volunteer/vcard/(?P<volunteer_id>\d+)/$', 'volunteer_vcard'),
    # add
    (r'^volunteer/add/$','volunteer_add'),
    # delete
    (r'^volunteer/delete/(?P<volunteer_id>\d+)/$', 'volunteer_delete'),
    # edit
    (r'^volunteer/edit/(?P<volunteer_id>\d+)/$', 'volunteer_edit'),
    # lists generator
    (r'^volunteer/list/$','list_volunteer_index'),
    # lists generator by previous job
    (r'^volunteer/by-job/(?P<job_id>\d+)/$','volunteer_byjob'),

    # EVENTS
    # search
    (r'^event/$', 'event_index'),
    # view
    (r'^event/(?P<event_id>\d+)/$', 'event_details'),
    # add
    (r'^event/add/$', 'event_add'),
    # delete
    (r'^event/delete/(?P<event_id>\d+)/$', 'event_delete'),
    # edit
    (r'^event/edit/(?P<event_id>\d+)/$', 'event_edit'),
    # csv export
    (r'^event/csv/(?P<event_id>\d+)/$', 'event_csv'),

    # NEEDS
    # add
    (r'^need/add/(?P<event_id>\d+)/$', 'need_add'),
    # delete
    (r'^need/delete/(?P<need_id>\d+)/$', 'need_delete'),
    # edit
    (r'^need/edit/(?P<need_id>\d+)/$', 'need_edit'),
    # planning
    (r'^need/planning/(?P<need_id>\d+)/$', 'need_planning'),

    # ANSWERS
    # search and view (all answer for an event)
    (r'^answer/$','answer_index'),
    # view (ok and unknow)
    (r'^answer/positive/(?P<event_id>\d+)/$', 'answer_positives'),
    (r'^answer/unknown/(?P<event_id>\d+)/$', 'answer_tocontact'),
    # add (from event and from unknow answers list
    (r'^event/answer/add/(?P<event_id>\d+)/$', 'event_answer_add'),
    (r'^event/answer/add/(?P<event_id>\d+)/(?P<volunteer_id>\d+)/$', 'event_answer_add'),
    # delete
    (r'^event/answer/delete/(?P<answer_id>\d+)/$', 'event_answer_delete'),
    # edit
    (r'^event/answer/edit/(?P<answer_id>\d+)/$', 'event_answer_edit'),

    # JOBS
    # all job list
    (r'^job/$','job_index'),
    # add
    (r'^job/add/$','job_add'),
    # delete
    (r'^job/delete/(?P<job_id>\d+)/$','job_delete'),
    # edit
    (r'^job/edit/(?P<job_id>\d+)/$','job_edit'),

    # COMMENT
    # add
    (r'^event/comment/add/(?P<event_id>\d+)/$', 'event_comment_add'),
    # delete
    (r'^event/comment/delete/(?P<comment_id>\d+)/$', 'event_comment_delete'),

    # API
    (r'^api/volunteer/get/$','api_volunteer_get'),
#    (r'^api/event/get/$','api_event_get'),
)

urlpatterns += patterns('',
    # Provide access to css files
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': OPENVOLUNTEER_SYSTEM_ROOT + '/static-files'}),
)
