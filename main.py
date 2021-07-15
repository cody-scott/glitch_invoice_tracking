from fastapi.param_functions import Header, Query, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI, Depends

from typing import List, Optional

from models import InvoiceModel, SheetsResponseModel
from security import verify_header

import google_tools
import processing

from dotenv import load_dotenv

load_dotenv()
google_tools.load_g_data()

app = FastAPI(
    dependencies=[Depends(verify_header)],
)
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post('/submitInvoice', response_model=SheetsResponseModel)
def view_submit_invoices(invoice_data: InvoiceModel, sheet_id: str = Header(...)):
    service = google_tools.get_service()
    result = processing.submit_invoice(service, sheet_id, invoice_data)
    return {"updated_rows": result["updates"]["updatedRows"], "status": "sucess"}


@app.get('/recentInvoices', response_model=List[InvoiceModel])
def view_recent_invoices(sheet_id: str = Header(...), invoice_count: Optional[int] = None):
    service = google_tools.get_service()
    res = processing.get_recent_invoices(service, sheet_id, invoice_count)
    return res


@app.get("/getCategories", response_model=List)
def view_get_categories(sheet_id: str = Header(...)):
    service = google_tools.get_service()
    data = processing.get_categories(service, sheet_id)
    return data

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
