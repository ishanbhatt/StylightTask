from datetime import date
from pprint import pprint

from sqlalchemy.exc import CompileError, OperationalError
from werkzeug.exceptions import BadRequest
from flask import request

from StylightApp import api, Resource, name_space
from StylightApp.models import Event


parser = api.parser()
parser.add_argument('offset', type=int)
parser.add_argument('limit', type=int)
parser.add_argument('group_by', type=str, help="Space Delimited")
parser.add_argument('order_by', type=str, help="Space Delimited")
parser.add_argument('client', type=str, help="Space Delimited")
parser.add_argument('client_group', type=str, help="Space Delimited")
parser.add_argument('device_type', type=str, help="Space Delimited")
parser.add_argument('category', type=str, help="Space Delimited")
parser.add_argument('valid', type=bool)
parser.add_argument('start_date', type=date)
parser.add_argument('end_date', type=date)


@name_space.route('/report')
class Report(Resource):

    @staticmethod
    def _split_model_parameters(req):
        model_dict = {}
        non_model_dict = {}
        integer_fields = ["category", "client", "client_group"]
        for key in req.args:
            if hasattr(Event, key):
                if key in integer_fields:
                    model_dict[key] = list(map(int, req.args.get(key).strip().split(" ")))

                elif key == "valid":
                    values = list(map(lambda x: True if x=="true" else False, req.args.get(key).strip().split(" ")))
                    model_dict[key] = values
                else:
                    model_dict[key] = req.args.get(key).strip().split(" ")
            else:
                non_model_dict[key] = req.args.get(key).strip().split(" ")
        return model_dict, non_model_dict

    @api.expect(parser)
    @api.doc(responses={200: 'OK', 400: 'Invalid / Inconsistent parameters', 406: 'Invalid Accept'})
    def get(self):
        builder = Event.query
        model_dict, non_model_dict = self._split_model_parameters(request)
        # https: // stackoverflow.com / questions / 19506105 / flask - sqlalchemy - query - with-keyword -as-variable
        pprint(model_dict)
        for k, v in model_dict.items():
            builder = builder.filter(getattr(Event, k).in_(v))

        try:
            # group by
            group_by_columns = non_model_dict.get("group_by")
            if group_by_columns:
                builder = builder.with_entities(*group_by_columns)  # Handling of groupby columns

            # order by
            order_by_columns = non_model_dict.get("order_by")
            if order_by_columns:
                for column in order_by_columns:
                    builder = builder.order_by(column)

            # limit
            limit = non_model_dict.get("limit", 0)
            if limit:
                response = builder.all()[:int(limit[0])]
            else:
                response = builder.all()

            if group_by_columns:
                # Super nasty but it works to get column names
                response = [{group_by_columns[i]: answer[i] for i in range(len(answer))} for answer in response]
            else:
                response = [x.to_dict() for x in response]

        except OperationalError:
            print("INVALID GROUP-BY Columns specified")
            raise BadRequest("Invalid / Inconsistent parameters")

        except CompileError:
            print("INVALID ORDER-BY Columns specified")
            raise BadRequest("Invalid / Inconsistent parameters")

        return response
