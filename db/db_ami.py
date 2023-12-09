from sqlalchemy.orm import Session
from fastapi import UploadFile
from io import StringIO
import csv
import pandas as pd
import io
from .models import Ami
from db.database import engine

async def upload_csv(file: UploadFile, db: Session):
    # 讀取 CSV 檔案
    content = await file.read()
    df_iter = pd.read_csv(io.StringIO(content.decode()), chunksize=10000)  # 每次處理 10000 行

    for df in df_iter:
        df.to_sql('ami', con=engine, if_exists='append', index=False, method='multi')

    db.close()

async def delete_all(db: Session):
    db.query(Ami).delete()
    db.commit()
    db.close()
