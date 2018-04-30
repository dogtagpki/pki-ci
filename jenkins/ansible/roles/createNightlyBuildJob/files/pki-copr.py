#!/usr/bin/python3
#
# Authors:
#     Dinesh Prasanth M K <dmoluguw@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2017 Red Hat, Inc.
# All rights reserved.
#

import getopt
import sys

from copr import CoprClient

from utils import Utils

# The COPR repo to work with
REPO = "10.6-nightly"

def print_help():
        print('Usage: pki-copr.py [options]')
        print()
        print('  -r, --repo <COPR repo name>        COPR Repository name.')
        print('  -g, --group <group name>           Group name.')
        print('  -p, --project <group/reponame>     Project name.')
        print()

try:
	opts, args = getopt.gnu_getopt(sys.argv, 't:r:g:p:', [
		'token=', 'repo=', 'group=', 'project='])

except getopt.GetoptError as e:
    print('ERROR: ' + str(e))
    print_help()
    sys.exit(1)

token = None
repo = None
group = 'pki'
project= None

for o, a in opts:
    if o in ('-r', '--repo'):
        repo = a

    elif o in ('-g', '--group'):
        group = a

    elif o in ('-p', '--project'):
	    project = a

    else:
        print('ERROR: unknown option ' + o)
        print_help()
        sys.exit(1)

if not repo and not project:
    repo = REPO

# Initialize Utils with the Repo we are going to work with
util = Utils(repo=REPO)

projectID = util.getProjectID(searchQuery=project, name=repo, group=group)

if projectID is None:
    print('ERROR: projectID cannot be obtained') 
    sys.exit(2)

deleteBuildIDs = util.getDeleteBuildIDs(projectID=projectID, package='pki-core', days=7)

# Get COPR API token using official COPR Client
cli = CoprClient.create_from_file_config()

for deleteBuildID in deleteBuildIDs:
    response = util.deleteBuild(buildID=deleteBuildID, login=cli.login, token=cli.token)
    if response is not None:
        result = {
            204: "was removed successfully",
            400: "can't be deleted currently",
            403: "authroization failed",
            404: "doesn't exists"
        }[response.status_code]
        print("Build ID:", deleteBuildID, result)
    else:
        print("Build ID:", deleteBuildID, " can't be deleted for unknown reasons!")
    