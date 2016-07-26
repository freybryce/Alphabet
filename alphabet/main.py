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
        # variables = {
        #     'search_term': self.request.get("search-input")
        # }
        variables = self.fetch_results(self.request.get("search-input"))
        self.response.write(main_template.render(variables))
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/reddit.html')
        variables = {
            'search_term': self.request.get("search-input")
        }
        self.response.out.write(main_template.render(variables))
    def fetch_results(self, search_term):
        """Use the Reddit API to fetch several posts."""
        logging.info("===== %s.get()" % self.__class__.__name__)

        base_url = 'https://reddit.com/'
        # other_params = '&api_key={key}&limit={num}'.format(key=GIPHY_API_KEY, num=10)
        search_terms = 'search.json?q={term}'.format(term=search_term)
        fullurl = base_url + search_terms
        logging.info("Fetching: %s" % fullurl)

        data_source = urlfetch.fetch(fullurl)

        results = json.loads(data_source.content)
        # Weird issue with href that causes the embeding to load slowly, might have to do with an unnecessary attribute on the the url given to us by the JSON
        post_href = base_url + results['data']['children'][0]['data']['permalink'] + "&ref=share&ref_source=embed"
        subreddit_href = base_url + '/r/' + results['data']['children'][0]['data']['subreddit']
        posts = {
            'timestamp': results['data']['children'][0]['data']['created'],
            'post_href': post_href,
            'title': results['data']['children'][0]['data']['title'],
            'subreddit_href': subreddit_href,
            'subreddit_name': results['data']['children'][0]['data']['subreddit'],
        }
        return posts
        # gifs = []
        # #   for i in results['data']:
        # #       gifs.append(results['data'][i]['images']['original']['url'])
        # gifs = [
        # results['data'][0]['images']['original']['url'],
        # results['data'][1]['images']['original']['url'],
        # results['data'][2]['images']['original']['url'],
        # results['data'][3]['images']['original']['url'],
        # ]
        # return gifs

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

#COPY AND PASTE GIPHY HANDLER HERE IF EVERYTHING BURNS DOWN
class GiphyResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Giphy search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        template = jinja_env.get_template('templates/giphy.html')
        #renders search input from HTML file
        search_term = self.request.get('search_input')
        embed_urls = self.fetch_embed_urls(search_term)
        variables = {
            'search_term': search_term,
            'giphy_embed_url': embed_urls,
        }

        self.response.write(template.render(variables))

#Finds the embed URL needed to display the embed URLs
    def fetch_embed_urls(self, search_term):
        logging.info("===== %s.get()" % self.__class__.__name__)
        data_source = urlfetch.fetch(self.giphy_search(search_term))
        results = json.loads(data_source.content)
        #Creates and array of URL of embed URLs for each item of the results
        embed_urls = []
        for gif_entry in results['data']:
            embed_urls.append(gif_entry['embed_url'])
        return embed_urls

    def giphy_search(self, search_term):
        logging.info("===== %s.get()" % self.__class__.__name__)
        #
        giphy_API_key = 'dc6zaTOxFJmzC'
        base_url = 'http://api.giphy.com/v1/gifs/search?'

     # Do we want to implement the post method? Or only the get method with URL arguments?
    #def post(self):
    #    main_template = jinja_env.get_template('templates/giphy.html')
    #    self.response.out.write(main_template.render())

    #Searches through the Giphy URL after entering a search_term
    def giphy_search(self, search_term):
        logging.info("===== %s.get()" % self.__class__.__name__)
        #
        giphy_API_key = 'dc6zaTOxFJmzC'
        base_url = 'http://api.giphy.com/v1/gifs/search?'
        url_params = {
            'q': search_term,
            'api_key': 'dc6zaTOxFJmzC',
            'limit': 5,
        }
        full_url = base_url + urllib.urlencode(url_params)
        return full_url

class DefaultHandler(webapp2.RequestHandler):
    # This handler should be designed to give the user a page that encourages them to go to the front page ('/') for all cases where the page route is not one of the predefined routes. When we get to it, we should create an HTML template for it instead of just writing onto the page as it is now.
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
