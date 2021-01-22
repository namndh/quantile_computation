from flask import Flask, request, make_response
from flask_restplus import Api, Resource, fields

from utils import compute_quantile

flask_app = Flask(__name__)
app = Api(app=flask_app, title="Quantile computation", description="Compute value of quantile p-th of an array")

name_space = app.namespace('/', description="List of APIs")

input_model = app.model("Input", {
    "pool": fields.List(fields.Float, required=True, description="List of samples"),
    "percentile": fields.Float(required=True, description="p-th percentile of the list of samples to compute")
})


@name_space.route('/quantile')
class Quantile(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument'})
    @app.expect(input_model)
    def post(self):
        try:
            if request.is_json:
                input_data = request.get_json()
                pool = input_data.get("pool")
                percentile = input_data.get("percentile")
                if pool is not None and percentile is not None:
                    pool = list(map(float, pool))
                    percentile = float(percentile)
                return make_response({"quantile": compute_quantile(pool, percentile)}, 200)
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not compute quantile", statusCode="400")


if __name__ == '__main__':
    flask_app.run(debug=True, host="0.0.0.0")
