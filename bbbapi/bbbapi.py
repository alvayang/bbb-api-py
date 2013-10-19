#!/bin/env python
#-*- coding:utf-8 -*-


# /**
# * @file   bbb-api-py.py
# * @author alvayang <netyang@gmail.com>
# * @date   Sat Oct  19 20:23:21 2013
# * 
# * @brief  Python Wrapper for BigBlueButton
# *         Few Basic Functions
# * 
# * 
# */

'''
#How to Use it

    BBBSALT = '7ae35909bf35d55ccaeeexe058141c8d'
    BBBBASE = u'http://v.1in1.cn/bigbluebutton/api/'
    s = BBB_API(BBBSALT, BBBAPI)
    print s.start_room('测试', 1, '123', '345', 'Welcome', '', 0, 0, 60, '')
    print s.join_room(1, '杨松', 1, '345')
'''

import hashlib
import urllib, urllib2
import xml.etree.ElementTree as ET

class BBB_API:
    def __init__(self, salt, api_url, timeout = 3, debug = 0):
        self._salt = salt
        self._apiurl = api_url
        self._debug = debug
        self._timeout = timeout
        self._ppt_extra = ''
        pass

    def generate_api_checksum(self, parameters, cmd):
        _salt = cmd + parameters + self._salt
        return hashlib.new('sha1', _salt).hexdigest()

    def make_bbb_get_request(self, params, cmd, data =  ''):
        url_values = urllib.urlencode(params)
        _sum = self.generate_api_checksum(url_values, cmd)
        url_values = url_values + "&checksum=" + _sum
        _url = self._apiurl + cmd + "?" + url_values
        handler=urllib2.HTTPHandler(debuglevel = self._debug)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        headers = {
                'Content-Type': 'text/xml'
                }
        try:
            if data:
                req = urllib2.Request(_url, headers = headers)
                response = urllib2.urlopen(req, data, timeout = self._timeout)
            else:
                req = urllib2.Request(_url)
                response = urllib2.urlopen(req, timeout = self._timeout)
            return (''.join(response.readlines()), _url)
        except:
            print traceback.format_exc()
            return ('', '')
        
    def parse_response(self, response):
        try:
            root = ET.fromstring(response)
            return "SUCCESS" == root.find('returncode').text
        except:
            return response.lower().startswith('<!doctype html')


    '''
     add pre-upload files, will be used to create a meeting
    '''
    def add_extra_document(self, pathlist = []):
        if len(pathlist) == 0: return
        self._ppt_extra = "<?xml version='1.0' encoding='UTF-8'?> <modules>  <module name='presentation'>%s</module></modules>" % (''.join(["<document url='%s' />" % str(x) for x in pathlist]))


    '''
       Create A meeting with given parameters.
       the return value is:
       ([True|False], create_url)
    '''
    def start_room(self
            , cls_name = '' # class name
            , meetingid = 0  # meeting id
            , attendeePW = ''  # password for attendee to join the meeting
            , moderatorPW = '' # password for moderator to join the meeting
            , welcome = ''  # welcome message will be displayed in the chat pannel
            , logoutURL = '' # redirect url after logout the meeting
            , maxParticipants = 0  # it's not a useful parameter now, read more[http://code.google.com/p/bigbluebutton/wiki/API#Create_Meeting]
            , record = 0  # record flog, 0 will send the api 'false', 1 for 'true'
            , duration = 120  # the duration of a meeting
            ):
        create_params = {
            'name' : cls_name,
            'meetingID' : meetingid,
            'attendeePW' : attendeePW,
            'moderatorPW' : moderatorPW,
            'welcome' : welcome,
            'logoutURL' : logoutURL,
            'maxParticipants' : maxParticipants, 
            'record' : record,
            'duration' : str(duration).encode('utf-8')
        }
        (info, _url) = self.make_bbb_get_request(create_params, 'create', self._ppt_extra)
        def _parse_result(_info):
            return self.parse_response(info)

        if not _parse_result(info):
            # 第一次请求失败，那么再来一次
            (info, _url) = self.make_bbb_get_request(create_params, 'create', self._ppt_extra)
            if not _parse_result(info):
                # 又失败，返回失败
                return (False, '')
        return (True, _url)


    '''
	join a meeting, the join api from bbb is wired, it will return the html code directly, it's really not friendly to the third-party integration.
        
        in this function, I will return the html code, and a url to join the meeting.

        @parameter: meetingid, meeting id specified when create a meeting
        @parameter: username, a user's name, it will be displayed at the users' pannel
        @parameter: userid, used in bbb, not for us.
        @parameter: moderator_or_attendee_password, this parameter will decide the role of this user, if the password is the moderatorPW specified in create meeting, the user will act as the moderator, otherwise a attendee.

	@return ([True|False], join url, htmlcode)
    '''
    def join_room(self, meetingid, username, userid, moderator_or_attendee_password = ''):
        get_info_param = {
            'password' : moderator_or_attendee_password,
            'meetingID' : meetingid,
            'fullName' : username,
            'userID' : userid
        }
        (_info, _url) = self.make_bbb_get_request(get_info_param, 'join')
        if not self.parse_response(_info):
            return (False, '', None)
        return (True, _url, _info)

    '''
      close a meeting.
      @parameter: meetingid, meeting id specified when create a meeting
      @parameter: moderator_password, moderatorPW specified in create meeting.
    '''
    def close_room(self, meetingid, moderator_password):
        _params = {
            'meetingID' : meetingid,
            'password' : moderator_password 
        }
        (info, _url) = self.make_bbb_get_request(_params, 'end')
        return self.parse_response(info)

