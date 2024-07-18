from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class SeriesData(BaseModel):
    SeriesInstanceUID: str
    PatientID: str
    PatientName: str
    StudyInstanceUID: str
    InstancesCount: int

def init_db():
    conn = sqlite3.connect('dicom_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dicom_series (
        SeriesInstanceUID TEXT PRIMARY KEY,
        PatientID TEXT,
        PatientName TEXT,
        StudyInstanceUID TEXT,
        InstancesCount INTEGER
    )''')
    conn.commit()
    cursor.execute('DELETE FROM dicom_series')
    conn.commit()
    conn.close()

@app.post("/store")
async def store_series(series: SeriesData):
    conn = sqlite3.connect('dicom_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO dicom_series VALUES (?, ?, ?, ?, ?)', (
            series.SeriesInstanceUID,
            series.PatientID,
            series.PatientName,
            series.StudyInstanceUID,
            series.InstancesCount
        ))
        conn.commit()
        return {"message": "Series stored successfully"}
    except sqlite3.IntegrityError:
        return {"message": "Series already exists"}
    finally:
        conn.close()

@app.get("/series")
async def get_series():
    conn = sqlite3.connect('dicom_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dicom_series')
    rows = cursor.fetchall()
    conn.close()
    return [SeriesData(
        SeriesInstanceUID=row[0],
        PatientID=row[1],
        PatientName=row[2],
        StudyInstanceUID=row[3],
        InstancesCount=row[4]
    ) for row in rows]


if __name__ == "__main__":
    import uvicorn
    init_db()  # Ensure the database is initialized when running directly
    uvicorn.run(app, host="0.0.0.0", port=8000)