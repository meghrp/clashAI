"""
ClashAI MVP - FastAPI Backend
Main entry point for the FastAPI application.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import player, advice

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="ClashAI API",
    description="AI-powered Clash of Clans player advice API",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(player.router, prefix="/api", tags=["player"])
app.include_router(advice.router, prefix="/api", tags=["advice"])


@app.get("/")
async def root():
    return {"message": "ClashAI API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
