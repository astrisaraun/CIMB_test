from behave import given, when, then, step
import requests
import allure
from tools import utility as ut
import json
import jmespath
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os 


BASE_URL = "https://gorest.co.in/public/v2/users/"
PATH_WITH_ID = "https://gorest.co.in/public/v2/users/{id}"

@when('I request specific user details')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }
    request, response = ut.send_request(method='GET',url=PATH_WITH_ID.format(id=context.carry_over_id), headers=headers)

    print(request)
    print(response.json())

    ut.log_api_in_report(step_name='Get Spesific User',request=request,response=response)

    ut.assert_equal(response.json()['id'],context.carry_over_id)
    ut.assert_equal(response.json()['name'],'Anaya geraldine')
    ut.assert_equal(response.json()['email'],'anaya.geraldine@test.com')
    ut.assert_equal(response.json()['gender'],'female')
    ut.assert_equal(response.json()['status'],'active')

@when('I request specific user details using the incorrect ID')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }
    request, response = ut.send_request(method='GET',url=PATH_WITH_ID.format(id=5))

    ut.log_api_in_report(step_name='Get Spesific User',request=request,response=response)

    ut.assert_equal(response.json()['message'],'Resource not found')

@when('I attempt to create a new user using the invalid token')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer ACCESS-TOKEN'
    }

    body = {
        "name": "Tenali Ramakrishna",
        "gender": "male",
        "email": "tenali.ramakrish@test.com",
        "status": "active"
    }

    request, response = ut.send_request(method='POST',url=BASE_URL,headers=headers,body=body)

    ut.log_api_in_report(step_name='Create new User',request=request,response=response)

    ut.assert_equal(response.json()['message'],'Invalid token')

@when('I attempt to create a new user with that email alredy taken')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }

    body = {
        "name": "Tenali Ramakrishna",
        "gender": "male",
        "email": "phd_chidambaram_tagore@keeling.test",
        "status": "active"
    }

    request, response = ut.send_request(method='POST',url=BASE_URL,headers=headers,body=body)
    

    ut.log_api_in_report(step_name='Create new User',request=request,response=response)

    expression = "[?field=='email'].message | [0]"
    result = jmespath.search(expression, response.json())

    ut.assert_equal(result,'has already been taken')

@when('I attempt to create a new user')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }

    body = {
        "name": "Caterin Amanda",
        "gender": "female",
        "email": "amanda.caterin123@test.com",
        "status": "active"
    }

    request, response = ut.send_request(method='POST', url=BASE_URL, headers=headers, body=body)
    context.carry_over_id = response.json()['id']
    ut.log_api_in_report(step_name='Create New User',request=request,response=response)

    ut.assert_equal(response.json()['id'],context.carry_over_id)
    ut.assert_equal(response.json()['name'],body['name'])
    ut.assert_equal(response.json()['email'],body['email'])
    ut.assert_equal(response.json()['gender'],body['gender'])
    ut.assert_equal(response.json()['status'],body['status'])



@when('I attempt to update specific user details')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }

    body = {
        "name": "Anaya geraldine",
        "gender": "female",
        "email": "anaya.geraldine@test.com",
        "status": "inactive"
    }

    request, response = ut.send_request(method='PATCH',url=PATH_WITH_ID.format(id=context.carry_over_id),headers=headers,body=body)

    ut.log_api_in_report(step_name='Update User',request=request,response=response)
    
    ut.assert_equal(response.json()['name'],body['name'])
    ut.assert_equal(response.json()['email'],body['email'])
    ut.assert_equal(response.json()['gender'],body['gender'])
    ut.assert_equal(response.json()['status'],body['status'])

@when('I attempt to update specific user details using the incorrect ID')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }

    body = {
        "name": "Caterin Amanda",
        "gender": "female",
        "email": "amanda.caterin@test.com",
        "status": "inactive"
    }

    request, response = ut.send_request(method='PATCH',url=PATH_WITH_ID.format(id=5),headers=headers,body=body)

    ut.log_api_in_report(step_name='Update User',request=request,response=response)

    ut.assert_equal(response.json()['message'],'Resource not found')

@when('I attempt to delete specific user')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }
    request, response = ut.send_request(method='DELETE',url=PATH_WITH_ID.format(id=context.carry_over_id),headers=headers)

    ut.log_api_in_report(step_name='Delete Spesific User',request=request,response=response)

    ut.assert_equal(response.status_code,204)


@when('I attempt to delete the user with the incorrect ID')
def get_spesific_user(context):
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer '+ os.getenv("TOKEN")
    }
    request, response = ut.send_request(method='DELETE',url=PATH_WITH_ID.format(id=5),headers=headers)

    ut.log_api_in_report(step_name='Delete Spesific User',request=request,response=response)

    ut.assert_equal(response.json()['message'],'Resource not found')