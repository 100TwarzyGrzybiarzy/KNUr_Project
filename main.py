from fastapi import FastAPI
from database import engine
from schema.schema import Base
from schema import schema as db_schema
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

from routers.AuthRouter import router as AuthRouter
from routers.PharmacyWarehouseRouter import router as PharmacyWarehouseRouter
from routers.UserRouter import router as UserRouter
from routers.DrugRouter import router as DrugRouter



app = FastAPI(
    title="Pharmacy API",
    description="API for managing pharmacy resources, users, and drugs.",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(DrugRouter)
app.include_router(PharmacyWarehouseRouter)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Pharmacy API - Navigate to /docs for API documentation"}


