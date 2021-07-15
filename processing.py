import re
from collections import OrderedDict
from typing import Optional
from fastapi.encoders import jsonable_encoder
from googleapiclient.discovery import Resource
import models

import datetime


def _get_range_data(service: Resource, spreadsheet_id: str, _range: str):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=_range).execute()
    return result


def get_categories(service: Resource, spreadsheet_id: str):
    _catg_range = "'Data Table'!C2:C200"
    result = _get_range_data(service, spreadsheet_id, _catg_range)
    values = [i[0] for i in result['values']]
    values.sort()
    return values


def get_recent_invoices(service: Resource, spreadsheet_id: str, invoice_count: Optional[int]=None):
    invoice_count = 10 if invoice_count is None else invoice_count

    _range = "'Appleshortcuts_Response'!A:D"
    result = _get_range_data(service, spreadsheet_id, _range)
    values = result['values'][1:]

    min_index = max(len(values) - invoice_count, 0)
    sub_values = values[min_index:]

    cost_pattern = re.compile(pattern='\$\s*-')
    results = []
    for val in sub_values:
        _item = val[0].strip()

        _fmt = "%m/%d/%Y" if "-" not in val[1] else "%Y-%m-%d"
        _date = datetime.datetime.strptime(val[1], _fmt).date()
        _cost = val[2].replace('$ ', '').strip()
        _cost = 0 if _cost=="-" else _cost
        _category = val[3].strip()
        results.append(models.InvoiceModel(
            item=_item, 
            date=_date, 
            cost=_cost, 
            category=_category))


    return results


def submit_invoice(service: Resource, spreadsheet_id: str, data: models.InvoiceModel):
    sheet = service.spreadsheets()

    data = [_ for _ in jsonable_encoder(data).values()]
    
    res = sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range='Appleshortcuts_Response',
        valueInputOption='USER_ENTERED',
        body={
            'values': [data]
            }
    ).execute()

    return res
