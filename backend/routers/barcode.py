from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database.remote_db import get_remote_db
from modules.barcode.generator import generate_barcode
from modules.barcode.reader import read_barcode

router = APIRouter(prefix="/barcode", tags=["barcode"])

@router.get("/generate/{data}")
def generate(data: str):
    barcode_base64 = generate_barcode(data)
    if not barcode_base64:
        raise HTTPException(status_code=500, detail="Erro ao gerar código de barras")
    return {"data": data, "barcode_base64": barcode_base64}

@router.get("/generate-from-db/{record_id}")
def generate_from_db(record_id: int, db: Session = Depends(get_remote_db)):
    # Simula a leitura de um banco remoto (somente leitura)
    data_to_encode = f"{record_id}" # Simplified for barcode compatibility
    barcode_base64 = generate_barcode(data_to_encode)
    
    if not barcode_base64:
        raise HTTPException(status_code=500, detail="Erro ao gerar código de barras do banco")
        
    return {"record_id": record_id, "barcode_base64": barcode_base64}

@router.post("/read")
async def read(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
        
    content = await file.read()
    decoded_data = read_barcode(content)
    
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Não foi possível ler o código de barras")
        
    return {"decoded_data": decoded_data}
