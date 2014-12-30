import facebook
import urllib
import urlparse
import subprocess
import warnings

# Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
warnings.filterwarnings('ignore', category=DeprecationWarning)


# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = '1399344420359978'
FACEBOOK_APP_SECRET = '7911f0f14d832d5424f22064c60fd6bb'
FACEBOOK_PROFILE_ID = 'cgada'

oauth_access_token = 'CAAT4skMYDyoBACJI357J6cxDzZBME1ZBhCQgBHNPZCXapCcfZCGWO3CVHgH4ll0ZCT1A6Q3MOj8hoRXrGv3U9EASZATKC5pCIM92e2i00EUmF1ovzKwjdPtYOy8WEFxuN3lrLWdKFOF8awm9suXnOP0fuOlT5Si7OkinJvt8nWZBpGMtXUpu0GbWzzZCvNXWKKnWBBFzMQZBTsgA6rjrPaaE0'

# Trying to get an access token. Very awkward.
oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')
oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
# oauth_response = subprocess.Popen(oauth_curl_cmd,
 #                                 stdout = subprocess.PIPE,
  #                                stderr = subprocess.PIPE).communicate()[0]

#try:
   # oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
#except KeyError:
 #   print('Unable to grab an access token!')
  #  exit()

facebook_graph = facebook.GraphAPI(oauth_access_token)
profile = facebook_graph.get_object(id='me')
friends = facebook_graph.get_connections(id='me', connection_name='taggable_friends')

friend_list = [(friend['name'], friend['phone_number') for friend in friends['data']]

print friend_list
