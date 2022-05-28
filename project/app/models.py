from typing import Optional

from pydantic.main import BaseModel
from sqlmodel import SQLModel, Field

class Mahasiswa(SQLModel, table=True):
    npm: str = Field(default=None, primary_key=True)
    nama: str = Field(nullable=False)

class MahasiswaCreate(Mahasiswa):
    pass

class MahasiswaResponse(Mahasiswa):
    status: str = "OK"

class UpdateResponse(BaseModel):
    status: str = "OK"