from fastapi import FastAPI
import os
from dotenv import load_dotenv

from modules.chatbot.adapter.input.web.router.chatbot import router as chatbot_router

load_dotenv()
app = FastAPI()
app.include_router(chatbot_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    uvicorn.run(app, host=host, port=port)
