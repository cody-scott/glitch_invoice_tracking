import os
import processing
import json

from flask import Flask, request, jsonify
import google_service_api
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


def _valid_secret_key(method=None):
    sk = request.headers.get('secret_key')
    if method == "POST":
        sk = request.json.get('secret_key')

    if sk == os.getenv("secret_key"):
        return True
    else:
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

    sheet_id = request.json.get('sheet_id')
    service = google_service_api.get_service()

    data = request.json.get('data', [])
    processing.submit_invoice(service, sheet_id, data)

    return "Success"


@app.route('/recentInvoices')
def view_recent_invoices():
    if not _valid_secret_key():
        return "Secret key not valid"

    sheet_id = request.headers.get('sheet_id')
    invoice_count = request.headers.get('invoice_count')

    service = google_service_api.get_service()
    data = processing.get_recent_invoices(
        service, spreadsheet_id=sheet_id, invoice_count=invoice_count)
    json_data = json.dumps(data)
    return json_data


@app.route("/getCategories")
def view_get_categories():
    if not _valid_secret_key():
        return "Secret key not valid"

    sheet_id = request.headers.get('SHEET_ID')
    service = google_service_api.get_service()
    data = processing.get_categories(service, sheet_id)
    return jsonify(data)


if __name__ == "__main__":
    app.run()
