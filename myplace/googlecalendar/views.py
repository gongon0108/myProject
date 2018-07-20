#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""

from __future__ import print_function
import sys
from oauth2client import client
from googleapiclient import sample_tools
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Calendar
from .form import PostForm
import sys
import datetime


def index(request):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret_5414.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    now = '2018-07-01T01:01:01.000001Z'
    print(now)
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=30, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    cal_list = []
    att = []
    count = 1
    if not events:
        print('No upcoming events found.')
    for event in events:
        print(count)
        #start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start, event['summary'])
        name=event['summary']
        print('title : ', name)
        loc=event['location']
        print('location : ', event['location'])
        dat=event['start'].get('dateTime')
        print('date : ', dat[0:10])
        temp=dat[0:10]

        att=event['attendees'][0]['email']
        res=event['attendees'][0]['responseStatus']

        """
        for i in range(len(event['attendees'])):
            print('number',i+1,'email: ',event['attendees'][i]['email'],' response: ',event['attendees'][i]['responseStatus'])
            att=event['attendees'][i]['email']
            res=event['attendees'][i]['responseStatus']
        """

        #cal_list.append(name)
        print(att)
        print(res)
        calendar = Calendar( date=dat[0:10],title=name,location=loc, attendee=att, response=res)
        cal_list.append(calendar)
        print('\n')
        count+=1
    print(cal_list)
    context = {'Calendar_list':cal_list}
    print('ok')
    """
    print("Create Event")
    event = {
        'summary': 'Gongon\'s party',
        'location': 'Seoul',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2017-02-04T11:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2017-02-04T12:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    
    print ('Event created: %s' % (event.get('htmlLink')))
    """
    return render(request, 'googlecalendar/index.html',context)

def post(request):
    print('post')
    if request.method == "POST":
        print('if')
        form=PostForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            title=form.cleaned_data['title']
            location=form.cleaned_data['location']
            attendee=form.cleaned_data['attendee']
            response=form.cleaned_data['response']
            #cal=form.save(commit=False)
            #cal.generate()
            #return redirect('index')
            print('date : ',date)
            print('title : ',title)
            print('location : ',location)
            print('attendee : ', attendee)
            print('response : ', response)
            print(type(date))

            SCOPES = 'https://www.googleapis.com/auth/calendar'
            store = file.Storage('credentials.json')
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
                creds = tools.run_flow(flow, store)
            service = build('calendar', 'v3', http=creds.authorize(Http()))
            event = {
                'summary': title,
                'location': location,
                'start': {
                    'dateTime': date+'T00:00:00-01:00',
                    'timeZone': 'Asia/Tokyo',
                },
                'end': {
                    'dateTime': date+'T00:00:00-01:00',
                    'timeZone': 'Asia/Tokyo',
                },
                'attendees':[
                    {
                        'email': attendee,
                        'responseStatus': response
                    }
                ]
            }

            event = service.events().insert(calendarId='primary', body=event).execute()

            print ('Event created: %s' % (event.get('htmlLink')))
            return HttpResponse('Request Success !')
    else:
        form = PostForm()
        print(type(form))
        print('else')
    return render(request,'googlecalendar/index.html', {'form':form})