from fastapi import FastAPI
from routers import Esp32
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.include_router(Esp32.router)

#if __name__ == "__main__":
#   uvicorn.run(app, host="192.168.74.125", port=5000)