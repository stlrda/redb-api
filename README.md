# Currently Implemented Routes

## /redb/parcel/redb_id
This endpoint returns json of lists which contain information about the parcel(s), building(s), and unit(s) related to a parcel id.<br><br>
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
This endpoint returns json of lists which contain information about the parcel(s), building(s), and unit(s) related to a legal_entity_id.<br><br>
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
This endpoint returns json of lists which contain information about the parcel(s), building(s), and unit(s) related to a street address.<br><br>
The address endpoint requires two inputs for a get request.<br>
- {AddressInput: str} - Input the address that you want to search the database for<br>
- {Current: bool} - True returns only current data, False returns all data and includes the current_flag field in the output<br>

The address end point uses trigrams and fuzzy matching in order to return all the information related to an address in the database that most closely matches the AddressInput.<br>
For example: **.../redb/parcel/address?AddressInput=10140%20LOOKAWAY%20DR&Current=True** would return the following:
<pre>
{
  "parcels": [
    {
      "parcel_id": "10001.10136990.000.0000",
      "county_id": "10001",
      "address": "10140 LOOKAWAY DR  MO USA 63137.0",
      "city_block_number": "9119.0",
      "parcel_number": "10136990",
      "owner_id": "10415",
      "description": "O. L. 119 RIVERVIEW DR. 75FT/79FT 11IN X 365FT/337FT RIVERVIEW ADDN. LOT 5  ",
      "frontage_to_street": 0,
      "land_area": 26950,
      "zoning_class": "A",
      "ward": "2",
      "voting_precinct": "3",
      "inspection_area": "2",
      "neighborhood_id": "73",
      "police_district": "6",
      "census_tract": "1270.0",
      "asr_neighborhood": "337",
      "special_parcel_type": null,
      "sub_parcel_type": null,
      "gis_city_block": "9119.0",
      "gis_parcel": "60.0",
      "gis_owner_code": "0",
      "create_date": "2020-08-04",
      "current_flag": true
    }
  ],
  "buildings": [],
  "units": []
}
</pre>

:warning: User beware :warning:<br>
The information provided by the city is not the most consistant at this time and this is especially true for parcel addresses.  For example were you to search for /redb/parcel/address?AddressInput=10140%20LOOKAWAY%20**DRIVE**&Current=True you would get no results.  It is an address within the database but is is associated with a legal entity rather than a parcel.  To a person it is obvious these should be the same address but to the database they are distinct which makes searching by address less reliable than using legal_id or parcel_id.

## /redb/legal_entity/name
This endpoint returns json of lists which contain information about legal entities within the database based on a name.<br><br>
The name endpoint requires a single input for a get request.<br>
- {NameInput: str} - Input the legal_entity_name that you want to search the database for<br>

The name endpoint uses trigrams and fuzzy matching in order to return all of the legal entity records whose legal_entity_name field is similar to the NameInput.  The output returned by the end point is ordered such that the closest matches are listed first so being more specific should help you find the desired legal_entity faster.  Legal Names are entered in Lastname, Firstname format.

For example: **.../redb/legal_entity/name?nameInput=Doug** would return the following:
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
This endpoint returns json which contain counts of the commercial use and residential use buildings located on parcels that match the selected criteria.<br><br>
The counts endpoint requires two inputs for a get request.<br>
- {FilterTypeInput: str} - The field you would like to filter on<br>
- {FilterValueInput: str} - The value of the filter field you want to filter on<br>

For example: **.../redb/filter/counts?FilterTypeInput=voting_precinct&FilterValueInput=4** would return the following:
<pre>
[
  {
    "building_use": "COM",
    "count": 198
  },
  {
    "building_use": "RES",
    "count": 1103
  }
]</pre>

The acceptable criteria for the FileTypeInput field are as follows:<br>
[zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]<br>

## /readb/filter/ids
This endpoint returns json which contain the parcel_ids of all the parcels that match the selected criteria.<br><br>
The ids endpoint requires two inputs for a get request.<br>
- {FilterTypeInput: str} - The field you would like to filter on<br>
- {FilterValueInput: str} - The value of the filter field you want to filter on<br>

For example: **.../redb/filter/ids?FilterTypeInput=inspection_area&FilterValueInput=3** would return the following:

<pre>
[
  {
    "parcel_id": "10001.10003754.000.0000"
  },
  {
    "parcel_id": "10001.10000140.000.0000"
  },
  {
    "parcel_id": "10001.10003516.000.0000"
  },
  {
    "parcel_id": "10001.10006542.000.0000"
  },
  {
    "parcel_id": "10001.10000388.000.0000"
  },
  {
    "parcel_id": "etc..."
  }
]
</pre>

The acceptable criteria for the FileTypeInput field are as follows:<br>
[zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]<br>

## /redb/latest
This endpoint returns json containing the date of the most recent update in redb.<br>
For example: If the database was most recently updated on 8/4/20 **.../redb/latest** would return the following:

<pre>{
  "update_date": "2020-08-04"
}</pre>
