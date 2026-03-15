import json

from flask import Flask, request, make_response, jsonify #, Response
from flask_restful import Api, Resource, abort, reqparse
from functools import wraps
import pandas as pd
import pdbasics
import ext_quotes as xq
import ext_founders as xf

# sug = pd.read_json("ext_quotes.json", encoding=None)
# # rows, columns = sug.shape
# r1 = sug.shape[0]
# # print(r1)


# hope = pdbasics.plsgo()
# print("Hopefully... ", hope)


# QUOTES = pd.read_json("ext_quotes.json", encoding=None).to_json()

# QUOTES = ()
FOUNDERS = xf.QDATA
QUOTES = xq.QDATA


app = Flask(__name__)
api = Api(app)


def login_required(event):
    @wraps(event)
    def login(*args, **kwargs):
        if request.authorization and \
                request.authorization.username == "admin" and \
                request.authorization.password == "test1234":
            return event(*args, **kwargs)

        return make_response("Could not verify your credentials.", 401, {'WWW-Authenticate': 'Basic realm="Login Realm"'})
    return login


parser = reqparse.RequestParser()
parser.add_argument("quote")
parser.add_argument("name")
parser.add_argument("text")


def abort_quote_does_not_exist(quote_id):
    if quote_id not in QUOTES:
        abort(404, message="Quote {} does not exist.".format(quote_id))


class Quote(Resource):
    # @login_required
    def get(self, quote_id):
        abort_quote_does_not_exist(quote_id)
        return QUOTES[quote_id]

    # def delete(self, quote_id):
    #     abort_quote_does_not_exist(quote_id)
    #     del QUOTES[quote_id]
    #     return "", 204
    #
    # def put(self, quote_id):
    #     args=parser.parse_args()
    #     quote_info = {"quote": args["quote"], "name": args["name"], "text": args["text"]}
    #     QUOTES[quote_id] = quote_info
    #     return quote_id, 201


class QuoteList(Resource):
    def get(self):
        return jsonify(QUOTES)


class PAfounders(Resource):
    def get(self):
        return jsonify(FOUNDERS)

    # def post(self):
    #     args = parser.parse_args()
    #
    #     current_quote_id = 0
    #
    #     if len(QUOTES) > 0:
    #         for quote in QUOTES:
    #             x = int(quote.split("_")[-1])
    #             if x > current_quote_id:
    #                 current_quote_id = x
    #
    #     QUOTES[f"quote_{current_quote_id + 1}"] = {"quote": args["quote"], "name": args["name"], "text": args["text"]}
    #     return QUOTES[f"quote_{current_quote_id + 1}"], 201


api.add_resource(PAfounders, "/founders")
api.add_resource(QuoteList, "/quotes")


api.add_resource(Quote, '/quotes/<quote_id>')

# def hello():
#     return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
