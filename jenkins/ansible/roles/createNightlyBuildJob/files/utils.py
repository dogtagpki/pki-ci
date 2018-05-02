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

import requests
from requests.auth import HTTPBasicAuth
import datetime


class CoprUtil:

    DELETE_RESULT = {
            204: "was removed successfully",
            400: "can't be deleted currently",
            403: "authroization failed",
            404: "doesn't exists"
    }

    def __init__(self, client=None):
        """
            :param unicode repo: COPR repo to work on
            :param unicode copr_url: COPR URL to access end points
        """
        self.client = client
        self.copr_api_url = client.api_root or u"https://copr.fedorainfracloud.org/api_2"
        self.netClient = client.nc

    def sendGetRequest(self, url, params):
        """
            :param unicode url: request URL
            :param json params: params to embed in the GET request
        """
        # Send GET request
        response = requests.get(url = url, params = params)

        # Extract data in JSON format
        return response.json()

    def getProjectID(self, name=None, group='pki'):
        """
            :param unicode searchQuery: search parameter similar to search box in COPR site
            :param unicode name: repository name to search for
            :param unicode group: group name of the project
        """
        # Construct URL for project endpoint
        url = "{0}/projects".format(self.copr_api_url)

        # Define params to be sent to the End Point
        if name and group:
            PARAMS = {'group': group, 'name': name}
        else:
            return None

        receivedData = self.sendGetRequest(url=url, params=PARAMS)

        projects = receivedData['projects']
        if(len(projects) != 1):
            raise ValueError("Provide project specific details to get Project ID")
        else:
            # Found exact project. Extract project ID
            project = projects[0]['project']
            return project['id']

    def findBuildIDs(self, projectID=None, package=None, minAge=None):
        """
            :param integer projectID: project ID
            :param unicode package: package name 
            :param integer days: no of latest days to filter out
        """
        # Construct URL for builds End point
        url = "{0}/builds".format(self.copr_api_url)

        if not projectID or not package or not minAge:
            raise ValueError('projectID, package and days are required') 
        
        PARAMS = {'project_id': projectID}

        # Send GET request
        receivedData = self.sendGetRequest(url=url, params=PARAMS) 
        

        # Extract build IDs
        buildIDs = []

        # Get current time
        currTimeStamp = datetime.datetime.now()

        for buildData in receivedData['builds']:
            build = buildData['build']
            timeStamp = datetime.datetime.fromtimestamp(build['submitted_on'])
            if(currTimeStamp - timeStamp >= datetime.timedelta(days=minAge) and
                build['package_name'] == package):
                buildIDs.append(build['id'])

        return buildIDs

    def deleteBuild(self, buildID=None):
        """
            :param integer buildID: build ID
            :param unicode login: COPR login parsed from ~/.config/copr
            :param unicode token: COPR token parsed from ~/.config/copr
        """
        if buildID is None:
            raise ValueError("Build ID is required")
        
        if type(buildID) is list:
            raise ValueError("Single build ID is required")

        # Construct URL for delete build End point
        url = "{0}/builds/{1}".format(self.copr_api_url, buildID)
        headers = {'content-type': 'application/json'}

        # Embed Basic Auth in the DELETE request
        response = requests.delete(url=url, headers=headers, auth=HTTPBasicAuth(self.netClient.login, self.netClient.token))

        return self.DELETE_RESULT[response.status_code]
