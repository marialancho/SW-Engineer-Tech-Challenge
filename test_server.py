import pytest
import sqlite3
from fastapi.testclient import TestClient
from server import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    init_db()
    yield
    conn = sqlite3.connect('dicom_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dicom_series')
    conn.commit()
    conn.close()

def test_store_dicom_series():
    series_data = {
        "SeriesInstanceUID": "2.25.265891057852514317505363974980016867097",
        "PatientID": "1",
        "PatientName": "Lehmann^Guido",
        "StudyInstanceUID": "2.25.195279363403791191586079347607892107643",
        "InstancesCount": 17
    }
    response = client.post("/store", json=series_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Series stored successfully"}

    response = client.post("/store", json=series_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Series already exists"}

def test_get_series():
    series_data = {
        "SeriesInstanceUID": "2.25.265891057852514317505363974980016867097",
        "PatientID": "1",
        "PatientName": "Lehmann^Guido",
        "StudyInstanceUID": "2.25.195279363403791191586079347607892107643",
        "InstancesCount": 17
    }
    client.post("/store", json=series_data)

    response = client.get("/series")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["SeriesInstanceUID"] == series_data["SeriesInstanceUID"]
    assert data[0]["PatientID"] == series_data["PatientID"]
    assert data[0]["PatientName"] == series_data["PatientName"]
    assert data[0]["StudyInstanceUID"] == series_data["StudyInstanceUID"]
    assert data[0]["InstancesCount"] == series_data["InstancesCount"]

def test_store_multiple_dicom_series():
    series_data_1 = {
        "SeriesInstanceUID": "2.25.265891057852514317505363974980016867097",
        "PatientID": "1",
        "PatientName": "Lehmann^Guido",
        "StudyInstanceUID": "2.25.195279363403791191586079347607892107643",
        "InstancesCount": 17
    }
    series_data_2 = {
        "SeriesInstanceUID": "2.25.879879856784564316877097879879856784564",
        "PatientID": "2",
        "PatientName": "Smith^John",
        "StudyInstanceUID": "2.25.584879879856784564316877097879856784564",
        "InstancesCount": 10
    }
    response = client.post("/store", json=series_data_1)
    assert response.status_code == 200
    assert response.json() == {"message": "Series stored successfully"}

    response = client.post("/store", json=series_data_2)
    assert response.status_code == 200
    assert response.json() == {"message": "Series stored successfully"}

    response = client.get("/series")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_series_empty_db():
    response = client.get("/series")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_store_invalid_data():
    series_data = {
        "SeriesInstanceUID": "2.25.265891057852514317505363974980016867097",
        "PatientID": "1",
        # Missing PatientName
        "StudyInstanceUID": "2.25.195279363403791191586079347607892107643",
        "InstancesCount": 17
    }
    response = client.post("/store", json=series_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_api_endpoints():
    response = client.get("/series")
    assert response.status_code == 200

    series_data = {
        "SeriesInstanceUID": "2.25.265891057852514317505363974980016867097",
        "PatientID": "1",
        "PatientName": "Lehmann^Guido",
        "StudyInstanceUID": "2.25.195279363403791191586079347607892107643",
        "InstancesCount": 17
    }
    response = client.post("/store", json=series_data)
    assert response.status_code == 200

def test_invalid_http_method():
    response = client.put("/store")
    assert response.status_code == 405  # Method Not Allowed
