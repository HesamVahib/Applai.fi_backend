from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import jobs

app = FastAPI()

origins = [
    "http://localhost",
    "https://applai-fi.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(jobs.router)