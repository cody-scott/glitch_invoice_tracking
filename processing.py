import requests
import json
import re
from collections import OrderedDict

import logging


def _get_range_data(service, spreadsheet_id, _range):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=_range).execute()
    return result


def get_categories(service, spreadsheet_id):
    _catg_range = "'Data Table'!C2:C200"
    result = _get_range_data(service, spreadsheet_id, _catg_range)
    values = [i[0] for i in result['values']]
    values.sort()
    return values


def get_recent_invoices(service, spreadsheet_id, invoice_count=None):
    if invoice_count is None:
        invoice_count = 10
    else:
        invoice_count = int(invoice_count)

    _range = "'Appleshortcuts_Response'!A1:D500"
    result = _get_range_data(service, spreadsheet_id, _range)
    values = result['values'][1:]

    min_index = max(len(values) - invoice_count, 0)
    sub_values = values[min_index:]

    cost_pattern = re.compile(pattern='\$\s*-')
    data_dict = OrderedDict()
    for val in sub_values:
        _item = val[0].strip()
        _date = val[1].strip().split("/")
        _cost = val[2].strip()

        if len(cost_pattern.findall(_cost)) > 0:
            _cost = '$ 0.00'

        out_str = " - ".join([_item, "/".join(_date), _cost])
        file_str = " ".join([_item, "_".join([_date[1], _date[0], _date[2]])])
        data_dict[out_str] = file_str

    return data_dict


def submit_invoice(service, spreadsheet_id, data):
    sheet = service.spreadsheets()

    dct = {
        'spreadsheetId': spreadsheet_id,
        'range': 'Appleshortcuts_Response',
        'valueInputOption': 'USER_ENTERED',
        'body': {
            'values': [data]
        }
    }
    sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range='Appleshortcuts_Response',
        valueInputOption='USER_ENTERED',
        body={
            'values': [data]
            }
    ).execute()

    pass


