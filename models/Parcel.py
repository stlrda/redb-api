from pydantic import BaseModel
from typing import List, Optional

# Define Parcel Models
class ParcelTest(BaseModel):
    parcel_id: str

class parcel_specific(BaseModel):
    parcel_id: str
    address_id: int
    parcel_number: str
    description: str
