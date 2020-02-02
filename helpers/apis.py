import requests
import json
import os
#path = "G:/Anaconda_CC/scraping"

username = "eds@dummy.com"
password = "dentintheuniverse"
base_url = "https://iex.dummy.com"


def generate_token():

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'username': username, 'password': password}

    api_token = base_url + "/generate-token"

    r = requests.post(url=api_token, headers=headers, params=params)

    return r.json()


def get_token():

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'username': username, 'password': password}

    api_token = base_url + "/api/get-token"

    r = requests.post(url=api_token, headers=headers, params=params)
    
    return r.json()


def get_client(token):
    headers = {'token': token, 'Content-Type': 'application/x-www-form-urlencoded'}

    api_get = base_url + "/" + "Prism/getClients"

    r = requests.get(url=api_get, headers=headers)
    return r.json()


def get_data(token, which_api, which_func,params):

    headers = {'token': token, 'Content-Type': 'application/x-www-form-urlencoded'}

    api_get = base_url+"/"+which_api+"/"+which_func+"/?"

    r = requests.get(url=api_get, headers=headers, params=params)

    return r.json()


def set_data(token, which_api, which_func, params):

    headers = {'token': token, 'content-type': 'application/json'}

    api_set = base_url + "/" + which_api + "/" + which_func

    r = requests.post(url=api_set, data=json.dumps(params), headers=headers)

    return r.text




#username = "eds@dummy.com"
#password = "dentintheuniverse"
#base_url = "https://iex.dummy.com/api"
#
#
#def get_token():
#    username = "eds@dummy.com"
#    password = "dentintheuniverse"
#    base_url = "https://iex.dummy.com/api"          
#    try:
#        headers = {}
#        params = {"username": username, "password": password}
#        api_token = base_url + "/get-token"
#        r = requests.post(url=api_token, headers=headers, params=params)
#        return r.json()
#    except Exception as e:
#        print("Error in getting token : {a}".format(a=e))
#
#def store_forecast_api(df):
#    try:
#        print("Setting up final dataframe for date>> {a} and region>> {b}".format(\
#              a=df.date.unique()[0] ,b=df.region.unique()[0]))
#        url = "https://iex.dummy.com/api/set-supply-mode"
#        ip=df.to_json(orient='records')
#        d = {'data' : ip}
#        os.chdir(path+"/tokens")
#        if not os.path.exists('token_pdf.json'):
#            new_token = get_token()
#            print('Regenerated Token Again')
#            #file is dumped as json
#            with open('token_pdf.json', 'w') as outfile:
#                json.dump(new_token, outfile)
#                print('Token file dumped')
#        #reading file from dump
#        with open('token_pdf.json', 'r') as outfile:
#            print('reading from json file')
#            content = outfile.read()
#            token = json.loads(content)['access_token']
#
#        header={'token': token}
#        response = requests.post(url=url, data=d, headers=header)
#        print("forecast in Mongo DB stored")
#        os.chdir(path)
#        return response.json()
#    except:
#        print("Error while stroing in DB")
