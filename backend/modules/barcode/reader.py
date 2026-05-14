from pyzbar.pyzbar import decode
from PIL import Image
import io

def read_barcode(image_bytes: bytes) -> str:
    """Lê um código de barras a partir de bytes de imagem"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        decoded_objects = decode(image)
        
        if not decoded_objects:
            return None
            
        # Retorna o primeiro código encontrado
        return decoded_objects[0].data.decode("utf-8")
    except Exception as e:
        print(f"Erro ao ler código de barras: {e}")
        return None
