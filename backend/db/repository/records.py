import logging as log

from sqlalchemy.orm import Session

from db.models.records import Records

def get_all_records_from_db(db: Session):
    try:
        records = db.query(Records).all()

        serialized_records = []

        for record in records:
            serialized_records.append({"id": record.id, "title": record.title, "description": record.description, "upload_date": record.upload_date.strftime("%Y-%m-%d %H:%M:%S")})
        
        return serialized_records
    except Exception as e:
        log.error("Error on getting all records from database")
        log.error(e)
        return []

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

