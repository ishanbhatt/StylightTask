import json


from datetime import datetime

from StylightApp import db
from StylightApp.models import Event

counter = 0
with open("input_data", "r") as handle:
    for line in handle:
        event_json_dict = json.loads(line)
        event_json_dict["timestamp"] = datetime.strptime(event_json_dict["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
        event = Event(**event_json_dict)
        db.session.add(event)
        counter += 1
        if counter % 500 == 0:
            db.session.commit()
    db.session.commit()
