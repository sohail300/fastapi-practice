# IMPORT STATEMENTS
# FastAPi framework to create APIs
from fastapi import FastAPI

# Pydantic for data conversion and dta validation
from pydantic import BaseModel

# We can create fields of Database models using this
from tortoise import fields

# Used to create models
from tortoise.models import Model

# Used to create pydantic models from tortoise models
from tortoise.contrib.pydantic import pydantic_model_creator

# Used to register tortoise
from tortoise.contrib.fastapi import register_tortoise

import requests # used to fetch data from external APIs

app = FastAPI() # Initialise FastAPI application

# DATABASE MODEL
# Defines a database model for storing city details using tortoise orm
class City(Model):
    id = fields.IntField(primary_key= True)
    name = fields.CharField(max_length= 50, unique=True)
    timezone = fields.CharField(max_length= 50)

    # Computed field that is not stored in the database
    def current_time(self) -> str:
        response = requests.get('/')
        current_time = response.json()['datetime']
        return current_time

    # It ensures that current_time is included in the serialized responses as well as in the Pydantic model even if it is not in the database. 
    class PydanticMeta:
        computed = ('current_time', )

# PYDANTIC MODEL
# Create Pydantic model from ORM model

# Used for response serialization
# includes all DB fields as well as computed fields
City_Pydantic = pydantic_model_creator(City, name= 'City')

# Used for request validation
# excludes readonly fields like id and current_time
CityIn_Pydantic = pydantic_model_creator(City, name='CityIn', exclude_readonly=True)

@app.get('/')
def index():
    return {'key' : 'value'}

@app.get('/cities')
async def get_cities():
    return await City_Pydantic.from_queryset(City.all())

@app.get('/cities/{city_id}')
async def get_city(city_id: int):
    return await City_Pydantic.from_queryset_single(City.get(id=city_id))

@app.post('/cities')
async def create_city(city: CityIn_Pydantic):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)

@app.delete('/cities/{city_id}')
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
    return {}

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)