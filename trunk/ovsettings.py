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
###############################################################################
#                       Main settings for OV app                              #
###############################################################################
# Django project name
OPENVOLUNTEER_PROJ_NAME   = "demo"

# This application name (no change is needed in most cases)
OPENVOLUNTEER_APP_NAME    = "openvolunteer"

# Path (from root) where the project is stored on system
OPENVOLUNTEER_PROJ_ROOT   = "/home/pampryl/working/demo"



###############################################################################
#                !!! DO NOT EDIT THIS PART OF SETTINGS !!!                    #
###############################################################################
# Something like "project.app." string
OPENVOLUNTEER_APP_PREFIX  = "%s.%s." % (OPENVOLUNTEER_PROJ_NAME, OPENVOLUNTEER_APP_NAME)

# Something like "/home/user/project/app/" string
OPENVOLUNTEER_SYSTEM_ROOT = "%s/%s" % (OPENVOLUNTEER_PROJ_ROOT, OPENVOLUNTEER_APP_NAME)

# Something like "/app" string
OPENVOLUNTEER_WEB_ROOT    = "/%s" % OPENVOLUNTEER_APP_NAME

# Something like "http://host.domain.tld/media/app" string
from django.conf import settings
OPENVOLUNTEER_MEDIA_URL   = settings.MEDIA_URL + OPENVOLUNTEER_APP_NAME
