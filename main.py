# API for Regional Entity Database
import sqlalchemy
import databases
import json

from datetime import date
from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse

# DB connection information in local gitignored file
from config import DATABASE_URL

# import the base models
from models.models import *

## Load Database Configuration ##
database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Allow All CORS
app = FastAPI(title='REDB API', docs_url="/redb/docs", redoc_url="/redb/redoc", openapi_url="/redb/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=['*'])

## Connect to DB on Startup and disconnect on Shutdown ##
@app.on_event('startup')
async def startup():
    await database.connect()
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

# Redirect Root to Docs 
@app.get('/redb')
async def get_api_docs():
    response = RedirectResponse(url='/redb/redoc')
    return response

## PARCEL ENDPOINTS!! ##
# Get a ParcelId
@app.get('/redb/parcel/redb_id', response_model=ParcelInfo)
async def Find_Parcel_By_REDB_Id(ParcelInput: str, Current: bool):

    values = {'ParcelId': ParcelInput}
    if Current == True:
        current_flag_select = ''
        current_flag_where = 'AND current_flag = TRUE'
    else:
        current_flag_select = ', current_flag'
        current_flag_where = ''

    query_parcels = f'''SELECT parcel_id
                        , county_id
                        , address_id
                        , city_block_number
                        , parcel_number
                        , owner_id
                        , description
                        , frontage_to_street
                        , land_area
                        , zoning_class
                        , ward
                        , voting_precinct
                        , inspection_area
                        , neighborhood_id
                        , police_district
                        , census_tract
                        , asr_neighborhood
                        , special_parcel_type.special_parcel_type
                        , sub_parcel_type.sub_parcel_type
                        , gis_city_block
                        , gis_parcel
                        , gis_owner_code
                        {current_flag_select}
                    FROM "core"."parcel" 
                    LEFT JOIN "core"."special_parcel_type"
                    ON COALESCE("special_parcel_type"."special_parcel_type_code", 'null') = COALESCE("parcel"."special_parcel_type_code", 'null')
                    LEFT JOIN "core"."sub_parcel_type"
                    ON COALESCE("sub_parcel_type"."sub_parcel_type_code", 'null') = COALESCE("parcel"."sub_parcel_type_code", 'null')
                    WHERE parcel_id = :ParcelId
                    {current_flag_where}'''
    
    query_buildings = f'''SELECT building_id
                        , owner_id
                        , description
                        , building_use
                        , apartment_count
                        {current_flag_select}
                    FROM "core"."building" 
                    WHERE CONCAT(SUBSTRING(building_id FROM 1 FOR 14), \'.000.0000\') = :ParcelId
                    {current_flag_where}'''
    
    query_units = f'''SELECT unit_id
                        , owner_id
                        , description
                        , condominium
                        {current_flag_select}
                    FROM "core"."unit" 
                    WHERE CONCAT(SUBSTRING(unit_id FROM 1 FOR 14), \'.000.0000\') = :ParcelId
                    {current_flag_where}'''

    parcel_info_dict = await database.fetch_all(query=query_parcels, values=values)
    building_info_dict = await database.fetch_all(query=query_buildings, values=values)
    unit_info_dict = await database.fetch_all(query=query_units, values=values)

    combined_dict = {'parcels':parcel_info_dict,'buildings':building_info_dict,'units':unit_info_dict}
    return combined_dict

@app.get('/redb/parcel/legal_entity_id', response_model=ParcelInfo)
async def Find_Parcels_By_Legal_Entity_Id(IdInput: str, Current:bool):
    
    values = {'Legal_Entity_Id': IdInput}

    if Current == True:
        current_flag_select = ''
        current_flag_where = 'AND current_flag = TRUE'
    else:
        current_flag_select = ', current_flag'
        current_flag_where = ''

    query_parcels = f'''SELECT parcel_id
                        , county_id
                        , address_id
                        , city_block_number
                        , parcel_number
                        , owner_id
                        , description
                        , frontage_to_street
                        , land_area
                        , zoning_class
                        , ward
                        , voting_precinct
                        , inspection_area
                        , neighborhood_id
                        , police_district
                        , census_tract
                        , asr_neighborhood
                        , special_parcel_type.special_parcel_type
                        , sub_parcel_type.sub_parcel_type
                        , gis_city_block
                        , gis_parcel
                        , gis_owner_code
                        {current_flag_select}
                    FROM "core"."parcel" 
                    LEFT JOIN "core"."special_parcel_type"
                    ON COALESCE("special_parcel_type"."special_parcel_type_code", 'null') = COALESCE("parcel"."special_parcel_type_code", 'null')
                    LEFT JOIN "core"."sub_parcel_type"
                    ON COALESCE("sub_parcel_type"."sub_parcel_type_code", 'null') = COALESCE("parcel"."sub_parcel_type_code", 'null')
                    WHERE owner_id = :Legal_Entity_Id
                    {current_flag_where}'''
    
    query_buildings = f'''SELECT building_id
                        , owner_id
                        , description
                        , building_use
                        , apartment_count
                        {current_flag_select}
                        FROM core.building 
                        WHERE owner_id = :Legal_Entity_Id
                        {current_flag_where}
                        ORDER BY building.building_id'''
    
    query_units = f'''SELECT unit_id
                        , owner_id
                        , unit.description
                        , condominium
                        {current_unit_flag_select}
                        FROM core.unit 
                        WHERE owner_id = :Legal_Entity_Id
                        {current_flag_where}'''

    parcel_info_dict = await database.fetch_all(query=query_parcels, values=values)
    building_info_dict = await database.fetch_all(query=query_buildings, values=values)
    unit_info_dict = await database.fetch_all(query=query_units, values=values)

    combined_dict = {'parcels':parcel_info_dict,'buildings':building_info_dict,'units':unit_info_dict}
    return combined_dict


@app.get('/redb/parcel/address', response_model=ParcelInfo)
async def Find_Parcels_By_Address(AddressInput: str, Current: bool):
    """This route returns parcel data for a given address. The parcel data includes
    parcel(s) from the "core.parcel" table as well as each building and unit associated with
    said parcel(s).

    The following logic goes as follows:
        Fetch parcel data for given address.
        Assign fetched parcel_ids, current_flags, and create_dates to variables.
        Fetch buildings and units that correspond to each parcel's parcel_id, current_flag, and create date.
        Return a dictionary containing a list of each parcel, building, and unit related to given address.

    Filtering buildings and units by a given parcel's parcel_id, current_flag, and create date is to ensure
    that the buildings and units correspond to the exact instance of the parcel. parcel_id alone is not
    sufficient because a parcel with an updated address and thus multiple instances of the same parcel_id
    can have buildings and units that correspend to that instance specifically, but not to previous instances.
    If we're assuming that only one instance of a parcel_id appears in parcels on a given date, the current_flag
    and create_date will distinguish the buildings and units that only correspond to the parcel_id from the
    buildings and units that also correspond to the given address.
    """

    values = {'address': AddressInput}
    address_subquery = '''
                        (
                        SELECT
                            address_id
                        FROM "core"."address"
                        WHERE
                            SIMILARITY(CONCAT(street_address, ' ', county_id, ' ', city, ' ', address.state, ' ', country, ' ', zip), :address) > 0.4
                        ORDER BY
                            WORD_SIMILARITY(CONCAT(street_address, ' ', county_id, ' ', city, ' ', address.state, ' ', country, ' ', zip), :address) DESC
                        LIMIT 1
                        )
                        '''
    parcel_where = f'WHERE p.address_id = {address_subquery} AND p.current_flag = TRUE' if Current else f'WHERE p.address_id = {address_subquery}'

    query_parcels = f'''
                    SELECT 
                        p.parcel_id
                        , p.county_id
                        , CONCAT(a."street_address", ' ', a."city", ' ', a."state", ' ', a."country", ' ', a."zip") as address
                        , p.city_block_number
                        , p.parcel_number
                        , p.owner_id
                        , p.description
                        , p.frontage_to_street
                        , p.land_area
                        , p.zoning_class
                        , p.ward
                        , p.voting_precinct
                        , p.inspection_area
                        , p.neighborhood_id
                        , p.police_district
                        , p.census_tract
                        , p.asr_neighborhood
                        , special_parcel_type.special_parcel_type
                        , sub_parcel_type.sub_parcel_type
                        , p.gis_city_block
                        , p.gis_parcel
                        , p.gis_owner_code
                        , p.create_date
                        , p.current_flag
                    FROM "core"."parcel" p
                    LEFT JOIN "core"."special_parcel_type"
                        ON COALESCE("special_parcel_type"."special_parcel_type_code", 'null') = COALESCE(p."special_parcel_type_code", 'null')
                    LEFT JOIN "core"."sub_parcel_type"
                        ON COALESCE("sub_parcel_type"."sub_parcel_type_code", 'null') = COALESCE(p."sub_parcel_type_code", 'null')
                    JOIN "core"."address" a
                        ON p."address_id" = a."address_id"
                    {parcel_where}
                    ;
                    '''

    parcels_fetch = await database.fetch_all(query=query_parcels, values=values)
    parcel_ids = [parcel['parcel_id'] for parcel in parcels_fetch]
    parcel_ids_and_current_flags = [parcel['parcel_id'] + str(parcel["current_flag"]).lower() for parcel in parcels_fetch]
    parcel_create_dates = [parcel['create_date'].strftime("%Y-%m-%d") for parcel in parcels_fetch]

    if Current:
        buildings_where = f'WHERE "current_flag" = True AND "parcel_id" = ANY(ARRAY{parcel_ids})'
        units_where = f'WHERE u."current_flag" = True AND "parcel_id" = ANY(ARRAY{parcel_ids})'
    else:
        buildings_where = f'''
                            WHERE
                                CONCAT("parcel_id", "current_flag"::text) = ANY(ARRAY{parcel_ids_and_current_flags})
                            AND CAST("create_date" as VARCHAR) = ANY(ARRAY{parcel_create_dates})
                          '''             
        units_where = f'''
                        WHERE
                            CONCAT(p."parcel_id", u."current_flag"::text) = ANY(ARRAY{parcel_ids_and_current_flags})
                        AND CAST(u."create_date" as VARCHAR) = ANY(ARRAY{parcel_create_dates})
                      '''

    query_buildings = f'''
                        SELECT 
                            building_id
                            , owner_id
                            , description
                            , building_use
                            , apartment_count
                            , create_date
                            , current_flag
                        FROM "core"."building"
                        {buildings_where}
                        ;
                        '''
    
    query_units = f'''
                    SELECT 
                        u.unit_id
                        , u.owner_id
                        , u.description
                        , u.condominium
                        , u.create_date
                        , u.current_flag
                    FROM "core"."unit" u
                    JOIN "core"."parcel" p
                        ON SUBSTRING(u."unit_id" FROM 1 FOR 14) = SUBSTRING(p."parcel_id" FROM 1 FOR 14)
                    {units_where}
                    ;
                    '''

    parcel_info_list = parcels_fetch
    building_info_list = await database.fetch_all(query=query_buildings)
    unit_info_list = await database.fetch_all(query=query_units)

    parcels_by_address_dict = {'parcels':parcel_info_list, 'buildings':building_info_list, 'units':unit_info_list}
    return parcels_by_address_dict

## Filter parcels ##
# Return counts of bus/res buildings by filter#
@app.get('/redb/filter/counts', response_model = List[FilterParcelCounts])
async def Building_Counts_By_Filter(FilterTypeInput: str, FilterValueInput: str):

    values = {'FilterValue': FilterValueInput}
    allowedFliters = ['zoning_class', 'ward', 'voting_precinct', 'inspection_area', 'neighborhood_id', 'police_district', 'census_tract']

    if FilterTypeInput in allowedFliters:
        query = f'''SELECT DISTINCT building_use, COUNT(*)
                    FROM core.building
                    JOIN (SELECT parcel_id, {FilterTypeInput} FROM core.parcel WHERE {FilterTypeInput} = :FilterValue AND current_flag = TRUE) Parcel_Filter
                    ON Parcel_Filter.parcel_id = building.parcel_id
                    GROUP BY building_use
                    HAVING "building_use" IN ('COM','RES')
                    '''
        building_counts = await database.fetch_all(query=query, values=values)        
        return building_counts
    else:
        raise HTTPException(status_code=400, detail='Unsupported filter. Please use one of the following: [zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]')

# Return all current parcel ids by filter #
@app.get('/redb/filter/ids', response_model = List[FilterParcelIds])
async def Building_IDs_By_Filter(FilterTypeInput: str, FilterValueInput: str):

    values = {'FilterValue': FilterValueInput}
    allowedFliters = ['zoning_class', 'ward', 'voting_precinct', 'inspection_area', 'neighborhood_id', 'police_district', 'census_tract']

    if FilterTypeInput in allowedFliters:
            query = f'''SELECT DISTINCT parcel_id 
                    FROM core.parcel 
                    WHERE {FilterTypeInput} = :FilterValue 
                    AND current_flag = TRUE'''
            parcelIDs = await database.fetch_all(query=query, values=values)        
            return parcelIDs
    else:
        raise HTTPException(status_code=400, detail='Unsupported filter. Please use one of the following: [zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract]')

## LEGAL_ENTITY ENDPOINTS! ##
@app.get('/redb/legal_entity/name', response_model=List[LegalEntityName])
async def Find_Legal_Entity_Id(nameInput: str):
    query = f'''SELECT * 
                FROM "core"."legal_entity"
                WHERE SIMILARITY(legal_entity_name, :name) > 0.4
                ORDER BY WORD_SIMILARITY("legal_entity_name", :name) DESC'''
    values = {'name': nameInput}
    legal_entities = await database.fetch_all(query=query, values=values)
    return legal_entities

## LAST UPDATE ENDPOINT! ##
@app.get('/redb/latest')
async def Find_Latest_Update():
    query = '''WITH LATEST_UPDATE AS
            (
                SELECT MAX("update_date") as "update_date" FROM "core"."neighborhood"
                UNION
                SELECT MAX("update_date") as "update_date" FROM  "core"."address"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."county_id_mapping_table"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."legal_entity"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."parcel"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."building"
                UNION
                SELECT MAX("update_date") as "update_date" FROM "core"."unit"
            )
            SELECT MAX("update_date") as "update_date" FROM LATEST_UPDATE'''
    return await database.fetch_one(query=query)


## Modify API Docs ##
# TODO address ERROR: api_docs() missing 1 required positional argument: 'openapi_prefix' when adding "openapi_prefix" param.
def api_docs():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='Regional Entity Database',
        version='0.1.0',
        description='Automatically Updated, land parcel data from Saint Louis, provided by the St. Louis Regional Data Alliance .<br><br>If you\'d prefer to interact with queries in browser, see the <a href=\'/docs\'>Swagger UI</a>',
        routes=app.routes,#[13:], # Need to Verify this to Obfuscate Some Routes from Docs
        #openapi_prefix=openapi_prefix
    )
    openapi_schema['info']['x-logo'] = {
        'url' : 'https://stldata.org/wp-content/uploads/2019/06/rda-favicon.png' # Need a more permanent source
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = api_docs()

