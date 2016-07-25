#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
#

# import necessary python libraries for running app engine, editing html, targeting file in the OS, logging issues, etc.
import webapp2
import json
import os
import urllib
import logging
import jinja2
# don't know if the next two are needed, but they are listed in comments for now just in case
# import time
# import datetime
# the import below will be necessary if we get to using google account sign in
# from google.appengine.api import users

# Make sure to use relative path for file path calls, that is how this version of the jinja Environment is set up. Also check copied code for 'jinja_env' vs 'jinja_environment'
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    # This handler manages the front page and should be connected to 'frontpage.html'
    def get(self):
        main_template = jinja_env.get_template('templates/frontpage.html')
        self.response.out.write(main_template.render())

class RedditResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests reddit search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/reddit.html')
        self.response.out.write(main_template.render())

class FacebookResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Facebook search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/facebook.html')
        self.response.out.write(main_template.render())

class TwitterResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests twitter search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/twitter.html')
        self.response.out.write(main_template.render())

class GiphyResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Giphy search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/giphy.html')
        self.response.out.write(main_template.render())

class DefaultHandler(webapp2.RequestHandler):
    # This handler should be designed to give the user a page that incourages them to go to the front page ('/') for all cases where the page route is not one of the predefined routes. When we get to it, we should create an HTML template for it instead of just writing onto the page as it is now.
    def get(self):
        self.response.write('<h1>404 NOT FOUND</h2><br><p>Try "/"</p>')

routes = [
    ('/', MainHandler),
    ('/reddit', RedditResultsHandler),
    ('/facebook', FacebookResultsHandler),
    ('/twitter', TwitterResultsHandler),
    ('/giphy', GiphyResultsHandler),
    # The following are reserved URL paths and their potential handlers. Don't know if we will need them yet, but just incase...
    #
    # ('/login', LoginHandler),
    # ('/logout, LogoutHandler'),
    # ('/signup', SignupHandler),
    #
    # DO NOT put anything below default handler, otherwise site requests go haywire
    #
    ('/.*', DefaultHandler),
]

app = webapp2.WSGIApplication(routes, debug=True)
