from flask import render_template
from flask import Response
from flask import request
from app import app
from urllib.request import urlopen
import json
import ssl
import BdMtgCal
import ResultsCal
import datetime
import uuid


@app.route('/boardmeeting', methods=['GET'])
def boardmeeting():
    try:
        file_uuid = str(uuid.uuid4())
        BdMtgCal.downloadPDF(
            request.args.get('url'), file_uuid)
        BMdate = BdMtgCal.GetDate("files/" + file_uuid + ".pdf")
        print(BMdate)
        return Response(datetime.datetime.strftime(BMdate, '%d-%b-%Y'))
    except:
        return Response("(error)")


@app.route('/results', methods=['GET'])
def results():
    try:
        results_date = ResultsCal.GetDate(
            request.args.get('title'), request.args.get('url'))
        print(results_date)
        return Response(datetime.datetime.strftime(results_date, '%d-%b-%Y'))
    except:
        return Response("(error)")
