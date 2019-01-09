from flask import render_template
from flask import Response
from flask import request
from app import app
from urllib.request import urlopen
import json
import ssl
import BdMtgCal
import datetime
import uuid


@app.route('/boardmeeting', methods=['GET'])
def index():
    file_uuid = str(uuid.uuid4())
    BdMtgCal.downloadPDF(
        request.args.get('url'), file_uuid)
    BMdate = BdMtgCal.GetDate("files/" + file_uuid + ".pdf")
    print(BMdate)
    return Response(datetime.datetime.strftime(BMdate, '%d-%b-%Y'))
