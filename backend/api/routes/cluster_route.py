import logging as log
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from api.agents_api.records_api import delete_records_cluster
from api.agents_api.schemas.records_schema import RecordClusterDeletion
from db.repository.cluster import add_cluster_in_db, delete_cluster_from_db, get_all_clusters_from_db
from db.session import get_db
from core.configurations import user_identifier

router = APIRouter()

@router.get("/get_clusters")
async def get_clusters(db: Session = Depends(get_db)):
    try:
        clusters = get_all_clusters_from_db(db=db)

        return JSONResponse(content={"clusters": clusters}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error("Error on route get_clusters")
        log.error(e)
        raise e
    

@router.post("/add_cluster")
async def add_cluster(cluster_name: str, db: Session = Depends(get_db)):
    try:
        cluster = add_cluster_in_db(name=cluster_name, db=db)

        if cluster is None:
            return JSONResponse(content={"error": "Creation failed"}, status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse(content={"message": "Created Successfully"}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        log.error("Error on route add_cluster")
        log.error(e)
        raise e


@router.delete("/delete_cluster")
async def delete_cluster(cluster_id: int, db: Session = Depends(get_db)):
    try:
        is_cluster_deleted, cluster_name = delete_cluster_from_db(id=cluster_id, db=db)

        if is_cluster_deleted == False:
            return JSONResponse(content={"error": "Deletion failed"}, status_code=status.HTTP_400_BAD_REQUEST)
        else:
            data = RecordClusterDeletion(identifier=user_identifier, cluster_name=cluster_name)
            response = await delete_records_cluster(data=data)

            if response.status_code == 200:
                return JSONResponse(content={"message": "Deleted Successfully"}, status_code=status.HTTP_202_ACCEPTED)
            else:
                return JSONResponse(content={"message": "Deleted Successfully, but error on vectordb"}, status_code=status.HTTP_202_ACCEPTED)
    except Exception as e:
        log.error("Error on route delete_cluster")
        log.error(e)
        raise e


    
