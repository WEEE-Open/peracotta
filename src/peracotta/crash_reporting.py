from requests import Session

from .config import CONFIG
from .peralog import logdir

url = CONFIG["REPORT_URL"]


def send_crash_notification():
    with Session() as s:
        try:
            s.get(url, timeout=2)
        except TimeoutError:
            return False

        with open(logdir.joinpath("peracotta.log"), "r") as fs:
            res = s.post(url, files={"file": fs})

        if res.status_code == 200:
            return True
