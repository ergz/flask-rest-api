from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema



blp = Blueprint("Tags", "tags", description="operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):


    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)

        return store.tags

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(store_id=store_id, **tag_data)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

@blp.route("/tag/<string:tag_id>")
class TagDetail(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = db.get_or_404(TagModel, tag_id)
        return tag
    
@blp.route("/tag/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItems(MethodView):

    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @blp.response(201, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "item removed from tag", "item": item, "tag": tag}


