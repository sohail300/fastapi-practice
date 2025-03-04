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

