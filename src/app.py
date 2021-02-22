from flask import Flask, request, make_response, jsonify
from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
app = Api(app=flask_app, title="Quantile computation", description="Compute value of quantile p-th of an array")

name_space = app.namespace('/', description="List of APIs")

pool_query_model = app.model("pool_query", {
    "pool_id": fields.List(fields.Float, required=True, description="List of samples"),
    "percentile": fields.Float(required=True, description="p-th percentile of the list of samples to compute")
})

pool_model = app.model("pool_model", {
    "poolId": fields.Integer(required=True, description="index of pool"),
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
                if len(pools) == 0:
                    pools.append({pool_id: pool_values})
                    return make_response({"status": "inserted"}, 200)
                else:
                    for pool in pools:
                        if pool_id in pool:
                            pool[pool_id].extend(pool_values)
                            return make_response({"status": "appended"}, 200)
                        else:
                            pool[pool_id] = pool_values
                            return make_response({"status": "inserted"}, 200)
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not insert/update pool", statusCode="400")


if __name__ == '__main__':
    flask_app.run(debug=True, host="0.0.0.0")
