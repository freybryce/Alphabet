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
from apiclient.discovery import build
from optparse import OptionParser
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
        variables = {
            "posts":  self.fetch_results(self.request.get("search_input")),
            "test": "hello",
            'search_term': self.request.get("search_input"),
        }
        # logging.info("The variables variable is passing in: " + str(variables))
        # variables = self.fetch_results(self.request.get("search_input"))
        logging.info('Here is the list being going to HTML {lists}'.format(lists=variables))
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
        posts_list = []
        for post_entry in results['data']['children']:
            post_dict = {}

            post_href = base_url + post_entry['data']['permalink'] + "&ref=share&ref_source=embed"

            post_dict['post_href'] = post_href

            subreddit_href = base_url + '/r/' + post_entry['data']['subreddit']

            post_dict['subreddit_href'] = subreddit_href

            post_dict["timestamp"] = post_entry['data']['created']

            post_dict["title"] = post_entry['data']['title']
            posts_list.append(post_dict)
        # logging.info('Here is the posts_list being returned: {item}'.format(item=posts_list))
        return posts_list

class FacebookResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests Facebook search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/facebook.html')
        self.response.out.write(main_template.render())
        import facebook
        token = 'EAAHQDNvMrgABAJfoObvmQl1QPaPMznPdTOyaY69eAVobHZCqjcEVueQEXoCyo7ZBHryzISRcyjcK5BPlQvZAKxsIVIpASttEmiZCJJtp5GsHVOS9S2W7zZAvyXNVWTtOdsvs4Hr5eipYPDiLiSXx0oQ8ZA15yFxiIY9BDZBfTRx5QZDZD'
        graph = facebook.GraphAPI(access_token=token)
        data = graph.request('/search?q=Clayton&type=user')
        logging.info("Her is the data that Facebook is giving us: {data}".format(data=data))
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/facebook.html')
        self.response.out.write(main_template.render())

class TwitterResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests twitter search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/twitter.html')
        variables = {
            'search_term': self.request.get("search_input"),
            'embed_href': self.href_builder(self.request.get("search_input")),
        }
        self.response.out.write(main_template.render(variables))
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/twitter.html')
        self.response.out.write(main_template.render())
    def href_builder(self, search_term):
        # This function builds a url to be passed into the template for the twitter widget
        base_url = 'https://twitter.com/hashtag/'
        final_url = base_url + search_term
        return final_url

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
            'limit': 25,
        }
        full_url = base_url + urllib.urlencode(url_params)
        return full_url

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
                q=self.request.get("search_input"),
                part="id,snippet",
                maxResults=25
            ).execute()

            # logging.info("Here is the JSON file that YouTube is passing through to us: {JSON}".format(JSON=search_response))

            videos = []
            channels = []
            playlists = []

# <img src="%s"/><br>
# search_result["snippet"]["thumbnails"]["high"]["url"],

            base_url = "https://www.youtube.com/embed/"

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    videos_dict = {}

                    video_id = search_result["id"]["videoId"]
                    embed_url = base_url + video_id
                    videos_dict['embed_url'] = embed_url

                    video_title = search_result["snippet"]["title"]
                    videos_dict['title'] = video_title

                    videos.append(videos_dict)
                elif search_result["id"]["kind"] == "youtube#channel":
                    channels.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["channelId"]))
                elif search_result["id"]["kind"] == "youtube#playlist":
                    playlists.append("%s (%s)" % (search_result["snippet"]["title"],                    search_result["id"]["playlistId"]))

        #    for search_result in search_response.get("items", []):
        #      if search_result["id"]["kind"] == "youtube#video":
        #         videos.append('%s (%s)' % (
        #             search_result["snippet"]["title"],
        #             search_result["id"]["videoId"]
        #             )
        #         )
        #      elif search_result["id"]["kind"] == "youtube#channel":
        #          channels.append("%s (%s)" % (search_result["snippet"]["title"],
        #            search_result["id"]["channelId"]))
        #      elif search_result["id"]["kind"] == "youtube#playlist":
        #          playlists.append("%s (%s)" % (search_result["snippet"]["title"],
        #            search_result["id"]["playlistId"]))

            template_values = {
                'videos': videos,
                'channels': channels,
                'playlists': playlists,
                'search_input': self.request.get("search_input"),
            }
            logging.info("This is the template_values dictionary that is being passed through to the template: {dict}".format(dict=template_values))
        #    for some reason the below line was part of the code YouTube gave me, but it returns the html as plain text
        #    self.response.headers['Content-type'] = 'text/plain'
            template = youtube_jinja_env.get_template('templates/youtube.html')
            self.response.write(template.render(template_values))

class InstagramResultsHandler(webapp2.RequestHandler):
    # This handler is designed to process requests reddit search results. Not sure if we are using the get method, the post method or both yet
    def get(self):
        main_template = jinja_env.get_template('templates/instagram.html')
        # This calls the fetch_results function with the search_input variable as an argument, it returns the variables necessary to build the reddit embeded posts
        # variables = {
        #     "posts":  self.fetch_results(self.request.get("search_input")),
        #     "test": "hello",
        #     'search_term': self.request.get("search_input"),
        # }
        # logging.info("The variables variable is passing in: " + str(variables))
        # variables = self.fetch_results(self.request.get("search_input"))
        # logging.info('Here is the list being going to HTML {lists}'.format(lists=variables))
        self.request.get('code')

        variables = {
            # 'search_term': self.request.get("search_input")
            'token': self.request.get("code")
        }
        self.response.out.write(main_template.render())
    # Do we want to implement the post method? Or only the get method with URL arguments?
    def post(self):
        main_template = jinja_env.get_template('templates/reddit.html')
        variables = {
            # 'search_term': self.request.get("search_input")
            'token': self.request.get("code")
        }
        logging.info(variables)
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
        posts_list = []
        for post_entry in results['data']['children']:
            post_dict = {}

            post_href = base_url + post_entry['data']['permalink'] + "&ref=share&ref_source=embed"

            post_dict['post_href'] = post_href

            subreddit_href = base_url + '/r/' + post_entry['data']['subreddit']

            post_dict['subreddit_href'] = subreddit_href

            post_dict["timestamp"] = post_entry['data']['created']

            post_dict["title"] = post_entry['data']['title']
            posts_list.append(post_dict)
        # logging.info('Here is the posts_list being returned: {item}'.format(item=posts_list))
        return posts_list

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
    ('/youtube', YouTubeResultsHandler),
    ('/instagram', InstagramResultsHandler),
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
