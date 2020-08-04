# Currently Implemented Routes

## /redb/parcel/redb_id
This endpoint returns a dictionary of lists which contain information about the parcel(s), building(s), and unit(s) related to a parcel id<br><br>
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
## /redb/parcel/adddress

## /redb/legal_entity/name

## /readb/filter/counts
## /readb/filter/ids

## /redb/latest
