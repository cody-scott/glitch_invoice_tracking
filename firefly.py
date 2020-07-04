import requests
import os
import datetime
import logging


def push_expense(spreadsheet_id, data):
    if len(data) == 0:
        return

    _sh = os.getenv('cs_sheet')
    if _sh != spreadsheet_id:
        return

    description = data[0]
    date = data[1]
    amount = data[2]
    tag = data[3]

    # firefly doesn't accept zero dollar api requests apparently
    if amount == 0:
        return

    # fix date
    tm_dt = datetime.datetime.strptime(date, "%m/%d/%Y")
    date = tm_dt.strftime("%Y-%m-%d")


    _url = f"{os.getenv('ff_url')}/api/v1/transactions"

    data = {
        "transactions": [{
            "type": "withdrawal",
            "description": description,
            "date": date,
            "amount": amount,
            "source_id": 1,
            "destination_name": description,
            "budget_name": None,
            "tags": ",".join([tag, "apple shortcuts"])
        }]
    }

    token = os.getenv("ff_token")
    headers = hdrs = {'Authorization': f"Bearer {token}"}

    # if token is not None:
    #     logging.info(True)
    #     logging.info(len(token))
    # else:
    #     logging.info(False)

    # logging.info(data)
    # logging.info(_url)

    r = requests.post(_url, json=data, headers=headers)
    # logging.info(r.text)
