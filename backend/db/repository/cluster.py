import logging as log

from sqlalchemy.orm import Session

from db.models.cluster import Cluster
from db.models.records import Records


def get_all_clusters_from_db(db: Session):
    try:
        clusters = db.query(Cluster).all()

        data = []

        for cluster in clusters:
            data.append({
                "id": cluster.id,
                "name": cluster.title
            })
        
        return data
    except Exception as e:
        log.error("Error on get_all_clusters_from_db")
        log.error(e)
        return []
    

def add_cluster_in_db(name: str, db: Session):
    try:
        new_cluster = Cluster(title = name)
        db.add(new_cluster)
        db.commit()
        db.refresh(new_cluster)
        return new_cluster
    except Exception as e:
        db.rollback()
        log.error("Error on add_cluster_in_db")
        log.error(e)
        return None
    

def delete_cluster_from_db(id: int, db: Session):
    try:
        deleted_records_count = db.query(Records).filter(Records.cluster_id == id).delete()
        cluster = db.query(Cluster).filter(Cluster.id == id).first()
        cluster_name = cluster.title

        deleted_cluster_count = db.query(Cluster).filter(Cluster.id == id).delete()

        db.commit()

        if (deleted_cluster_count > 0):
            return True, cluster_name
        else:
            return False, None

    except Exception as e:
        db.rollback()
        log.error("Error on delete_cluster_from_db")
        log.error(e)
        return False, None
