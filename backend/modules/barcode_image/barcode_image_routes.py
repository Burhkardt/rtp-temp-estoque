from flask import jsonify, Blueprint, request
from backend.utils.barcode_by_image import read_image_and_delete

bar_up_bp = Blueprint("barcodeup", __name__)

@bar_up_bp.route("/upload", methods=['POST'])
def upload_barcode():
    # 1. Validações iniciais do arquivo enviado
    if 'barcode_image' not in request.files:
        return jsonify({'error': 'Nenhum arquivo recebido pelo servidor'}), 400
    
    file = request.files['barcode_image']
    if file.filename == '':
        return jsonify({'error': 'Nome do arquivo vazio'}), 400
    
    # 2. Define o caminho onde a imagem vai ser salva temporariamente
    # Usamos o próprio nome original do arquivo (file.filename) para ser dinâmico
    caminho_salvamento = f"backend/utils/temp_barcode/{file.filename}"
    
    # 3. Salva o arquivo no disco
    file.save(caminho_salvamento)
    
    # 4. Chama a sua função passando o caminho dinâmico do arquivo que acabou de ser salvo
    codigos_extraidos = read_image_and_delete(caminho_salvamento)
    
    # 5. Verifica se algum código foi de fato encontrado
    if not codigos_extraidos:
        return jsonify({
            'status': 'erro', 
            'message': 'Nenhum código de barras válido foi detectado na imagem.'
        }), 422 # Código 422 significa que o arquivo foi recebido, mas os dados eram ilegíveis
    
    # 6. Retorna o sucesso e a lista de códigos de volta para o JavaScript do Frontend
    return jsonify({
        'status': 'sucesso',
        'codigos': codigos_extraidos
    }), 200