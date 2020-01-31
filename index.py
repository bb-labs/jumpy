from flask import Flask, request, make_response
from flask_cors import CORS

import json
import numpy as np

app = Flask(__name__)
CORS(app)

cache = {}
DEBUG = False


@app.route("/invoke", methods=["GET"])
def invoke():
    # Each numpy call has arguments, a context, and a field
    args = json.loads(request.headers.get('args'))
    this = json.loads(request.headers.get('this'))
    field = json.loads(request.headers.get('field'))

    # Lookup array arguments by their addresses
    for i, arg in enumerate(args):
        if isinstance(arg, dict) and arg.get('address'):
            args[i] = cache[arg['address']]

    # Set the context depending on the `this` argument
    context = cache[this['address']] if isinstance(this, dict) else np

    # Get the numpy attribute of interest
    attribute = getattr(context, field)

    # Call the numpy field if it's a method, otherwise just get its value
    result = attribute(*args) if callable(attribute) else attribute

    if DEBUG:
        print('-------------{}--------------'.format(field))
        print(this)
        print(args)
        print(result)

    # If the result is of type np.array, cache it, and send the header back
    if isinstance(result, (np.ndarray, np.generic)):
        address, _ = result.__array_interface__['data']
        cache[address] = result

        return make_response(json.dumps({
            'address': address,
            'size': result.size,
            'shape': result.shape,
            'dtype': str(result.dtype),
            'strides': result.strides,
        }), {
            'content-type': "array"
        })

    # If the result is of type bytes, send it over.
    if isinstance(result, bytes):
        return make_response(result, {
            'content-type': "bytes",
        })

    # Otherwise just dump the json
    return json.dumps(result)
