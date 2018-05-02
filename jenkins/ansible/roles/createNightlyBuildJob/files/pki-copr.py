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

from copr.client_v2.client import CoprClient

from utils import CoprUtil

def print_help():
        print('Usage: pki-copr.py [options]')
        print()
        print('  -r, --repo <COPR repo name>        COPR Repository name.')
        print('  -g, --group <group name>           Group name.')
        print()

try:
	opts, args = getopt.gnu_getopt(sys.argv, 'g:r:', [
		'group=', 'repo='])

except getopt.GetoptError as e:
    print('ERROR: ' + str(e))
    print_help()
    sys.exit(1)

# The COPR repo to work with
repo = "10.6-nightly"
group = 'pki'

for o, a in opts:
    if o in ('-r', '--repo'):
        repo = a

    elif o in ('-g', '--group'):
        group = a

    else:
        print('ERROR: unknown option ' + o)
        print_help()
        sys.exit(1)

# Get COPR API token using official COPR Client
client = CoprClient.create_from_file_config()

# Initialize CoprUtil with the official COPR client
util = CoprUtil(client)

projectID = util.getProjectID(name=repo, group=group)

if not projectID:
    print('ERROR: project not found') 
    sys.exit(2)

deleteBuildIDs = util.findBuildIDs(projectID=projectID, minAge=7)

for deleteBuildID in deleteBuildIDs:
    response = util.deleteBuild(buildID=deleteBuildID)
    print("Build ID:", deleteBuildID, response)      
    