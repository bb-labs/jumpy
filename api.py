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

    return make_response(array.tobytes(), {
        'Access-Control-Expose-Headers': 'metadata',
        'metadata': json.dumps({
            'address': address,
            'size': array.size,
            'shape': array.shape,
            'dtype': str(array.dtype),
            'strides': array.strides,
        })
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

    array = cache[this.get('address')]
    attribute = getattr(array, field)

    result = attribute(*clean_args) if callable(attribute) else attribute

    if isinstance(result, np.ndarray):
        return make_array_response(result)

    return attribute


@app.route("/static", methods=["GET"])
def static_fields():
    args = json.loads(request.headers.get('args'))
    field = json.loads(request.headers.get('field'))

    clean_args = lookup_arrays(args)

    attribute = getattr(np, field)

    result = attribute(*clean_args) if callable(attribute) else attribute

    if isinstance(result, np.ndarray):
        return make_array_response(result)

    return result
