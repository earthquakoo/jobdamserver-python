from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.user.router import router as user_router
from src.presentation.chat_room.router import router as chat_room_router
from src.infrastructure.database import Base, engine
from src.exceptions.handler import base_custom_exception_handler
from src.exceptions.base_exceptions import BaseCustomException

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(chat_room_router)
app.add_exception_handler(BaseCustomException, base_custom_exception_handler)


@app.get("/")
def health_check():
    return {"message": "I'm doing fine, thanks for asking"}
