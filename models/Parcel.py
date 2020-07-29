from pydantic import BaseModel
from typing import List, Optional

# Define Parcel Models
class ParcelTest(BaseModel):
    parcel_id: str

class current_single_parcel_info(BaseModel):
    parcel_id: str
    address_id: int
    parcel_number: str
    description: str
    buildings: list
    units: list

class parcel_owned_by_id(BaseModel):
    parcel_id: str