import json

def lambda_handler(event, context):
    # Parse query string parameters
    params = event.get('queryStringParameters', {})
    code = params.get('code', '')
    name = params.get('name', '')
    country = params.get('country', '')

    print(f'code = {code}')
    print(f'name = {name}')
    print(f'country = {country}')

    # Construct response body
    response = {
        'code': code,
        'name': name,
        'country': country,
        'message': 'Hello from Lambda'
    }

    # Construct http response object
    responseObj = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }

    # Return the response object
    return responseObj
