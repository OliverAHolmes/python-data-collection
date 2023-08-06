from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import db.db_internal as db_internal
from routers import column_constraint, column_definition, home, users, table_configurations

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(str(exc), status_code=400)

# CORS configuration
origins = [
    "http://0.0.0.0:8000",  # Adjust this as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    db_internal.create_db()

app.include_router(home.router, tags=["home"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(column_constraint.router, prefix="/constraints", tags=["constraints"])
app.include_router(column_definition.router, prefix="/columns", tags=["columns"])
app.include_router(table_configurations.router, prefix="/table-configurations", tags=["table-configurations"])
