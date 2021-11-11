import datetime
import pytz

DR_TIMEZONE_NAME = "America/Santo_Domingo"

DR_TIMEZONE = pytz.timezone(DR_TIMEZONE_NAME)


def get_current_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
