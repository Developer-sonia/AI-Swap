from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="AI-Swap API",
    description="Professional face swapping application API",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Swap API",
        "version": "1.0.0",
        "status": "running",
        "note": "Basic deployment test - working!"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-swap-api"}

@app.get("/test")
async def test():
    """Simple test endpoint"""
    return {"message": "API is working!", "test": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 