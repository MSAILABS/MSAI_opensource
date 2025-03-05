from datetime import datetime
import os
import logging as log
import threading
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from router.base import api_router

# loading environment variables
load_dotenv()
# setting up logger
logger = log.getLogger(__name__)

def setup_logging(): 
    # Get the current date and time 
    current_time = datetime.now().strftime("date=%Y_%m_%d_time=%H_%M_%S")
    # Check if logs directory exists, if not, create it 
    if not os.path.exists("logs"): 
        os.makedirs("logs")

    log_filename = os.path.join("logs",f'agent_{current_time}.log')
    # Configure logging 
    log.basicConfig( 
        level=log.INFO, # Set the log level 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Format for the log messages 
        handlers=[ 
            log.FileHandler(log_filename), # Log messages to a file named bot.log 
            log.StreamHandler() # Also print log messages to the console 
        ] 
    ) 
    return log_filename

def db_initial_setup():
    env_dir = os.getenv("PROJECT_ENVIRONMENT") or "dev"

    if not os.path.exists(f"DB_FILES/{env_dir}"): 
        os.makedirs(f"DB_FILES/{env_dir}")

# this function has code for when application starts and shurdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # this code will run when application starts
    log.info('app Starting................')
    db_initial_setup()

    # test function
    # await RunTests()
    yield

    # this code will run when application shutdown
    log.info('app Shutting down................')

def application_setup():
    lfp = setup_logging()

    app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, title="MSAI Agents", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if lfp:
        log.info('Log has been setup at '+ os.path.abspath(lfp))

    app.include_router(api_router)

    return app

app = application_setup()

if __name__ == "__main__": 
    uvicorn.run("main:app", host="0.0.0.0", port=8000)