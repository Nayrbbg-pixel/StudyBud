from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import sqlite3

app = FastAPI()
app.add_middleware(

    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["GET"],
    allow_credentials = True

)

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

async def process_and_store_data(data1:str,data2:str)->None:
    cursor.execute('INSERT INTO data VALUES(?,?)',(data1,data2))
    conn.commit()

async def get_processed_data(id:int):
    try:
        cursor.execute(f"SELECT * FROM data WHERE rowid = ?",(str(id)))
        val = cursor.fetchall()
        return {'data1':val[0][0],'data2':val[0][1]}
    
    except:
        return {"error":"data does not exist!"}

class Data(BaseModel):
    data1 : Optional[str] = None
    data2 : str

@app.post('/post-data/')
async def post_data(Data:Data)->None:
    await process_and_store_data(Data.data1,Data.data2)
    return {Data}

@app.get('/get-data/{id}')
async def get_data(id:int,):
    value = await get_processed_data(id)
    return value

conn.commit()