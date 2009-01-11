from ovsettings import *
from django.conf.urls.defaults import *
from django.contrib.comments import urls

urlpatterns = patterns('demo.openvolunteer.views',
    # MAIN view
    (r'^$', 'index'),
    
    # VOLUNTEERS views, search tool and vcard generation
    (r'^volunteer/$','volunteer_index'),
    (r'^volunteer/(?P<volunteer_id>\d+)/$', 'volunteer_details'),
    (r'^vcard/(?P<vcard_type>\D{3,})/(?P<volunteer_id>\d+)/$', 'volunteer_vcard'),
    
    # EVENTS views and search tool
    (r'^event/$', 'event_index'),
    (r'^event/(?P<event_id>\d+)$', 'event_details'),
    
    # ANSWERS views and search tool
    (r'^answers/event/(?P<event_id>\d+)/$', 'event_volunteers'),
    (r'^answers/nocontact/event/(?P<event_id>\d+)/$', 'event_tocontact'),
    (r'^answer/$','answer_index'),
    
    # JOBS views and index
    (r'^job/$','job_index'),
    (r'^job/(?P<selected_job>\D{3,})/$','job_index'),
    
    # LISTS generators
    (r'^list/volunteer/$','list_volunteer_index'),
    (r'^list/volunteer/csv/$','csv_generator'),
)

urlpatterns += patterns('',
    # Provide MEDIA data to application
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': APPLICATION_PATH + '/media'}), #APPLICATION_PATH + '/media'}),
)
