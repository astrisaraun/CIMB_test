from tools import utility as ut
import time
import os

def before_all(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer ' + os.getenv("TOKEN")
    }
    
    body = {
        "name": "Anaya geraldine",
        "gender": "female",
        "email": "anaya.geraldine@test.com",
        "status": "active"
    }

    request, response = ut.send_request(method='POST', url='https://gorest.co.in/public/v2/users', headers=headers, body=body)

    print(request,response.json())
    context.carry_over_id = response.json()['id']