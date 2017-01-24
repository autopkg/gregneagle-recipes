#!/usr/bin/python
#
# Copyright 2016 Greg Neagle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for BluejeansAppURLProvider class"""

import json
import os
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["BluejeansAppURLProvider"]

# this URL was snarfed out of the Blue Jeans Launcher.app that you get
# when you try to download the "Blue Jeans App for Mac"
# from http://bluejeans.com/downloads
# ala:
# https://swdl.bluejeans.com/desktop/mac/launchers/BlueJeansLauncher_live_165.dmg
FEED_URL = 'https://swdl.bluejeans.com/desktop/mac/live.json'
# the feed points to the current installer pkg, which is downloaded and
# installed by the "Launcher.app"
FEED_URL_KEY = 'installer_download_url'
# and the feed_url_key determines which key is fetched to provide the url variable

class BluejeansAppURLProvider(Processor):
    """Provides URL to the latest Bluejeans app package."""
    description = __doc__
    input_variables = {
        "feed_url": {
            "required": False,
            "description": "Default is '%s." % FEED_URL,
        },
        "feed_url_key": {
            "required": False,
            "description": "Default is '%s." % FEED_URL_KEY,
        },
    }
    output_variables = {
        "filename": {
            "description": "Filename portion of the URL.",
        },
        "url": {
            "description": "URL to the latest Bluejeans app package.",
        },
        "version": {
            "description": "version of the pkg, as claimed by the feed"
        },
    }

    def get_feed_from_url(self, feed_url):
        """Get the JSON pkg feed from the feed_url"""
        #pylint: disable=no-self-use
        try:
            # let's hope urllib2 stays up to the task; may need
            # to replace with curl at some point in the future.
            url_handle = urllib2.urlopen(feed_url)
            response = url_handle.read()
            url_handle.close()
        except BaseException as err:
            raise ProcessorError(
                'Can\'t read response from URL %s: %s' % (feed_url, err))
        try:
            response_dict = json.loads(response)
            return response_dict
        except ValueError as err:
            raise ProcessorError(
                'Could not parse json from URL %s: %s' % (feed_url, err))

    def main(self):
        """Provide a Bluejeans app pkg URL and related metadata"""
        # Because PyLint can't import autopkglib, it complains about
        # self.env and self.output
        #pylint: disable=no-member
        feed_url = self.env.get('feed_url', FEED_URL)
        feed_url_key = self.env.get('feed_url_key', FEED_URL_KEY)
        feed = self.get_feed_from_url(feed_url)
        try:
            self.env['url'] = feed[feed_url_key]
            self.output('Found URL %s' % self.env['url'])
        except AttributeError:
            raise ProcessorError(
                'Missing installer_download_url from feed at URL %s' % feed_url)
        # grab last path item from URL as filename
        self.env['filename'] = os.path.split(self.env['url'])[-1]
        self.output('Filename: %s' % self.env['filename'])
        try:
            self.env['version'] = feed['version']
            self.output('Found version number %s' % self.env['version'])
        except AttributeError:
            raise ProcessorError(
                'Missing version from feed at URL %s' % feed_url)

# Because PyLint can't import autopkglib, it complains about
# PROCESSOR.execute_shell
#pylint: disable=no-member
if __name__ == "__main__":
    PROCESSOR = BluejeansAppURLProvider()
    PROCESSOR.execute_shell()
