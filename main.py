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
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

# import the base models
from models.parcel import *
from models.building import *
from models.unit import *
from models.legal_entity import *

## Load Database Configuration ##
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Allow All CORS
app = FastAPI(title='REDB API')
app.add_middleware(CORSMiddleware, allow_origins=['*'])

## Connect to DB on Startup and disconnect on Shutdown ##
@app.on_event('startup')
async def startup():
    await database.connect()
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

# Redirect Root to Docs 
@app.get('/')
async def get_api_docs():
    response = RedirectResponse(url='/redoc')
    return response

## PARCEL ENDPOINTS!! ##
# Get a ParcelId
@app.get('/parcel', response_model=SingleParcelInfo)
async def Parcel_Search(ParcelInput: str, Current: bool):

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

#Filter parcels
@app.get('/filter', response_model = List[FilterParcels])
async def Building_Types_By_Filter(FilterTypeInput: str, FilterValueInput: str):

    values = {'FilterValue': FilterValueInput}
    allowedFliters = ['zoning_class', 'ward', 'voting_precinct', 'inspection_area', 'neighborhood_id', 'police_district', 'census_tract']

    if FilterTypeInput in allowedFliters:
        query = f'''SELECT DISTINCT building_use, COUNT(*)
                    FROM core.building
                    JOIN (SELECT parcel_id, {FilterTypeInput} FROM core.parcel WHERE {FilterTypeInput} = :FilterValue) Parcel_Filter
                    ON Parcel_Filter.parcel_id = building.parcel_id
                    GROUP BY building_use
                    HAVING "building_use" IN ('COM','RES')
                    '''

        building_counts = await database.fetch_all(query=query, values=values)        
        return building_counts
    else:
        raise HTTPException(status_code=400, detail='Unsupported filter. Try one of the following zoning_class, ward, voting_precinct, inspection_area, neighborhood_id, police_district, census_tract')

## LEGAL_ENTITY ENDPOINTS! ##
@app.get('/legal_entity/{nameInput}', response_model=List[LegalEntityName])
async def Find_Legal_Entity_Id(nameInput: str):
    query = f'''SELECT * 
                FROM "core"."legal_entity" 
                WHERE SIMILARITY(legal_entity_name, :name) > 0.4'''
    values = {'name': nameInput}
    legal_entities = await database.fetch_all(query=query, values=values)
    return legal_entities

## LAST UPDATE ENDPOINT! ##
@app.get('/latest')
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



# @app.get('/crime/detailed', response_model=List[CrimeDetailed])
# async def crime_detailed(start: date, end: date, category: str):
#     query = "SELECT id, date, time, description, lon, lat FROM crime WHERE count = true AND date >= :start AND date <= :end AND LOWER(category) = LOWER(:category);"
#     values = {'start': start, 'end': end, 'category': category}
#     return await database.fetch_all(query=query, values=values)

# ## Modify API Docs ##
# def api_docs(openapi_prefix: str):
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title='St. Louis Crime',
#         version='0.1.0',
#         description='Automatically Updated, Clean Crime Data from the Saint Louis Metropolitan Police Department, provided by the St. Louis Regional Data Alliance in partnership with the Insititute for Public Health at Washington University.<br><br>If you\'d prefer to interact with queries in browser, see the <a href=\'/docs\'>Swagger UI</a>',
#         routes=app.routes,#[13:], # Need to Verify this to Obfuscate Some Routes from Docs
#         openapi_prefix=openapi_prefix
#     )
#     openapi_schema['info']['x-logo'] = {
#         'url' : 'https://stldata.org/wp-content/uploads/2019/06/rda-favicon.png' # Need a more permanent source
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = api_docs

if __name__ == "__main__":
    app.run()