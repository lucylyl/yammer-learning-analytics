#!/usr/bin/env python
import oauth2 as oauth
import urllib, cgi
import getopt
import sys

def fetch_yammer_msg():

	# create the OAuth consumer credentials
	consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
	client = oauth.Client(consumer)

	# Behind the scenes you request a REQUEST_TOKEN and SECRET from yammer by 
	# passing your CONSUMER_KEY (application key) to 
	# https://www.yammer.com/oauth/request_token. 

	response, content = client.request('https://www.yammer.com/oauth/request_token', 'POST', urllib.urlencode({'method': 'get', 'keys': ''}))
	print response, content, "\n"
	parsed_content = dict(cgi.parse_qsl(content))
	request_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])
	 
	print request_token

	# Your application redirects the user to a special oauth authorization
	# url, passing your REQUEST_TOKEN and SECRET. 
	# https://www.yammer.com/oauth/authorize?oauth_token=REQUEST_TOKEN.


	# ask the user to authorize this application
	#print 'Authorize this application at: %s?oauth_token=%s' % (parsed_content['login_url'], parsed_content['oauth_token'])
	oauth_verifier = raw_input('Enter the PIN / OAuth verifier: ').strip()
	# associate the verifier with the request token
	request_token.set_verifier(oauth_verifier)
	 
	# Your application requests a permanent ACCESS_TOKEN and SECRET by passing the 
	# REQUEST_TOKEN you were initially given along with the oauth_verifier to: 
	# https://www.yammer.com/oauth/access_token.

	client = oauth.Client(consumer, request_token)
	response, content = client.request('https://www.yammer.com/oauth/access_token', 'POST')
	parsed_content = dict(cgi.parse_qsl(content))
	access_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])
	 
	# make an authenticated API call
	client = oauth.Client(consumer, access_token)
	response = client.request('https://www.yammer.com/api/v1/messages.json', 'POST', urllib.urlencode({'method': 'currentUser'}))
	print response[1]

def parse_cmd_line():
    # parse command line options
    if (len(sys.argv) < 2):
    	print "Please enter CONSUMER_KEY & CONSUMER_SECRET at command prompt!"
    	sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print "usage: program_name CONSUMER_KEY CONSUMER_SECRET"  
            sys.exit(0)

if __name__ == "__main__":
	parse_cmd_line()
	fetch_yammer_msg()


