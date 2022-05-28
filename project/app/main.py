from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models import Mahasiswa, MahasiswaCreate, MahasiswaResponse, UpdateResponse
import uvicorn

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.post("/")
async def add_mahasiswa(mahasiswa: MahasiswaCreate, session: AsyncSession = Depends(get_session)):
    try:
        mahasiswa = Mahasiswa(npm=mahasiswa.npm, nama=mahasiswa.nama)
        session.add(mahasiswa)
        await session.commit()
        await session.refresh(mahasiswa)
        return UpdateResponse()
    except Exception as e:
        return UpdateResponse(status=f"Internal Server Error {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)