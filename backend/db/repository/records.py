import logging as log
from typing import Literal

from sqlalchemy.orm import Session

from db.models.cluster import Cluster
from db.models.records import Records

def get_all_records_from_db(cluster_id: int, db: Session) -> list:
    try:
        records = db.query(Records).filter(Records.cluster_id == cluster_id).all()

        serialized_records = []

        for record in records:
            serialized_records.append({"id": record.id, "title": record.title, "description": record.description, "upload_date": record.upload_date.strftime("%Y-%m-%d %H:%M:%S"), "vectorized": record.vector_processed, "embedding_model": record.embedding_model})
        
        return serialized_records
    except Exception as e:
        log.error("Error on getting all records from database")
        log.error(e)
        return []
    
def get_records_count_from_db(db: Session) -> int:
    try:
        records_count = db.query(Records).count()
        return records_count
    except Exception as e:
        log.error("error on getting count of records from db")
        log.error(e)
        return 0
    
def get_record_by_id(record_id: int, db: Session) -> tuple[Records | None, Cluster | None] | None:
    try:
        record = db.query(Records).filter(Records.id == record_id).first()
        cluster = db.query(Cluster).filter(Cluster.id == record.cluster_id).first()
        
        return record, cluster
    except Exception as e:
        log.error("Error on getting record using record_id from database")
        log.error(e)
        return None


def mark_record_as_vectorized(record_id, embedding_model, db: Session) -> None | Records:
    try:
        record = db.query(Records).filter(Records.id == record_id).first()

        if not record:
            log.warning(f"Record with ID {record_id} not found.")
            return None

        record.vector_processed = True
        record.embedding_model = embedding_model
        db.commit()
        db.refresh(record)  # Ensures updated state is returned
        return record
    except Exception as e:
        db.rollback()  # Ensure rollback on failure
        log.error("Error on updating record vector_processed flag using record_id from database")
        log.error(e)
        return None


def add_record_into_db(title: str, text: str, cluster_id: int, db: Session) -> Records | None:
    try:
        cluster = db.query(Cluster).filter(Cluster.id == cluster_id).first()

        if cluster is None:
            log.error(f"Error on adding new record in database, Cluster not found on id: {cluster_id}")
            return None

        new_record = Records(
            title = title,
            description = text,
            cluster_id = cluster_id
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    except Exception as e:
        db.rollback()
        log.error("Error on adding new record in database")
        log.error(e)
        return None


def delete_record_from_db(record_id: int, db: Session) -> tuple[Literal[True], Cluster | None] | tuple[Literal[False], None]:
    try:
        record = db.query(Records).filter(Records.id == record_id).first()
        cluster = db.query(Cluster).filter(Cluster.id == record.cluster_id).first()
        db.delete(record)
        db.commit()
        return True, cluster
    except Exception as e:
        db.rollback()
        log.error("Error on deleting record from database")
        log.error(e)
        return False, None


def update_record_in_db(record_id: int, title: str, description: str, db: Session) -> tuple[Literal[True], Cluster | None] | tuple[Literal[False], None]:
    try:
        record = db.query(Records).filter(Records.id == record_id).first()
        cluster = db.query(Cluster).filter(Cluster.id == record.cluster_id).first()
        if record:
            record.title = title
            record.description = description
            db.commit()
            return True, cluster
        else:
            log.error("Record not found")
            return False, None
    except Exception as e:
        db.rollback()
        log.error("Error on updating record in database")
        log.error(e)
        return False, None

