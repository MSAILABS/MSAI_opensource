from pydantic import BaseModel


class RecordData(BaseModel):
    record_id: int
    record_description: str
    record_title: str
    record_upload_date: str
    identifier: str
    cluster_name: str

class RecordDataDelete(BaseModel):
    record_id: int
    identifier: str
    cluster_name: str


class RecordDataQuery(BaseModel):
    query: str
    identifer: str
    cluster_name: str


class RecordClusterDeletion(BaseModel):
    identifier: str
    cluster_name: str
