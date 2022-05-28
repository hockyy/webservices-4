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


@app.get("/", response_model=list[Mahasiswa])
async def get_mahasiswa(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Mahasiswa))
    mahasiswa = result.scalars().all()
    return mahasiswa


@app.get("/{npm}", response_model=MahasiswaResponse)
async def get_mahasiswa_npm(npm: str, session: AsyncSession = Depends(get_session)):

    try:
        result = await session.execute(select(Mahasiswa).where(Mahasiswa.npm == npm))
        mahasiswa = result.scalars().one()
    except:
        mahasiswa = MahasiswaResponse(status="Not Found", npm=npm, nama="")
    return mahasiswa

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)