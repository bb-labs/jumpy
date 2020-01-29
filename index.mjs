import fields from './fields.mjs'

class Tensor {
    constructor(header) { this.header = header }

    /** Numpy API */
    static API = {
        static: 'http://localhost:5000/static',
        instance: 'http://localhost:5000/instance',
    }

    /** Numpy Types */
    static int8 = class int8 extends Int8Array { }
    static int16 = class int16 extends Int16Array { }
    static int32 = class int32 extends Int32Array { }
    static int64 = class int64 extends BigInt64Array { }
    static uint8 = class uint8 extends Uint8Array { }
    static uint16 = class uint16 extends Uint16Array { }
    static uint32 = class uint32 extends Uint32Array { }
    static uint64 = class uint64 extends BigUint64Array { }
    static float32 = class float32 extends Float32Array { }
    static float64 = class float64 extends Float64Array { }
    static complex64 = class complex64 extends Float32Array { }
    static complex128 = class complex128 extends Float64Array { }

    /** Numpy Generic Invoker */
    static invoker(field) {
        return async function (...args) {
            const api = this === Tensor
                ? Tensor.API.static
                : Tensor.API.instance

            const response = await fetch(api, {
                headers: {
                    args: JSON.stringify(args, Tensor.clean),
                    this: JSON.stringify(this, Tensor.clean),
                    field: JSON.stringify(field, Tensor.clean),
                }
            })

            return 'Pending'
        }
    }

    /** JSON Reference and Type Replacement */
    static clean(key, value) {
        if (value.constructor === Function)
            return value.name

        if (value.constructor === Tensor)
            return value

        return value
    }
}

/** Numpy Static Fields */
for (const field of fields.static)
    Tensor[field] = Tensor.invoker(field)

/** Numpy Instance Fields */
for (const field of fields.instance)
    Tensor.prototype[field] = Tensor.invoker(field)

export default Tensor
