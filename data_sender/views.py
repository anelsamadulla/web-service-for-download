# data_sender/views.py
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

def download_file(request, jwt_token):
    # Set the appropriate content type and headers for file download
    file_content = jwt_token.encode('utf-8')
    response = HttpResponse(file_content, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="generated_key.txt"'
    return response

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
                    'status': form.cleaned_data['status'],
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
                jwt_token = response['key']
                return download_file(request, jwt_token)
            else:
                # Handle the case where 'key' is not in the response
                return HttpResponse("Key not found in the response", status=500)
    else:
        form = DataSenderForm()

    return render(request, 'data_sender/user_data_info.html', {'form': form})
