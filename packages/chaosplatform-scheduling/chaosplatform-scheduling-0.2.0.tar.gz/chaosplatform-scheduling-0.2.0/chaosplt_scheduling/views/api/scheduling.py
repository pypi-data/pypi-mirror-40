# -*- coding: utf-8 -*-
from uuid import UUID

from dateparser import parse
from flask import abort, Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError
import simplejson as json

from chaosplt_scheduling.schemas import schedule_schema, \
        upload_scheduling_schema

__all__ = ["api"]

api = Blueprint("scheduling", __name__)


@api.route('', methods=['POST'])
@login_required
def new():
    user_id = current_user.id
    try:
        payload = upload_scheduling_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    org_id = payload["org"]
    workspace_id = payload["workspace"]
    experiment_id = payload["experiment"]
    token_id = payload["token"]
    scheduled_at = payload["scheduled"]

    # periodicity
    interval = payload.get("interval", None)
    cron = payload.get("cron", None)
    repeat = payload.get("repeat", None)

    # context for the experiment
    settings = payload.get("settings", None)
    configuration = payload.get("configuration", None)
    secrets = payload.get("secrets", None)

    if interval and cron:
        return jsonify({
            "message": "Cannot use cron and interval at the same time"
        }), 422

    schedule_dt = parse(scheduled_at, settings={'TO_TIMEZONE': 'UTC'})
    if not schedule_dt:
        return jsonify({
            "message": "Invalid schedule date"
        }), 422

    token = request.services.auth.access_token.get(user_id, token_id)
    if not token:
        return jsonify({
            "message": "Invalid token"
        }), 422

    experiment = request.services.experiment.get_by_user(
        user_id, experiment_id)
    if not experiment:
        return jsonify({
            "message": "Invalid experiment"
        }), 422

    # store the schedule
    schedule = request.services.scheduling.create(
        user_id, org_id, workspace_id, experiment_id, token_id,
        scheduled_at, repeat, interval, cron, settings, configuration, secrets)

    # trigger the actual scheduler
    job_id = request.services.scheduler.schedule(
        str(schedule.id), str(user_id), str(org_id), str(workspace_id),
        str(schedule.experiment_id), str(token_id), token.access_token,
        scheduled_at, json.dumps(experiment.payload),
        interval, repeat, cron, settings, configuration, secrets)

    # update our records
    request.services.scheduling.job_started(schedule.id, job_id)
    schedule = request.services.scheduling.get(user_id, schedule.id)
    schedule.job_id = job_id

    return schedule_schema.jsonify(schedule)


@api.route('<uuid:schedule_id>', methods=['GET'])
@login_required
def get(schedule_id: UUID):
    user_id = current_user.id
    schedule = request.services.scheduling.get(user_id, schedule_id)
    if not schedule:
        return abort(404)
    return schedule_schema.jsonify(schedule)


@api.route('<uuid:schedule_id>', methods=['DELETE'])
@login_required
def delete(schedule_id: UUID):
    user_id = current_user.id
    schedule = request.services.scheduling.get(user_id, schedule_id)
    if schedule:
        request.services.scheduler.cancel(str(schedule.job_id))
        request.services.scheduling.delete(schedule_id)
    return jsonify(""), 204
