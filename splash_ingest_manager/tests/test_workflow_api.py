from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from mongomock import MongoClient
import pytest

from splash_ingest_manager.api import app, CreateJobRequest, CreateJobResponse
from ..auth_service import create_api_key, init_api_service
from ..ingest_service import init_ingest_service
from ..model import Job
from ..api import INGEST_JOBS_API, API_KEY_NAME


@pytest.fixture()
def client():
    client = TestClient(app)
    db = MongoClient().test_db
    init_api_service(db)
    init_ingest_service(db)
    return client


def test_create_job(client: TestClient):
    key = create_api_key('user1', 'sirius_cybernetics_gpp', INGEST_JOBS_API)
    request = CreateJobRequest(file_path="/foo/bar.hdf5", mapping_name="beamline_mappings", mapping_version="42")
    response: CreateJobResponse = client.post(url="/ingest_jobs", data=request.json(), headers={API_KEY_NAME: key})
    assert response.status_code == 200
    job_id = response.json()['job_id']

    response = client.get(url="/ingest_jobs/" + job_id)
    assert response.status_code == 403, 'ingest jobs wihtout api key'

    response = client.get(url="/ingest_jobs/" + job_id + "?" + API_KEY_NAME + "=" + key)
    job = Job(**response.json())
    assert job.document_path == "/foo/bar.hdf5"
