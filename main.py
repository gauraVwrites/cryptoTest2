import requests as rq
import json
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker as sql_session
from datetime import datetime as dt
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("KEY")
db_url = os.getenv("DB_URL")

# get today's top 10 then store them in a container to use them later on for the rest of the project 
# def top10(key):
#     endpoint = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
#     parameters = {
#        'start':1,
#        'limit':20,
#        'sort':'cmc_rank'
#     }
#     headers = {
#        'Accepts': 'application/json',
#        'X-CMC_PRO_API_KEY': key,
#        'Accept-Encoding': 'deflate'
#     }
#     session = rq.Session()
#     session.headers.update(headers)

#     response = session.get(endpoint, params=parameters)
#     data = json.loads(response.text)
#     return data

# k = top10(key)['data']
# top = []
# storing IDs in a list that is sorted already on the basis of CMC rank

# for i in k:
#    top.append(i['id'])

# loading them again and getting other related information for them to make a dimension table
# this table will hold metadata information for our top 10

# def metadata(id, key):
#     endpoint = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
#     parameters = {
#         'id':id,
#     }
#     headers = {
#         'Accepts':'application/json',
#         'X-CMC_PRO_API_KEY':key,
#         'Accept-Encoding':'deflate'
#     }
#     session = rq.Session()
#     session.headers.update(headers)

#     response = session.get(endpoint, params= parameters)
#     data = json.loads(response.text)

#     return data

# logos = []
# ids = []
# names = []
# symbols = []
# slugs = []
# dates = []
# tags = []
# categories = []
# descriptions = []
# for i in top:
#     data = metadata(i, key)['data'][str(i)]
#     logos.append(data['logo'])
#     ids.append(data['id'])
#     names.append(data['name'])
#     symbols.append(data['symbol'])
#     slugs.append(data['slug'])
#     dates.append(data['date_launched'])
#     categories.append(data['category'])
#     descriptions.append(data['description'])
#     tags.append(data['tags'][0])

# data = {
#     'id':ids,
#     'name':names,
#     'symbol':symbols,
#     'slug':slugs,
#     'category':categories,
#     'tags':tags,
#     'logo':logos,
#     'description':descriptions
# }

# this dataframe holds basic information about today's top 10 cryptoCurrencies, on the basis of CMC rank
# df = pd.DataFrame(data)
# if data:
#     print(f"DataFrame created Successfully")
# else:
#     print(f"Error in creating Dataframe")

# 1. create engine to connect
engine = create_engine(db_url, echo= True)
# 2. creating a session maker
SessionLocal = sql_session(bind= engine)
# 3. defining Base Class
Base = declarative_base()
# defining base table top10
class tableTop10(Base):
    __tablename__ = 'top10'
    
    #defining the structure of table
    id = Column('id', Integer, primary_key= True)
    name = Column('name', String)
    symbol = Column('symbol', String)
    slug = Column('slug', String)
    category = Column('category', String)
    tags = Column('tags', String)
    logo = Column('logo', String)
    description = Column('description', String)

    def __init__(self, id, name, symbol, slug, category, tags, logo, description):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.slug = slug
        self.category = category
        self.tags = tags
        self.logo = logo
        self.description = description
    
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.symbol}, {self.slug}, {self.category}, {self.tags}, {self.logo}, {self.description})"
    
# Create a Session to work around the data
session_sql = SessionLocal()

# Insert data into table by creating instances like this:

# for index, rows in df.iterrows():
#     currencyInfo = tableTop10(rows['id'], rows['name'], rows['symbol'], rows['slug'], rows['category'], rows['tags'], rows['logo'], rows['description'])
#     session_sql.add(currencyInfo)

# session_sql.commit()

ids  = session_sql.query(tableTop10.id).all()

idString = ''
idList = []
for i in range(len(ids)):
    idList.append(str(ids[i][0]))
    if i != len(ids)-1:
        idString += str(ids[i][0])+','
    else:
        idString += str(ids[i][0])



# creating a new table in our postgresql table that is hosted in cloud
# understanding structure of this table
# [id(integer,pkey), name(string), symbol(string), slug(string), category(string), tags(string), logo(string), description(log)]


def quotes(key, id):
    endpoint = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'id':id
    }
    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':key,
        'Accept-Encoding':'deflate'
    }
    session = rq.Session()
    session.headers.update(headers)

    response = session.get(endpoint, params= parameters)
    data = json.loads(response.text)
    return data

# converted the time, and its same, if late then, by 1-3 mins


# the data availabe regarding dates is stored in Zulu Timezone, we need to conver this into Indian TimeZone
def convert_to_datetime(k):
    dateTime = dt.fromisoformat(k.replace('Z', '+00:00'))
    timeZone = pytz.timezone("Asia/Kolkata")
    dateTime = dateTime.astimezone(timeZone)
    return dateTime

# understanding quotes
# in documentation it was stated that we can send multiple ids by seperating them with column
# we've already created one in previous step, it will be very efficient for us if in one call we can get info for all 10, with a cost of 1

data = quotes(key, idString)['data']
price = []
id1 = [] #stores ids in integer
marketCap = []
lastUpdated = []
date = []


for i in idList:
    p = data[i]
    id1.append(p['id']) #appending ids to id1 as integers
    price.append(p['quote']['USD']['price'])
    marketCap.append(p['quote']['USD']['market_cap_dominance'])
    lastUpdated.append(convert_to_datetime(p['last_updated']))

data = {
    'id':id1,
    'price':price,
    'market_cap':marketCap,
    'last_updated':lastUpdated
}

df = pd.DataFrame(data)

# now we'll create a new table object onto which we'll feed this dataframe intervally later on
class dynamicTable(Base):
    __tablename__ = 'mainTable'
    
    #defining the structure of table
    id = Column('id', Integer)
    price = Column('price', Numeric(10,3))
    market_cap = Column('market_cap', Numeric(10,3))
    last_updated = Column('last_updated', DateTime)
    rowNum = Column('rowNum', Integer, primary_key= True, autoincrement= True)

    def __init__(self, id, price, market_cap, last_updated):
        self.id = id
        self.price = price
        self.market_cap = market_cap
        self.last_updated = last_updated
    
    def __repr__(self):
        return f"({self.id}, {self.price}, {self.market_cap}, {self.last_updated})"

# Create Table Only If not Exists
Base.metadata.create_all(engine)

# Adding data to the table
for index, rows in df.iterrows():
    currencyInfo = dynamicTable(rows['id'], rows['price'], rows['market_cap'], rows['last_updated'])
    session_sql.add(currencyInfo)

session_sql.commit()

# close the session
session_sql.close()