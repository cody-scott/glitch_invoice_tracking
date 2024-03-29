import os
import processing
import json
import logging
from flask import Flask, request, jsonify
import google_service_api
from dotenv import load_dotenv
load_dotenv()

# import firefly

import load_google
load_google.load_g_data()

app = Flask(__name__)

from _log import setup_logger
setup_logger()
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


logging.info("Starting app")


def _valid_secret_key(method=None):
    sk = request.headers.get('secret_key')
    if method == "POST":
        sk = request.json.get('secret_key')

    if sk == os.getenv("secret_key"):
        return True
    else:
        logging.warning("Invalid Secret Key: {}".format(sk))
        return False


@app.route("/")
def view_index():
    req = request
    env = os.environ

    if not _valid_secret_key():
        return "Secret key not valid"

    return "Completed"


@app.route('/submitInvoice', methods=['POST'])
def view_submit_invoices():
    res = request
    if not _valid_secret_key('POST'):
        return "Secret key not valid"
      
    logging.info("logging receipt")

    sheet_id = request.json.get('sheet_id')
    service = google_service_api.get_service()

    data = request.json.get('data', [])

    logging.info(data[1])
    logging.info(data[2])

    processing.submit_invoice(service, sheet_id, data)

    # firefly.push_expense(sheet_id, data)


    logging.info("Invoice Submitted")
    return "Success"


@app.route('/recentInvoices')
def view_recent_invoices():
    if not _valid_secret_key():
        return "Secret key not valid"

    logging.info("getting recent invoices")
    
    sheet_id = request.headers.get('sheet_id')
    invoice_count = request.headers.get('invoice_count')

    service = google_service_api.get_service()
    data = processing.get_recent_invoices(
        service, spreadsheet_id=sheet_id, invoice_count=invoice_count)
    # json_data = json.dumps(data)
    # return json_data
    return jsonify(data)


@app.route("/getCategories")
def view_get_categories():
    if not _valid_secret_key():
        return "Secret key not valid"
    
    logging.info("Getting categories")
    
    sheet_id = request.headers.get('SHEET_ID')
    service = google_service_api.get_service()
    data = processing.get_categories(service, sheet_id)
    return jsonify(data)


if __name__ == "__main__":
    app.run()
