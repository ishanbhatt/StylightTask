from StylightApp import db, fields


class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    device_type = db.Column(db.String(20))
    category = db.Column(db.Integer)
    client = db.Column(db.Integer)
    client_group = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    valid = db.Column(db.Boolean)
    value = db.Column(db.Float)

    @staticmethod
    def __json__():
        return {"id": fields.String(required=True),
                "device_type": fields.String(required=True),
                "category": fields.Integer(required=True),
                "client": fields.Integer(required=True),
                "client_group": fields.Integer(required=True),
                "timestamp": fields.DateTime(required=True),
                "valid": fields.Boolean(required=True),
                "value": fields.Float(required=True)
                }

    def __str__(self):
        return f"{self.id} - {self.device_type} - {self.category} - {self.device_type}"

    def to_dict(self):
        return {"id": self.id,
                "device_type": self.device_type,
                "category": self.category,
                "client": self.client,
                "client_group": self.client_group,
                "timestamp": self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "valid": self.valid,
                "value": self.value
                }
