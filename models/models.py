from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Define Parcel Models
class ParcelInfo(BaseModel):
    parcels: list
    buildings: list
    units: list

class FindLatestUpdate(BaseModel):
    last_update: date

class FilterParcelCounts(BaseModel):
    building_use: str
    count: int

class FilterParcelIds(BaseModel):
    parcel_id: str

class LegalEntity(BaseModel):
    legal_entity_id: int
    legal_entity_address: Optional[str]
    legal_entity_name: Optional[str]
    legal_entity_secondary_name: Optional[str]
    address_id: int