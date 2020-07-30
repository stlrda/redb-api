from pydantic import BaseModel
from typing import List, Optional

# Define Parcel Models
class single_parcel_info(BaseModel):
    parcels: list
    buildings: list
    units: list