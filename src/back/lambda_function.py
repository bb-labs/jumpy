import json
import base64
import numpy as np

cache = {}


def make_response(content_type, content):
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Content-Type": content_type,
        },
        'body': content
    }


def lambda_handler(event, context):
    # Each numpy call has arguments, a context, and a field
    body = json.dumps(event['body'])

    args = body['args']
    this = body['this']
    field = body['field']

    # Lookup array arguments by their addresses
    for i, arg in enumerate(args):
        if isinstance(arg, dict) and 'address' in arg:
            args[i] = cache[arg['address']]

    # Set the context depending on the `this` argument
    context = cache[this['address']] if isinstance(this, dict) else np

    # Get the numpy attribute of interest
    attribute = getattr(context, field)

    # Call the numpy field if it's a method, otherwise just get its value
    result = attribute(*args) if callable(attribute) else attribute

    print('-------------{}--------------'.format(field))
    print(this)
    print(args)
    print(result)

    # If the result is of type np.array, cache it, and send the header back
    if isinstance(result, (np.ndarray, np.generic)):
        address, _ = result.__array_interface__['data']
        cache[address] = result

        return make_response('array', json.dumps({
            'address': address,
            'size': result.size,
            'shape': result.shape,
            'dtype': str(result.dtype),
            'strides': result.strides,
        }))

    # If the result is of type bytes, send it over.
    if isinstance(result, bytes):
        return make_response('bytes', base64.b64encode(result).decode('utf8'))

    # Otherwise just dump the json
    return json.dumps(result)
