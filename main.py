# API for St Louis Crime DB
import sqlalchemy
import databases
import json

from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends, BackgroundTasks
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

## Version 2.0 Endpoints ##
# Redirect Root to Docs
@app.get('/')
async def get_api_docs():
    response = RedirectResponse(url='/redoc')
    return response
    
# Parcel Endpoints?!
@app.get('/parcel', response_model=List[ParcelTest])
async def parcel_test():
    query = f'SELECT * FROM "core"."parcel" LIMIT 100'
    return await database.fetch_all(query=query)

# Get a specificVar
@app.get('/parcel/{specificVar}', response_model=parcel_specific)
async def crime_points(specificVar: str):
    query = f'SELECT * FROM "core"."parcel" WHERE parcel_id = :specific AND current_flag = true'
    values = {'specific': specificVar}
    return await database.fetch_one(query=query, values=values)

@app.get('/legal_entity/{nameInput}', response_model=List[legal_entity_name])
async def find_name(nameInput: str):
    query = f'SELECT * FROM "core"."legal_entity" WHERE SIMILARITY(legal_entity_name, :name) > 0.4'
    values = {'name': nameInput}
    return await database.fetch_all(query=query, values=values)


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