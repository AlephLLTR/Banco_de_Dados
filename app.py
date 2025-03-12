from flask import Flask, render_template, request, jsonify
from Database import Database
from Bucket import Bucket
import Hash
import Statistics
import time
from math import ceil

app = Flask(__name__)

# Variáveis globais
DB = Database()
PAGE_LIST = []
BUCKET_LIST = []
setup_completed = False

def create_pages(keys_per_page: int):
    global PAGE_LIST
    PAGE_LIST = []
    try:
        total_pages = max(1, ceil(DB.get_size()/keys_per_page))
        for i in range(total_pages):
            start_idx = keys_per_page * i
            end_idx = min(start_idx + keys_per_page, DB.get_size())
            PAGE_LIST.append(DB.get_interval(start_idx, end_idx))
    except Exception as e:
        print(f"Erro ao criar páginas: {str(e)}")
        raise
    print(len(PAGE_LIST))

def create_buckets(keys_per_bucket: int):
    global BUCKET_LIST
    BUCKET_LIST = []
    try:
        total_buckets = max(1, ceil(DB.get_size()/keys_per_bucket))
        for i in range(total_buckets):
            BUCKET_LIST.append(Bucket(keys_per_bucket))
    except Exception as e:
        print(f"Erro ao criar buckets: {str(e)}")
        raise
def store_keys():
    try:
        total_keys = 0
        for page_index, page in enumerate(PAGE_LIST):
            for key in page:
                if key:  # Verifica se a chave não é vazia
                    total_keys += 1
                    hash_value = Hash.Hash_1(key, len(BUCKET_LIST))
                    BUCKET_LIST[hash_value].insert_reference(key, page_index)
        
        print(f"Total de chaves processadas: {total_keys}")
        print(f"Total de buckets: {len(BUCKET_LIST)}")
        print(f"Colisões: {Statistics.collisions}")
        print(f"Overflows: {Statistics.overflow}")
    except Exception as e:
        print(f"Erro ao armazenar chaves: {str(e)}")
        print(f"Tipo do erro: {type(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")
        raise

def search_key_hash(key: str):
    try:
        if not key:
            return None
        key_hash = Hash.Hash_1(key, len(BUCKET_LIST))
        return BUCKET_LIST[key_hash].get_key(key)
    except Exception as e:
        print(f"Erro na busca por hash: {str(e)}")
        return None

def table_search(key: str):
    try:
        if not key:
            return None, 0
        pages_read = 0
        for page_index, page in enumerate(PAGE_LIST):
            pages_read += 1
            for k in page:
                if k == key:
                    return page_index, pages_read
        return None, pages_read
    except Exception as e:
        print(f"Erro no table scan: {str(e)}")
        return None, 0

@app.route('/')
def index():
    return render_template('index.html', setup_completed=setup_completed)

@app.route('/setup', methods=['POST'])
def setup():
    global setup_completed
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados não fornecidos'}), 400

        # Reseta as estatísticas antes de iniciar o setup
        Statistics.reset()
        
        keys_pages = max(1, int(data.get('keys_pages', 1)))
        keys_buckets = max(1, int(data.get('keys_buckets', 1)))
        
        print(f"Iniciando setup com {keys_pages} tuplas por página e {keys_buckets} tuplas por bucket")
        
        create_pages(keys_pages)
        print(f"Total de páginas criadas: {len(PAGE_LIST)}")
        
        create_buckets(keys_buckets)
        print(f"Total de buckets criados: {len(BUCKET_LIST)}")
        
        store_keys()
        
        setup_completed = True
        
        return jsonify({
            'status': 'success',
            'message': 'Setup concluído com sucesso',
            'collisions': f'{Statistics.collisions * 100/DB.get_size():.2f}%',
            'overflow': f'{Statistics.overflow * 100/DB.get_size():.2f}%',
            'first_page': PAGE_LIST[0] if PAGE_LIST else [],
            'last_page': PAGE_LIST[-1] if PAGE_LIST else [],
            'total_pages': len(PAGE_LIST),
            'total_keys': DB.get_size()
        })
    except Exception as e:
        print(f"Erro no setup: {str(e)}")
        print(f"Tipo do erro: {type(e)}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/pages', methods=['GET'])
def get_pages():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if not PAGE_LIST:
            return jsonify({
                'status': 'error',
                'message': 'Sistema não inicializado'
            }), 400
            
        total_pages = len(PAGE_LIST)
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_pages)
        
        pages = []
        for i in range(start_idx, end_idx):
            pages.append({
                'page_number': i + 1,
                'content': PAGE_LIST[i]
            })
            
        return jsonify({
            'status': 'success',
            'current_page': page,
            'total_pages': total_pages,
            'per_page': per_page,
            'pages': pages
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados não fornecidos'}), 400

        key = data.get('key')
        if not key:
            return jsonify({'status': 'error', 'message': 'Chave de busca não fornecida'}), 400
        
        # Busca por hash
        start_time = time.time()
        hash_result = search_key_hash(key)
        hash_time = time.time() - start_time
        
        # Busca por table scan
        start_time = time.time()
        table_result, pages_read = table_search(key)
        table_time = time.time() - start_time
        
        if hash_result is not None:
            hash_result += 1
        if table_result is not None:
            table_result += 1
        
        return jsonify({
            'hash_result': hash_result,
            'table_result': table_result,
            'hash_time': f'{hash_time:.6f}',
            'table_time': f'{table_time:.6f}',
            'pages_read': pages_read
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 