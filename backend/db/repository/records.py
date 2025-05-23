import logging as log

from sqlalchemy.orm import Session
from sqlalchemy import func

from db.models.records import Records

def get_all_records_from_db(db: Session):
    try:
        records = db.query(Records).all()

        serialized_records = []

        for record in records:
            serialized_records.append({"id": record.id, "title": record.title, "description": record.description, "upload_date": record.upload_date.strftime("%Y-%m-%d %H:%M:%S"), "vectorized": record.vector_processed, "embedding_model": record.embedding_model})
        
        return serialized_records
    except Exception as e:
        log.error("Error on getting all records from database")
        log.error(e)
        return []
    
def get_records_count_from_db(db: Session):
    try:
        records_count = db.query(Records).count()
        return records_count
    except Exception as e:
        log.error("error on getting count of records from db")
        log.error(e)
        return 0
    
def get_record_by_id(record_id: int, db: Session):
    try:
        record = db.query(Records).filter(Records.id == record_id).first()
        return record
    except Exception as e:
        log.error("Error on getting record using record_id from database")
        log.error(e)
        return None


def mark_record_as_vectorized(record_id, embedding_model, db: Session):
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


def add_record_into_db(title: str, text: str, db: Session) -> Records | None:
    try:
        new_record = Records(
            title = title,
            description = text
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


def delete_record_from_db(record_id: int, db: Session):
    try:
        record = db.query(Records).filter(Records.id == record_id).first()
        db.delete(record)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        log.error("Error on deleting record from database")
        log.error(e)
        return False


def update_record_in_db(record_id: int, title: str, description: str, db: Session) -> bool:
    try:
        record = db.query(Records).filter(Records.id == record_id).first()
        if record:
            record.title = title
            record.description = description
            db.commit()
            return True
        else:
            log.error("Record not found")
            return False
    except Exception as e:
        db.rollback()
        log.error("Error on updating record in database")
        log.error(e)
        return False

