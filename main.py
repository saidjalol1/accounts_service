from fastapi import FastAPI


from api.v1 import api as v1_api

Application = FastAPI(title="Users Service")

Application.include_router(v1_api.router, prefix="/api/v1", tags=["v1"])
