import time
from requests import Session

url = "http://localhost:9999/crash_report"


def send_crash_notification(message):
    with Session() as s:
        try:
            s.get(url, timeout=2)
        except TimeoutError:
            return False

        msg = {}
        msg["timestamp"] = time.time()
        msg["context"] = message
        with open("logs/peracotta.log", "r") as fs:
            msg["log"] = fs.read()
        res = s.post(url, json=msg)

        if res.status_code == 200:
            return True
