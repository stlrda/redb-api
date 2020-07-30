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