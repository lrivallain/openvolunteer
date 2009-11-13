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
    (r'^event/need/add/(?P<event_id>\d+)/$', 'event_need_add'),
    # delete
    (r'^event/need/delete/(?P<need_id>\d+)/$', 'event_need_delete'),
    #edit
    (r'^event/need/edit/(?P<need_id>\d+)/$', 'event_need_edit'),

    # ANSWERS views and search tool
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

)

urlpatterns += patterns('',
    # Provide access to css files
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': OPENVOLUNTEER_SYSTEM_ROOT + '/static-files'}),
)
