
import allure
import httpx
import copy
import json

def send_request(method='GET', url='', params=None, headers=None, body=None):
    request = httpx.Request(method, url, params=params, headers=headers, json=body)
    response = httpx.Client().send(request)
    return request, response


def parse_json_to_report(request=None, response=None):
    # can only use for request or response cant both
    if request:
        body = str(request.content.decode('ascii'))
        header_dict = {}
        for key in request.headers.keys():
            header_dict[key] = copy.copy(request.headers[key])

        if body:
            # to check if body is eligible to converted to dict
            try:
                body = json.loads(body)
                content = json.dumps({
                    "url": request.url,
                    "header": header_dict,
                    "body": body
                }, indent=4, sort_keys=False, default=str)

            except:
                content = json.dumps({
                    "url": request.url,
                    "header": header_dict,
                    "body": 'replace'
                }, indent=4, sort_keys=False, default=str)
                content = str(content).replace(
                    "replace", '\n' + body.replace("\"", "'"))

        else:
            content = json.dumps({
                "url": request.url,
                "header": header_dict,
                "body": ""
            }, indent=4, sort_keys=False, default=str)
        return content

    if response:
        header_dict = {}
        for key in response.headers.keys():
            header_dict[key] = copy.copy(response.headers[key])
        body = str(response.text)

        if body:
            # to check if body is eligible to converted to dict
            try:
                body = json.loads(body)
                content = json.dumps({
                    "status code": response.status_code,
                    "header": header_dict,
                    "body": body
                }, indent=4, sort_keys=False, default=str)

            except:
                content = json.dumps({
                    "status code": response.status_code,
                    "header": header_dict,
                    "body": 'replace'
                }, indent=4, sort_keys=False, default=str)
                content = str(content).replace(
                    "replace", '\n' + body.replace("\"", "'"))

        else:
            content = json.dumps({
                "status code": response.status_code,
                "header": header_dict,
                "body": ""
            }, indent=4, sort_keys=False, default=str)
        return content

def log_api_in_report(step_name: str, request='', response=''):
    @allure.step(step_name)
    def default_request():
        # request part
        content = parse_json_to_report(request=request)
        allure.attach(content, 'api request : ' + step_name +
                      '.json', allure.attachment_type.JSON)

        # response part
        content = parse_json_to_report(response=response)
        allure.attach(content, 'api response : ' + step_name +
                      '.json', allure.attachment_type.JSON)
    default_request()

def log_single_response_in_report(step_name: str, response: any, type=None):
    @allure.step(step_name)
    def log_single():
        # default None for full response like def log_api_in_report
        if type == None:
            content = parse_json_to_report(response=response)
            allure.attach(content, 'response : ' + step_name +
                          '.json', allure.attachment_type.JSON)

        # for simple json, not from api response
        if type == 'JSON':
            try:
                content = json.dumps(json.loads(response),
                                     indent=4, sort_keys=False, default=str)
            except:
                content = json.dumps(response, indent=4,
                                     sort_keys=False, default=str)

            allure.attach(content, 'response : ' + step_name +
                          '.json', allure.attachment_type.JSON)

        # for text str
        if type == 'TEXT':
            allure.attach(str(response), 'response : ' +
                          step_name + '.txt', allure.attachment_type.TEXT)
    log_single()

# general assertion
def assert_equal(actual, expected):
    result = actual == expected
    message = f"The actual value: {actual} is {'equal' if result else 'not equal'} with expected value: {expected}"
    log_single_response_in_report(
        step_name=message, response=message, type='TEXT')
    assert result, message