from pydantic import BaseModel
from typing import List, Optional

# Define Parcel Models
class LegalEntityName(BaseModel):
    legal_entity_id: int
    legal_entity_address: Optional[str]
    legal_entity_name: Optional[str]
    legal_entity_secondary_name: Optional[str]
    address_id: int