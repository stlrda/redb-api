from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Define Parcel Models
class SingleParcelInfo(BaseModel):
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
    