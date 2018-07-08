import requests
import json

ENDPOINT = 'https://api.imagga.com/v1'

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['imagga']['api_key']
    api_secret = api_keys['imagga']['api_secret']

    with open(image_filename, 'rb') as image_file:
        filename = image_file.name

        # Upload the multipart-encoded image with a POST
        # request to the /content endpoint
        content_response = requests.post(
            '%s/content' % ENDPOINT,
            auth=(api_key, api_secret),
            files={filename: image_file})

        # Example /content response:
        # {'status': 'success',
        #  'uploaded': [{'id': '8aa6e7f083c628407895eb55320ac5ad',
        #                'filename': 'example_image.jpg'}]}
        uploaded_files = content_response.json()['uploaded']

        # Get the content id of the uploaded file
        content_id = uploaded_files[0]['id']


    #image_url = "D:/PBL/cloudy_vision-master/input_images/" + image_filename 

    #response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url,
                        #auth=(api_key, api_secret))

    verbose = False
    language='en'

    tagging_query = {
        'content': content_id,
        'verbose': verbose,
        'language': language
    }
    tagging_response = requests.get(
        '%s/tagging' % ENDPOINT,
        auth=(api_key, api_secret),
        params=tagging_query)


    return json.loads(tagging_response.text)


def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }

    api_result = api_result["results"][0]

    if 'tags' in api_result:
        for tag in api_result['tags']:
            output['tags'].append((tag['tag'], tag['confidence']))
    else:
        output['tags'].append(('none found', None))

    return output
