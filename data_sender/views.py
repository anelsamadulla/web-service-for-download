# data_sender/views.py
# JSOn response that I get
# {'company': 'Altyn', 'created_at': 'Tue, 23 Jan 2024 00:00:00 GMT', 'issued_for': {'fname': 'Anel', 
# 'lname': 'Samadulla', 'patronym': 'Sheralykyzy'}, 
# 'key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkX2F0IjoiMTcwNTk2ODAwMCIsImRldmljZXMiOjMwMCwic2VydmljZXMiOlsxLDIsM10sImV4cGlyZXNfYXQiOjE3MTgxNTA0MDAuMCwiaXNzdWVkX2ZvciI6ImFuZWthIiwiZGV2aWNlX2lkIjoiZGZoczRmZHNoajAwMSJ9.e_AmljE-RtLf0G4sVumVxFNc57Xt58BWWIBCfFUgM6M', 
# 'payment_status': 'Completed', 'status': 200}

import requests
from django.shortcuts import render, redirect
from .forms import DataSenderForm
import json
from django.http import HttpResponse

def send_data_to_flask(data):
    flask_api_url = 'http://192.168.11.44:5000/api/v1/'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(flask_api_url, json=data, headers=headers)
    
     # Check if the content type is JSON
    if 'application/json' in response.headers.get('content-type', ''):
        try:
            return response.json()
        except json.JSONDecodeError:
            # Handle JSON decoding error if needed
            pass

    # If not JSON, return the response content as is
    return response.content

# def download_file(request, jwt_token):
#     # Set the appropriate content type and headers for file download
#     file_content = jwt_token.encode('utf-8')

#     response = HttpResponse(file_content, content_type='application/octet-stream')
#     response['Content-Disposition'] = 'attachment; filename="generated_key"'
#     return response


import json
from django.http import HttpResponse

def download_file(request, response):
    # Check if 'key' is present in the response
    if 'key' in response:
        jwt_token = response['key']

        # Extract other attributes from the response
        company = response.get('company', '')
        created_at = response.get('created_at', '')
        issued_for = response.get('issued_for', '')
        fname = issued_for.get('fname', '')
        lname = issued_for.get('lname', '')
        patronym = issued_for.get('patronym', '')
        payment_status = response.get('payment_status', '')

        # Construct a dictionary with the data you want to include in the JSON response
        response_data = {
            'company': company,
            'created_at': created_at,
            'issued_for': {'fname': fname, 'lname': lname, 'patronym': patronym},
            'jwt_token': jwt_token,
            'payment_status': payment_status
        }

        # Convert the response data to JSON
        json_data = json.dumps(response_data, indent=2)

        # Set the appropriate content type and headers for file download
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="generated_key"'

        return response
    else:
        return HttpResponse("JWT token not found in the response", status=500)


def test(request):
    x = 1
    y = 2
    return HttpResponse("Test")

def data_sender(request):
    if request.method == 'POST':
        form = DataSenderForm(request.POST)
        if form.is_valid():
            services_list = [int(service) for service in form.cleaned_data['services']]
            data = {
                'company': form.cleaned_data['company'],
                'person': {
                    'fname': form.cleaned_data['fname'],
                    'lname': form.cleaned_data['lname'],
                    'patronym': form.cleaned_data['patronym'],
                },
                'payment': {
                    'status': int(form.cleaned_data['status']),
                    'amount': int(form.cleaned_data['amount']),
                    'created_at': form.cleaned_data['created_at'].timestamp(),
                },
                'expires_at': form.cleaned_data['expires_at'].timestamp(),
                'services': services_list,
                'issued_for': form.cleaned_data['issued_for'],
                'device_id': form.cleaned_data['device_id'],
                'devices': int(form.cleaned_data['devices']),
            }

            # print(data['services'])

            # Send data to Flask app
            response = send_data_to_flask(data)

            print(response)
        
            if 'key' in response:
                return download_file(request, response)
            else:
                # Handle the case where 'key' is not in the response
                return HttpResponse("Key not found in the response", status=500)

    else:
        form = DataSenderForm()

    return render(request, 'data_sender/user_data_info.html', {'form': form})
