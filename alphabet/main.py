#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
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
import unicodedata
from google.appengine.api import urlfetch
# from apiclient.discovery import build
# from optparse import OptionParser
# don't know if the next two are needed, but they are listed in comments for now just in case
# import time
# import datetime
# the import below will be necessary if we get to using google account sign in
# from google.appengine.api import users

# Make sure to use relative path for file path calls, that is how this version of the jinja Environment is set up. Also check copied code for 'jinja_env' vs 'jinja_environment'
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

youtube_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEVELOPER_KEY = "AIzaSyCtZRkKChHBPT-mwRj1hgPwK23F9IdkZuQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class MainHandler(webapp2.RequestHandler):
    # This handler manages the front page and should be connected to 'frontpage.html'
    def get(self):
        main_template = jinja_env.get_template('templates/frontpage.html')
        self.response.out.write(main_template.render())

class RedditResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests reddit search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/reddit.html')
        # This calls the fetch_results function with the search_input variable as an argument, it returns the variables necessary to build the reddit embeded posts
        # variables = {
        #     "posts":  self.fetch_results(self.request.get("search_input")),
        # }
        # logging.info("The variables variable is passing in: " + str(variables))
        variables = self.fetch_results(self.request.get("search_input"))
        self.response.out.write(main_template.render(variables))
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/reddit.html')
        variables = {
            'search_term': self.request.get("search_input")
        }
        self.response.out.write(main_template.render(variables))
    def fetch_results(self, search_term):
        # This function uses the Reddit API to fetch several posts for the get/post function to just call
        #
        logging.info("===== %s.get()" % self.__class__.__name__)
        # This base_url is used as a variable for building essential URLs
        base_url = 'https://reddit.com'
        # The following lines build the url that is used to retrieve the search results JSON file and then loads the JSON file so it can be read and variables can be taken from it
        logging.info("This is our " + str(search_term))
        search_terms = 'search.json?q={term}'.format(term=search_term)
        fullurl = base_url + '/' + search_terms
        logging.info("Fetching: %s" % fullurl)
        data_source = urlfetch.fetch(fullurl)
        results = json.loads(data_source.content)
        # logging.info("results= " + str(results))
        #
        # Weird issue with href that causes the embeding to load slowly, might have to do with an unnecessary attribute on the the url given to us by the JSON
        # posts = []
        # for i in range(0,11):
        #     post_href = base_url + results['data']['children'][i]['data']['permalink'] + "&ref=share&ref_source=embed"
        #     #
        #     subreddit_href = base_url + '/r/' + results['data']['children'][i]['data']['subreddit']
        #     #
        #     post = {
        #         'timestamp': results['data']['children'][i]['data']['created'],
        #         'post_href': post_href,
        #         'title': results['data']['children'][i]['data']['title'],
        #         'subreddit_href': subreddit_href,
        #         'subreddit_name': results['data']['children'][i]['data']['subreddit'],
        #     }
        #     posts.append(post)
        #     logging.info("Post being appended" + str(post) + '\n')
        # # logging.info("Here is the posts dictionary we have built: {post}".format(post=posts))
        # return posts

        post_href = base_url + results['data']['children'][0]['data']['permalink'] + "&ref=share&ref_source=embed"
        subreddit_href = base_url + '/r/' + results['data']['children'][0]['data']['subreddit']
        posts = {
            'timestamp': results['data']['children'][0]['data']['created'],
            'post_href': post_href,
            'title': results['data']['children'][0]['data']['title'],
            'subreddit_href': subreddit_href,
            'subreddit_name': results['data']['children'][0]['data']['subreddit'],
            'search_term': search_term,
        }
        return posts

#{% for post in posts['posts'] %}
#{% endfor %}

class FacebookResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Facebook search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/facebook.html')
        self.response.out.write(main_template.render())
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/facebook.html')
        self.response.out.write(main_template.render())

class TwitterResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests twitter search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/twitter.html')
        self.response.out.write(main_template.render())
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/twitter.html')
        self.response.out.write(main_template.render())

class GiphyResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Giphy search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/giphy.html')
        self.response.out.write(main_template.render())
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/giphy.html')
        self.response.out.write(main_template.render())

class DefaultHandler(webapp2.RequestHandler):
    # This handler should be designed to give the user a page that incourages them to go to the front page ('/') for all cases where the page route is not one of the predefined routes. When we get to it, we should create an HTML template for it instead of just writing onto the page as it is now.
    def get(self):
        self.response.write('<h1>404 NOT FOUND</h2><br><p>Try "/"</p>')

class YouTubeResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Facebook search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
         if DEVELOPER_KEY == "REPLACE_ME":
           self.response.write("You must set up a project and get an API key to run this project.  Please visit <landing page> to do so.")
         else:
           youtube = build(
             YOUTUBE_API_SERVICE_NAME,
             YOUTUBE_API_VERSION,
             developerKey=DEVELOPER_KEY)
           search_response = youtube.search().list(
             q="Hello",
             part="id,snippet",
             maxResults=5
           ).execute()

           videos = []
           channels = []
           playlists = []

           for search_result in search_response.get("items", []):
             if search_result["id"]["kind"] == "youtube#video":
                 videos.append("%s (%s)" % (search_result["snippet"]["title"],
                   search_result["id"]["videoId"]))
             elif search_result["id"]["kind"] == "youtube#channel":
                 channels.append("%s (%s)" % (search_result["snippet"]["title"],
                   search_result["id"]["channelId"]))
             elif search_result["id"]["kind"] == "youtube#playlist":
                 playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                   search_result["id"]["playlistId"]))

           template_values = {
            'videos': videos,
            'channels': channels,
            'playlists': playlists
           }

           self.response.headers['Content-type'] = 'text/plain'
           template = youtube_jinja_env.get_template('templates/youtube.html')
           self.response.write(template.render(template_values))





routes = [
    ('/', MainHandler),
    ('/reddit', RedditResultsHandler),
    ('/facebook', FacebookResultsHandler),
    ('/twitter', TwitterResultsHandler),
    ('/giphy', GiphyResultsHandler),
    ('/youtube', YouTubeResultsHandler),
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
