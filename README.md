# Currently Implemented Routes

## /redb/parcel/redb_id
This endpoint returns a dictionary of lists which contain information about the parcel(s), building(s), and unit(s) related to a parcel id.<br><br>
The redb_id endpoint requires two inputs for a get request.<br>
- {ParcelInput: str} - Input the full redb parcel id that you want to search the database for<br>
- {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>

For example: **.../redb/parcel/redb_id?ParcelInput=10001.10003220.000.0000&Current=True** would return the following:
<pre>
  {
  "parcels": [
    {
      "parcel_id": "10001.10003220.000.0000",
      "county_id": "10001",
      "address": "210 N TUCKER BLVD  MO USA 63101.0",
      "city_block_number": "503.0",
      "parcel_number": "10003220",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "frontage_to_street": 0,
      "land_area": 1,
      "zoning_class": "I",
      "ward": "7",
      "voting_precinct": "4",
      "inspection_area": "3",
      "neighborhood_id": "29",
      "police_district": "4",
      "census_tract": "1256.0",
      "asr_neighborhood": "261",
      "special_parcel_type": null,
      "sub_parcel_type": "Condo",
      "gis_city_block": "503.0",
      "gis_parcel": "8141.0",
      "gis_owner_code": "0"
    }
  ],
  "buildings": [
    {
      "building_id": "10001.10003220.101.0000",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "building_use": "COM",
      "apartment_count": 0
    },
    {
      "building_id": "10001.10003220.102.0000",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "building_use": "RES",
      "apartment_count": 0
    }
  ],
  "units": [
    {
      "unit_id": "10001.10003220.102.1001",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "condominium": true
    }
  ]
}
</pre>


## /redb/parcel/legal_entity_id
This endpoint returns a dictionary of lists which contain information about the parcel(s), building(s), and unit(s) related to a legal_entity_id.<br><br>
The legal_entity_id endpoint requires two inputs for a get request.<br>
- {IdInput: str} - Input the legal_entity_id that you want to search the database for<br>
- {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>

For example: **.../redb/parcel/legal_entity_id?IdInput=367&Current=True** would return the following:
<pre>
{
  "parcels": [
    {
      "parcel_id": "10001.10003222.000.0000",
      "county_id": "10001",
      "address": "210 N TUCKER BLVD  MO USA 63101.0",
      "city_block_number": "503.0",
      "parcel_number": "10003222",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 N TUCKER CONDO UNIT 302  ",
      "frontage_to_street": 0,
      "land_area": 1,
      "zoning_class": "I",
      "ward": "7",
      "voting_precinct": "4",
      "inspection_area": "3",
      "neighborhood_id": "29",
      "police_district": "4",
      "census_tract": "1256.0",
      "asr_neighborhood": "261",
      "special_parcel_type": null,
      "sub_parcel_type": "Condo",
      "gis_city_block": "503.0",
      "gis_parcel": "8141.0",
      "gis_owner_code": "0"
    },
    {
      "parcel_id": "10001.10003220.000.0000",
      "county_id": "10001",
      "address": "210 N TUCKER BLVD  MO USA 63101.0",
      "city_block_number": "503.0",
      "parcel_number": "10003220",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "frontage_to_street": 0,
      "land_area": 1,
      "zoning_class": "I",
      "ward": "7",
      "voting_precinct": "4",
      "inspection_area": "3",
      "neighborhood_id": "29",
      "police_district": "4",
      "census_tract": "1256.0",
      "asr_neighborhood": "261",
      "special_parcel_type": null,
      "sub_parcel_type": "Condo",
      "gis_city_block": "503.0",
      "gis_parcel": "8141.0",
      "gis_owner_code": "0"
    }
  ],
  "buildings": [
    {
      "building_id": "10001.10003220.101.0000",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "building_use": "COM",
      "apartment_count": 0
    },
    {
      "building_id": "10001.10003220.102.0000",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "building_use": "RES",
      "apartment_count": 0
    },
    {
      "building_id": "10001.10003222.101.0000",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 N TUCKER CONDO UNIT 302  ",
      "building_use": "COM",
      "apartment_count": 0
    },
    {
      "building_id": "10001.10003222.102.0000",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 N TUCKER CONDO UNIT 302  ",
      "building_use": "COM",
      "apartment_count": 0
    }
  ],
  "units": [
    {
      "unit_id": "10001.10003220.102.1001",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 NORTH TUCKER CONDO UNIT 300  ",
      "condominium": true
    },
    {
      "unit_id": "10001.10003222.102.1001",
      "owner_id": "367",
      "description": "C.B. 0503 12TH ST 210 N TUCKER CONDO UNIT 302  ",
      "condominium": true
    }
  ]
}
</pre>

If you don't know the legal_entity_id of a person or business try looking it up by using the **/redb/legal_entity/name** endpoint first. :eyes:

## /redb/parcel/adddress
This endpoint returns a dictionary of lists which contain information about the parcel(s), building(s), and unit(s) related to a legal_entity_id.<br><br>
The address endpoint requires two inputs for a get request.<br>
- {AddressInput: str} - Input the address that you want to search the database for<br>
- {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>

The address end point uses trigrams and fuzzy matching in order to return all the information related to an address in the database that most closely matches the AddressInput.<br>
For example: **/redb/parcel/address?AddressInput=210%20N%20TUCKER%20BLVD&Current=True** will would currently return information on 39 different parcels that all use the same address of 210 N TUCKER BLVD  MO USA 63101.0 as well as all the current buildings and units associated with those parcels.  

## /redb/legal_entity/name
This endpoint returns a dictionary of lists which contain information about legal entities within the database based on a name.<br><br>
The name endpoint requires a single input for a get request.<br>
- {NameInput: str} - Input the legal_entity_name that you want to search the database for<br>

The name endpoint uses trigrams and fuzzy matching in order to return all of the legal entity records whose legal_entity_name field is similar to the NameInput.  The output returned by the end point is ordered such that the closest matches are listed first so being more specific should help you find the desired legal_entity faster.  Legal Names are entered in Lastname, Firstname format.

For example: **/redb/legal_entity/name?nameInput=Doug** would return the following:
<pre>
[
  {
    "legal_entity_id": 101450,
    "legal_entity_address": "4501 LINDELL BLVD UNIT 5 D",
    "legal_entity_name": "WEBER, DOUG",
    "legal_entity_secondary_name": null,
    "address_id": 212696
  },
  {
    "legal_entity_id": 26162,
    "legal_entity_address": "2103 MENARD ST",
    "legal_entity_name": "DOUG JO LLC",
    "legal_entity_secondary_name": null,
    "address_id": 132327
  }
]
</pre>
## /readb/filter/counts


## /readb/filter/ids

## /redb/latest
This endpoint returns a dictionary containing the date of the most recent update in redb.<br>
For example: If the database was most recently updated on 8/4/20 **.../redb/latest** would return

<pre>{
  "update_date": "2020-08-04"
}</pre>
