# From stable release (0.2) to trunk #
  1. copy for backup needs the folder of openvolunteer previous release
  1. get files from trunk by: ` svn checkout http://openvolunteer.googlecode.com/svn/trunk/ openvolunteer`
  1. changes settings in openvolunteer/ovsettings.py file
  1. on django (&openvolunteer) database: `` ALTER TABLE `openvolunteer_answer` ADD `updating_vol_info` BOOL NOT NULL , ADD `updated_vol_info` BOOL NOT NULL ; ALTER TABLE `openvolunteer_schedule` ADD `next_day` BOOL NOT NULL AFTER `end` ; ``
  1. synchronize database new models: ` python manage.py syncdb `