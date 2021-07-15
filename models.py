from pydantic import BaseModel
import datetime
from typing import List, Optional

class InvoiceModel(BaseModel):
    item: str
    date: datetime.date
    cost: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "item": "test",
                "date": datetime.date(2019, 1, 1),
                "cost": 0.0,
                "category": "eating out",
            }
        }

class SheetsResponseModel(BaseModel):
    updated_rows: int
    status: str
