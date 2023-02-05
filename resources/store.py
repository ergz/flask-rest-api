import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import StoreSchema
from models import StoreModel
from db import db

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        return store

    def delete(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted"}


@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = db.session.execute(
            db.select(StoreModel)
        ).scalars().all()

        return stores

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400, 
                message="A store with that name exists already!"
            )
        except SQLAlchemyError:
            abort(
                404, 
                message="unable to perform new store insert into database"
            )

        return store