#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


# GET /bakeries - all bakeries with nested baked goods
@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in all_bakeries]
    return make_response(jsonify(bakery_list), 200)


# GET /bakeries/<int:id> - one bakery with nested baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    return make_response(jsonify(bakery.to_dict()), 200)


# GET /baked_goods/by_price - all baked goods sorted by price DESC
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = [good.to_dict() for good in goods]
    return make_response(jsonify(goods_list), 200)


# GET /baked_goods/most_expensive - single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(jsonify(most_expensive.to_dict()), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
