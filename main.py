# API for St Louis Crime DB
import sqlalchemy
import databases
import json

# DB connection information in local gitignored file
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

# import the base models
from models.Parcel import *
from models.Building import *
from models.Unit import *

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

## Legacy Endpoints ##
# Necessary Until the Deprecation of Current Dashboard
@app.get('/legacy/latest', response_model=LegacyCrimeLatest)
async def legacy_latest():
    query = "SELECT crime_last_update FROM update"
    return await database.fetch_one(query=query)

## Version 2.0 Endpoints ##

# Redirect Root to Docs
@app.get('/')
async def get_api_docs():
    response = RedirectResponse(url='/redoc')
    return response

# Get Latest Date
@app.get('/latest', response_model=CrimeLatest)
async def latest_data():
    query = "SELECT (date_trunc('month', crime_last_update::date) + interval '1 month' - interval '1 day')::date AS latest FROM update;"
    return await database.fetch_one(query=query)

# Get Point Level Coordinates
@app.get('/crime/', response_model=List[CrimePoints])
async def crime_points(start: date, end: date, category: str):
    query = "SELECT id, lon, lat FROM crime WHERE count = true AND date >= :start AND date <= :end AND LOWER(category) = LOWER(:category);"
    values = {'start': start, 'end': end, 'category': category}
    return await database.fetch_all(query=query, values=values)

@app.get('/crime/detailed', response_model=List[CrimeDetailed])
async def crime_detailed(start: date, end: date, category: str):
    query = "SELECT id, date, time, description, lon, lat FROM crime WHERE count = true AND date >= :start AND date <= :end AND LOWER(category) = LOWER(:category);"
    values = {'start': start, 'end': end, 'category': category}
    return await database.fetch_all(query=query, values=values)

# Get Geometric Aggregations
@app.get('/crime/{geometry}', response_model=List[CrimeAggregate])
async def crime_aggregate(start: date, end: date, geometry: str, category: str):
    geometry = geometry.lower()
    category = category.lower()
    if geometry == 'neighborhood':
        query = "SELECT neighborhood AS region, SUM(CASE WHEN count THEN 1 END) as count FROM crime WHERE date >= :start AND date <= :end AND LOWER(category) = :category GROUP BY neighborhood;"
    elif geometry == 'district':
        query = "SELECT district AS region, SUM(CASE WHEN count THEN 1 END) as count FROM crime WHERE date >= :start AND date <= :end AND LOWER(category) = :category GROUP BY district;"
    else:
        raise HTTPException(status_code=400, detail='Unsupported Geometry. Try one of "neighborhood" or "district"')
    values = {'start': start, 'end': end, 'category': category}
    # Need to find and implement geometries, geojson, type checking model and feature collection response
    # Can also consolidate query here
    return await database.fetch_all(query=query, values=values)

# Get Temporal Aggregations
# @app.get('crime/trends')
# async def crime_trends(start: str, end: str, interval: str, category: list, correct: bool, total: bool):
#     # Interval should be one of days, weeks, months, years
#     # Correct Specifies whether to apply seasonal correction
#     # Total Specifies whether to just get a total count (i.e. total of all categories in a single month)
#     # Need to Figure out Postgres for Time Series
#     return None

# Download Entire Research Files
# @app.get('crime/download')
# async def crime_download(start: date, end: date, category: Optional[str] = 'all'):
#     # Can we automatically export this as a CSV? Figure out pydantic models
#     return None

## Modify API Docs ##
def api_docs(openapi_prefix: str):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='St. Louis Crime',
        version='0.1.0',
        description='Automatically Updated, Clean Crime Data from the Saint Louis Metropolitan Police Department, provided by the St. Louis Regional Data Alliance in partnership with the Insititute for Public Health at Washington University.<br><br>If you\'d prefer to interact with queries in browser, see the <a href=\'/docs\'>Swagger UI</a>',
        routes=app.routes,#[13:], # Need to Verify this to Obfuscate Some Routes from Docs
        openapi_prefix=openapi_prefix
    )
    openapi_schema['info']['x-logo'] = {
        'url' : 'https://stldata.org/wp-content/uploads/2019/06/rda-favicon.png' # Need a more permanent source
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = api_docs