import base64
import json
import requests
import os
import ssl
try:
    import httplib  # Python 2
except:
    import http.client as httplib  # Python 3



def _convert_image_to_base64(image_filename):
    with open(image_filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    return encoded_string


def call_vision_api(image_filename, api_keys):

	api_key = api_keys['sighthound']
	
	headers = {"Content-type": "application/json",
           		"X-Access-Token": api_key}
	
	conn = httplib.HTTPSConnection("dev.sighthoundapi.com", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))

	base64_image = _convert_image_to_base64(image_filename)
	
	params = json.dumps({"image": base64_image})

	conn.request("POST", "/v1/detections?type=all&faceOption=landmark,gender", params, headers)
	response = conn.getresponse()
	#result = response.read()	
	#result.raise_for_status()
	#result = str(result)[2:]
	#result = result[:-1]

	return json.load(response)


def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }

    objects = api_result['objects']
    tag_names = []
    tag_scores = []

    for obj in objects:
        tag_names.append(obj['type'])
        tag_scores.append(1)

    output['tags'] = zip(tag_names, tag_scores)

    return output