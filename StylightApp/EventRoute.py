import json
from datetime import datetime

from flask import request, make_response
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from werkzeug.exceptions import BadRequest, NotFound, NotAcceptable, Conflict

from StylightApp import api, Resource, name_space, db
from StylightApp.models import Event


model = api.model("Event Model", Event.__json__())


@name_space.route('/event')
class PostEvent(Resource):

    @api.doc(responses={201: 'Created', 400: 'Invalid payload supplied', 406: 'Invalid Accept', 409: "Event already exists"})
    @api.expect(model, validate=True)
    def post(self):
        if request.headers.get("Accept") != 'application/json':
            raise NotAcceptable("Invalid Accept")

        request_dict = json.loads(request.data.decode("utf-8"))
        request_dict["timestamp"] = datetime.strptime(request_dict["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
        try:
            event = Event(**request_dict)
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Conflict("Event already exists")

        return make_response(json.dumps({"Added": "OK"}), 201)


@name_space.route('/event/<string:id>')
class GetDeleteEvent(Resource):

    @api.doc(responses={200: 'OK', 400: 'Invalid ID supplied', 404: 'Event not found', 406: "Invalid Accept"})
    def get(self, id):
        if request.headers.get("Accept") != 'application/json':
            raise NotAcceptable("Invalid Accept")

        if len(id) != 36:
            raise BadRequest("Invalid ID supplied")

        try:
            event = Event.query.filter_by(id=id).one()
        except NoResultFound:
            raise NotFound("Event not found")

        return event.to_dict()

    @api.doc(responses={204: 'OK', 400: 'Invalid ID supplied', 406: "Invalid Accept"})
    def delete(self, id):
        if request.headers.get("Accept") != 'application/json':
            raise NotAcceptable("Invalid Accept")

        try:
            event = Event.query.filter_by(id=id).one()
        except NoResultFound:
            raise BadRequest("Invalid ID supplied")

        db.session.delete(event)
        db.session.commit()
        return make_response(json.dumps({"Deleted": "OK"}), 204)
