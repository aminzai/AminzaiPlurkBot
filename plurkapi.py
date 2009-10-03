"""
    plurkapi.py
    Copyright 2008 David Blume <david.blume@gmail.com>
    Portions Copyright 2008 Ryan Lim <plurk-api@ryanlim.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

2008-07-12 : Original, based on RLPlurkAPI.php, by Ryan Lim

"""

import time
import urllib
import urllib2
import cookielib
import simplejson # http://www.undefined.org/python/
import re

class PlurkError(Exception): pass

def permalinkToPlurkID(permalink):
    base36number = permalink[len('http://www.plurk.com/p/'):]
    return int(base36number, 36)

def _baseN(num,b):
    return ((num == 0) and  "0" ) or ( _baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def PlurkIDToPermalink(plurk_id):
    return 'http://www.plurk.com/p/' + _baseN(int(plurk_id), 36)

class PlurkAPI:
    
    def __init__(self):
        self._logged_in = False
        self._uid = -1
        self._nickname = None
        self._friends = {}
        self._cookies = cookielib.CookieJar()
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookies))
        urllib2.install_opener(self._opener)

    def login(self, nickname, password):
        """ login to plurk and keep a session cookie """
        post = urllib.urlencode({'nick_name': nickname, 'password': password})
        request = urllib2.Request( self._plurk_paths['login'], post) 
        response = urllib2.urlopen( request )
        self._cookies.extract_cookies( response, request )
        for cookie in self._cookies:
            if cookie.name.startswith('plurkcookie'):
                self._logged_in = True
                break
        if self._logged_in == True:
            response = urllib2.urlopen('http://www.plurk.com/%s' % (nickname) )
            page = response.read()
            uid_pat = re.compile('var GLOBAL = \{.*"uid": ([\d]+),.*\}')
            matches = uid_pat.findall(page)
            if len(matches):
                self._uid = matches[0]
            else:
                raise PlurkError, "Could not find user_id."
            self._nickname = nickname;
            post = urllib.urlencode({ 'user_id': self._uid })
            response = urllib2.urlopen(self._plurk_paths['getCompletion'], post )
            self._friends = simplejson.load(response)
        return self._logged_in

    def addPlurk(self, lang='en', qualifier='says', content='', allow_comments=True, limited_to=[]):
        """ Add a plurk to your timeline.  (Must be logged in.) """
        if self._logged_in == False:
            return False

        if allow_comments == True:
            no_comments = '0'
        else:
            no_comments = '1'

        params = {'posted': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
                  'qualifier': qualifier,
                  'content': content,
                  'lang': lang,
                  'uid': self._uid,
                  'no_comments': no_comments }

        if len(limited_to):
            params['limited_to'] = '[%s]' % ','.join(limited_to)

        post = urllib.urlencode(params)
        response = urllib2.urlopen( self._plurk_paths['plurk_add'], post) 
        page = response.read()
        if page.find('anti-flood') != -1:
            raise PlurkError, 'Anti-flood rules prohibited the plurk.'
        matches = re.compile('"error":\s(\S+)}').findall(page)
        if len(matches) and matches[0] != 'null':
            raise PlurkError, matches[0]
        
        return True
            
    def getPlurks(self, uid = None, date_from = None, only_responded = False):
        """ If logged in, gets yours and your friends' plurks.
            If not logged in, gets only the plurks for the specified user id.
            date_from should be of the form 2008-9-5T19:07:29 """
        if uid == None:
            uid = self._uid

        params = { 'user_id': uid, }
        if date_from != None:
            params['offset'] = date_from
        if only_responded != False:
            params['only_responded'] = 1
        post = urllib.urlencode(params)
        response = urllib2.urlopen(self._plurk_paths['plurk_get'], post )
        page = response.read()
        # The following two lines are a hack around the fact that
        # simplejson doesn't create Date objects.
        date_pat = re.compile('\"posted\": new Date\((\".+?\")\)')
        data = simplejson.loads(re.sub(date_pat, '"posted": \g<1>', page))
        return data

    def getPlurksById(self, ids = []):
        """ Gets individual plurks by their ids. """

        params = { 'ids': '[%s]' % (','.join([str(id) for id in ids]), ), }
        post = urllib.urlencode(params)
        response = urllib2.urlopen(self._plurk_paths['plurk_get_by_id'], post )
        page = response.read()
        # The following two lines are a hack around the fact that
        # simplejson doesn't create Date objects.
        date_pat = re.compile('\"posted\": new Date\((\".+?\")\)')
        data = simplejson.loads(re.sub(date_pat, '"posted": \g<1>', page))
        return data

    def getPlurkResponses(self, plurk_id):
        """ Gets individual plurks by their ids. """

        post = urllib.urlencode({ 'plurk_id': plurk_id })
        response = urllib2.urlopen(self._plurk_paths['plurk_get_responses'], post )
        page = response.read()
        # The following two lines are a hack around the fact that
        # simplejson doesn't create Date objects.
        date_pat = re.compile('\"posted\": new Date\((\".+?\")\)')
        data = simplejson.loads(re.sub(date_pat, '"posted": \g<1>', page))
        return data
    
    def respondToPlurk(self, plurk_id, lang='en', qualifier='says', content=''):
        """ Respond to the specified plurk. """
        if self._logged_in == False or len(content) > 140:
            return False
        params = {'posted': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
                  'qualifier': qualifier,
                  'content': content,
                  'lang': lang,
                  'p_uid': self._uid,
                  'uid': self._uid,
                  'plurk_id': plurk_id }
        post = urllib.urlencode(params)
        response = urllib2.urlopen( self._plurk_paths['plurk_respond'], post) 
        return response.read()

    def getAlerts(self):
        """ Parse any pending Alerts and returns a list of user ids requesting friendship. """
        if self._logged_in == False:
            return False
        response = urllib2.urlopen( self._plurk_paths['notification'] ) 
        page = response.read()
        notification_pat = re.compile('DI\s*\(\s*Notifications\.render\(\s*(\d+),\s*0\)\s*\);')
        matches = notification_pat.findall(page)
        return matches

    def befriend(self, uids, befriend=True):
        """ Accept or deny friendship requests. """
        if self._logged_in == False:
            return False

        string_path_accept_deny = self._plurk_paths['notification_accept']
        if not befriend:
            string_path_accept_deny = self._plurk_paths['notification_deny']

        for uid in uids:
            post = urllib.urlencode({ 'friend_id': uid, })
            response = urllib2.urlopen( string_path_accept_deny, post )
        return True

    def uidToUserinfo(self, uid):
        """ Returns a dict of available user info for the given uid.
            TODO: Make the dict be a class?  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308 """
        post = urllib.urlencode({ 'user_id': uid })
        response = urllib2.urlopen(self._plurk_paths['user_get_info'], post )
        page = response.read()
 
        # The following two lines are a hack around the fact that
        # simplejson doesn't create Date objects.
        date_pat = re.compile(': new Date\((\".+?\")\)')
        return simplejson.loads(re.sub(date_pat, ': \g<1>', page))

    def removeFriend(self, uid):
        """ Removes the user with the specified uid as a friend """
        if self._logged_in == False:
            return False
        post = urllib.urlencode({ 'friend_id': uid })
        response = urllib2.urlopen(self._plurk_paths['remove_friend'], post )
        return response.read()

    def uidToNickname(self, uid):
        """ Returns the nickname for the user with the given user id. """
        uid = str(uid)
        if uid == self._uid:
            return self._nickname
        if self._friends.has_key(uid):
            return self._friends[uid]['nick_name']
        else:
            return 'User %s' % uid

    uid = property(lambda self: self._uid)
    logged_in = property(lambda self: self._logged_in)
    nickname = property(lambda self: self._nickname)
    friends = property(lambda self: self._friends)

    _plurk_paths = {
        'http_base'             : 'http://www.plurk.com',
        'login'                 : 'http://www.plurk.com/Users/login',
        'getCompletion'         : 'http://www.plurk.com/Users/getCompletion',
        'plurk_add'             : 'http://www.plurk.com/TimeLine/addPlurk',
        'plurk_respond'         : 'http://www.plurk.com/Responses/add',
        'plurk_get'             : 'http://www.plurk.com/TimeLine/getPlurks',
        'plurk_get_by_id'       : 'http://www.plurk.com/TimeLine/getPlurksById',
        'plurk_get_responses'   : 'http://www.plurk.com/Responses/get2',
        'plurk_get_unread'      : 'http://www.plurk.com/TimeLine/getUnreadPlurks',
        'plurk_mute'            : 'http://www.plurk.com/TimeLine/setMutePlurk',
        'plurk_delete'          : 'http://www.plurk.com/TimeLine/deletePlurk',
        'notification'          : 'http://www.plurk.com/Notifications',
        'notification_accept'   : 'http://www.plurk.com/Notifications/allow',
        'notification_makefan'  : 'http://www.plurk.com/Notifications/allowDontFollow',
        'notification_deny'     : 'http://www.plurk.com/Notifications/deny',
        'friends_get'           : 'http://www.plurk.com/Users/friends_get',
        'friends_block'         : 'http://www.plurk.com/Friends/blockUser',
        'friends_remove_block'  : 'http://www.plurk.com/Friends/removeBlock',
        'friends_get_blocked'   : 'http://www.plurk.com/Friends/getBlockedByOffset',
        'user_get_info'         : 'http://www.plurk.com/Users/fetchUserInfo',
        'remove_friend'         : 'http://www.plurk.com/Users/removeFriend'
    }

    _qualifiers = { 'en': (':', 'loves',  'likes', 'shares', 'gives', 'hates', 'wants', 'wishes',
                             'needs', 'will', 'hopes', 'asks', 'has', 'was', 'wonders', 'feels', 'thinks', 'says', 'is')
                  }
                  

