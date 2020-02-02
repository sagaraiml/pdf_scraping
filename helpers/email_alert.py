# -*- coding: utf-8 -*-
import requests
import json

class JsonEncoder(json.JSONEncoder):
    def JsonEncoder(self, obj):
        return json.JSONEncoder.default(self, obj)
    
def send_notification(to, subject, body):

    email_alert_url = "https://apis.dummy.com/api/send-notification"

    headers = {'Content-Type': 'application/json'}

    obj = dict()
    obj['from'] = "errorbot@dummy.com"

    obj['to'] = to
    obj['subject'] = subject
    obj['body'] = body
    obj['channel_type'] = 'email'

    params = json.dumps(obj, cls=JsonEncoder)

    r = requests.post(url=email_alert_url, data=params, headers=headers)
    return r.json()

#def send_notification(to, subject, body):
#    data = dict()
#    data['to'] = to
#    data['subject'] = subject
#    data['body'] = body
#    data['channel_type'] = 'email'
#    jsdata = json.dumps(data)
#    respo = requests.post(url = "https://apis.dummy.com/api/send-notification",
#            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}, data= jsdata)
#    return respo