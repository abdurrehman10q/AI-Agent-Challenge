from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.exceptions import FraudDetectionException, fraud_exception_handler
from api.routes import health, transaction, feedback

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_exception_handler(FraudDetectionException, fraud_exception_handler)

app.include_router(health.router, prefix=settings.API_V1_PREFIX, tags=["Health"])
app.include_router(transaction.router, prefix=settings.API_V1_PREFIX, tags=["Transactions"])
app.include_router(feedback.router, prefix=settings.API_V1_PREFIX, tags=["Learning"])

@app.get("/")
def root():
    return {"message": "Fraud Detection API Running", "docs": "/docs"}