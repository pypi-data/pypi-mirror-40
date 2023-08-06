from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields

__all__ = ["ma", "schedule_schema", "upload_scheduling_schema",
           "setup_schemas"]

ma = Marshmallow()


def setup_schemas(app: Flask):
    return ma.init_app(app)


class ScheduleSchema(ma.Schema):
    class Meta:
        ordered = True
    id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    org_id = fields.UUID(required=True)
    workspace_id = fields.UUID(required=True)
    experiment_id = fields.UUID(required=True)
    token_id = fields.UUID(required=True)
    job_id = fields.UUID(allow_none=True)
    scheduled = fields.DateTime()
    repeat = fields.Integer(allow_none=True)
    interval = fields.Integer(allow_none=True)
    cron = fields.String(allow_none=True)
    results = fields.List(fields.Dict(keys=fields.String()), allow_none=True)
    url = ma.AbsoluteURLFor('scheduling.get', schedule_id='<id>')
    links = ma.Hyperlinks({
        'self': ma.URLFor('scheduling.get', schedule_id='<id>')
    })


class UploadSchedulingSchema(ma.Schema):
    org = fields.UUID(required=True)
    workspace = fields.UUID(required=True)
    experiment = fields.UUID(required=True)
    token = fields.UUID(required=True)
    scheduled = fields.String(required=True)
    repeat = fields.Integer(allow_none=True)
    interval = fields.Integer(allow_none=True)
    cron = fields.String(allow_none=True)
    settings = fields.Dict(keys=fields.String(), allow_none=True)
    configuration = fields.Dict(keys=fields.String(), allow_none=True)
    secrets = fields.Dict(keys=fields.String(), allow_none=True)


schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)
upload_scheduling_schema = UploadSchedulingSchema()
