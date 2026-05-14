import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

def generate_barcode(data: str, code_type: str = "code128") -> str:
    """Gera um código de barras e retorna como base64"""
    try:
        BARCODE_CLASS = barcode.get_barcode_class(code_type)
        rv = BytesIO()
        code = BARCODE_CLASS(data, writer=ImageWriter())
        code.write(rv)
        
        img_str = base64.b64encode(rv.getvalue()).decode("utf-8")
        return img_str
    except Exception as e:
        print(f"Erro ao gerar código de barras: {e}")
        return None
