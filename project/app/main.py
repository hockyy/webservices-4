import random

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

async def get_npm_function(npm: str, session: AsyncSession) -> MahasiswaResponse:
    try:
        result = await session.execute(select(Mahasiswa).where(Mahasiswa.npm == npm))
        mahasiswa = result.scalars().one()
        mahasiswa = MahasiswaResponse(nama=mahasiswa.nama, npm=mahasiswa.npm, status=f"OK {random.randint(1, 1000000000)}")
    except:
        mahasiswa = MahasiswaResponse(status="Not Found", npm=npm, nama="")
    return mahasiswa

@app.get("/{npm}", response_model=MahasiswaResponse)
async def get_mahasiswa_npm(npm: str, session: AsyncSession = Depends(get_session)):
    return await get_npm_function(npm, session)


@app.get("/{npm}/{trx_id}", response_model=MahasiswaResponse)
async def get_mahasiswa_npm(npm: str, trx_id: str, session: AsyncSession = Depends(get_session)):
    before_append = await get_npm_function(npm, session)
    before_append.status += f"-{str(trx_id)}"
    return before_append

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)