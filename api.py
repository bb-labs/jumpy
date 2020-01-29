from flask import Flask, request, make_response
from flask_cors import CORS

import json
import numpy as np

app = Flask(__name__)
CORS(app)

cache = {}


def make_array_response(array):
    address, _ = array.__array_interface__['data']

    cache[address] = array

    return json.dumps({
        'address': address,
        'size': array.size,
        'shape': array.shape,
        'dtype': str(array.dtype),
        'strides': array.strides,
    })


def lookup_arrays(args):
    for i, arg in enumerate(args):
        if isinstance(arg, dict) and arg.get('address'):
            args[i] = cache[arg['address']]

    return args


@app.route("/instance", methods=["GET"])
def instance_fields():
    args = json.loads(request.headers.get('args'))
    this = json.loads(request.headers.get('this'))
    field = json.loads(request.headers.get('field'))

    clean_args = lookup_arrays(args)

    array = cache[this]
    attribute = getattr(array, field)

    result = attribute(*clean_args) if callable(attribute) else attribute

    print('-------------INSTANCE--------------')
    print(this)
    print(field)
    print(clean_args)
    print(result)

    if isinstance(result, (np.ndarray, np.generic)):
        return make_array_response(result)

    return json.dumps(result)


@app.route("/static", methods=["GET"])
def static_fields():
    args = json.loads(request.headers.get('args'))
    field = json.loads(request.headers.get('field'))

    clean_args = lookup_arrays(args)

    attribute = getattr(np, field)

    result = attribute(*clean_args) if callable(attribute) else attribute

    print('----------STATIC-----------------')
    print(field)
    print(clean_args)
    print(result)

    if isinstance(result, (np.ndarray, np.generic)):
        return make_array_response(result)

    return json.dumps(result)
