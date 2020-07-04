import requests
import os
import datetime

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

    # fix date
    tm_dt = datetime.datetime.strptime(date, "%m/%d/%Y")
    date = tm_dt.strftime("%Y-%m-%d")

    # fix amount
    amount = float(amount.replace("$", "").replace(",",""))

    # check to make sure only my requests are going through. 
    # smarter way would be to add a different token system and route on that maybe


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

    r = requests.post(_url, json=data, headers=headers)
