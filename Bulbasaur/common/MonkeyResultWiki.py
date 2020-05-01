#!/usr/bin/env python
# coding: utf-8

import urllib
import urllib.request as urllib2
import http.cookiejar as cookie_jar
from bs4 import BeautifulSoup
from model.Tester import *
from common.PublicMethod import *


def login_and_post(login_page, request_url, user, password):
    
    try:
        # Set cookie
        cj = cookie_jar.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent',
                              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')]
        urllib2.install_opener(opener)

        # log in
        login_data = {
            "os_username": user,
            "os_password": password,
            "os_cookie": "true",
            "login": "login",
            "os_destination": ""}
        login_data = urllib.urlencode(login_data)
        req = urllib2.Request(login_page, login_data)
        conn = urllib2.urlopen(req)

        # Open the specified page after successful login
        point_url = urllib2.urlopen(request_url).read()
        # print point_url

        soup = BeautifulSoup(
            point_url,  # docstring
            'html.parser',  # parser
            from_encoding='utf-8'  # Document encoding
        )
        token = soup.find_all('meta', id='atlassian-token')
        token_content = token[0].attrs['content']
        print(token_content)  # Get token value

        draft_id = soup.find_all('input', id='draftId')
        draft_id_result = draft_id[0].attrs['value']
        print(draft_id_result)  # get draft id

        entity_id = soup.find_all('input', id='entityId')
        entity_id_result = entity_id[0].attrs['value']
        print(entity_id_result)  # Obtain entityId

        # Read the contents of the Monkey.Summary.txt file
        for listdir in Tester.lis:
            if 'Summary' in listdir:
                file = open(listdir, 'rb')
                file_data = file.read()
                file.close()

        # Submit form data to Android Monkey AutoTest Tracking page
        page_data = {
            "atl_token": "%s" % token_content,
            "fromPageId": "8770164",
            "spaceKey": "ANDROID",
            "labelsString": "",
            "titleWritten": "false",
            "linkCreation": "false",
            "title": "%s" % get_format_current_time(),
            "wysiwygContent": "%s" % file_data,
            "confirm": "Save",
            "parentPageString": "Android Monkey AutoTest Tracking",
            "moveHierarchy": "true",
            "position": "",
            "targetId": "",
            "draftId": "%s" % draft_id_result,
            "entityId": "%s" % entity_id_result,
            "newSpaceKey": "ANDROID"
        }

        post_data = urllib.urlencode(page_data)
        url = 'http://wiki.niceprivate.com/pages/docreatepage.action'
        req2 = urllib2.Request(url=url, data=post_data)
        # View the content returned after submitting the form
        response = urllib2.urlopen(req2)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    loginUrl = 'xxxxxxx'
    user = 'xxxxxx'
    password = 'xxxxxx'
    requestUrl = 'xxxxxxx'

    # Login test
    login_and_post(loginUrl, requestUrl, user, password)
