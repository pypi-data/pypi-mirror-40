import subprocess
from datetime import datetime
import pause

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    if request.method == 'POST':
        num = request.json["number"]
        message = request.json["message"]

        datetime_to_send = datetime.strptime(
            request.json["datetime"],
            '%b %d %Y %I:%M%p')

        pause.until(datetime_to_send)

        return str(subprocess.call(
            "termux-sms-send -n " + num + " " + message,
            shell=True
        ))
