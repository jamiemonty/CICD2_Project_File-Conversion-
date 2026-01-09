import pytest
from fastapi import HTTPException
from app.services.convertor import convert_file

class FakeUploadFile:
    def __init__(self, filename, data=b"hello"):
        self.filename = filename
        self._data = data

    async def read(self):
        return self._data

@pytest.mark.asyncio
async def test_rejects_unsupported_input():
    f = FakeUploadFile("file.pdf")
    with pytest.raises(HTTPException):
        await convert_file(f, "txt", False, False)