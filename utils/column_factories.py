import datetime
import uuid


def datetime_now_no_tz():
    return datetime.datetime.utcnow().replace(tzinfo=None)


def str_uuid_factory():
    return str(uuid.uuid4())
