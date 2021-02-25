from flask import Flask, request, make_response
from flask_restplus import Api, Resource, fields

from helper import compute_quantile

flask_app = Flask(__name__)
app = Api(app=flask_app,
          title="Quantile computation",
          description="""An application with two APIs that:
                            - Store and update pools of samples and 
                            - Compute value of quantile p-th of a pool with given p-th quantile""")

name_space = app.namespace('/', description="List of APIs")

pool_query_model = app.model("pool_query", {
    "poolId": fields.Integer(required=True, description="Index of pool"),
    "percentile": fields.Float(required=True, description="p-th percentile of the list of samples to compute value")
})

pool_model = app.model("pool", {
    "poolId": fields.Integer(required=True, description="Index of pool"),
    "poolValues": fields.List(fields.Float, required=True, description="List of samples")
})

pools = []


@name_space.route('/pool')
class Pool(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @app.expect(pool_model)
    def post(self):
        try:
            if request.is_json:
                input_data = request.get_json()
                pool_id = input_data.get("poolId")
                pool_values = input_data.get("poolValues")
                if pool_id is not None and pool_values is not None:
                    pool_id = int(pool_id)
                    pool_values = list(map(float, pool_values))
                    for pool in pools:
                        if pool_id in pool:
                            pool[pool_id].extend(pool_values)
                            return make_response({"status": "appended"}, 200)
                    pools.append({pool_id: pool_values})
                    return make_response({"status": "inserted"}, 200)
                else:
                    raise ValueError("poolId/poolValues is None")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not insert/update pool", statusCode="400")


@name_space.route('/quantile')
class Quantile(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 204: 'No Content'})
    @app.expect(pool_query_model)
    def post(self):
        try:
            if request.is_json:
                input_data = request.get_json()
                pool_id = input_data.get("poolId")
                percentile = input_data.get("percentile")
                if pool_id is not None and percentile is not None:
                    pool_id = int(pool_id)
                    percentile = float(percentile)
                for pool in pools:
                    if pool_id in pool:
                        return make_response(
                            {
                                "numSamples": len(pool[pool_id]),
                                "percentile": compute_quantile(pool[pool_id], percentile)
                            },
                            200)
                return make_response({}, 204)
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not query the pool", statusCode="400")


if __name__ == '__main__':
    flask_app.run(debug=True, host="0.0.0.0")
