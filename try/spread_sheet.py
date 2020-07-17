import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests
from urllib.parse import urlencode

print("Done Importing")
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_cred.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Tech Test").sheet1
api_key = "4e729c19-df8f-4f97-825d-2308b611075e"
endpoint = f'https://api.hubapi.com/contacts/v1/contact/?hapikey={api_key}'
headers = {"Content-Type": "application/json"}

data = sheet.get_all_records()

max_results = 500


# hapikey = '4e729c19-df8f-4f97-825d-2308b611075e'
# contact_list = []
# property_list = []
# get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
# parameter_dict = {'hapikey': hapikey, "property": "lastmodified"}
# headers = {}
#
# # Paginate your request using offset
# has_more = True
# while has_more:
#     parameters = urlencode(parameter_dict)
#     get_url = get_all_contacts_url + parameters
#     r = requests.get(url=get_url, headers=headers)
#     response_dict = json.loads(r.text)
#     for i in range(len(response_dict["contacts"])):
#         print(response_dict["contacts"][i]["properties"])
#     has_more = response_dict['has-more']

def get_others(other, dict):
    get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
    # parameter_dict = {'hapikey': '4e729c19-df8f-4f97-825d-2308b611075e'}
    headers = {}
    has_more = True
    parameter_dict = {'hapikey': '4e729c19-df8f-4f97-825d-2308b611075e', "property": f"{other}"}
    others = []
    while has_more:
        parameters = urlencode(parameter_dict)
        get_url = get_all_contacts_url + parameters
        r = requests.get(url=get_url, headers=headers)
        response_dict = json.loads(r.text)
        for i in range(len(response_dict["contacts"])):
            # print(response_dict["contacts"][i]["properties"])
            other_col = response_dict["contacts"][i]["properties"][f"{other}"]["value"]
            others.append(other_col)

            dict.update({f"{other}": others})
        has_more = response_dict['has-more']
    return dict


vals = ["email", "country", "industry", "jobtitle", "founded", "kind", "size", "tag", "website", "job_title_full", "email_reliability_status"]
l = {}
for t in vals:
    d = get_others(t, l)
    print(d)

# print("You've succesfully parsed through {} contact records and added them to a list".format(list_length))
