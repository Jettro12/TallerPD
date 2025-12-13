"""
Simple FastAPI backend that exposes a Hello World endpoint.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    Root endpoint that returns Hello World.
    
    Returns:
        dict: A dictionary containing the Hello World message
    """
    return {"message": "Memento mori, memento vivere"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
