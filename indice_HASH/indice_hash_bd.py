import time
import math

class Page:
    def __init__(self, number, records):
        self.number = number
        self.records = records

    def __str__(self):
        return f"Página {self.number}: {self.records}"


class Bucket:
    def __init__(self, size):
        self.size = size  
        self.entries = [None] * size  
        self.overflow = []           

    def insert(self, key, page_number):
        collision = any(e is not None for e in self.entries)
        for i in range(self.size):
            if self.entries[i] is None:
                self.entries[i] = {"key": key, "page": page_number}
                return collision, False
        self.overflow.append({"key": key, "page": page_number})
        return collision, True


class HashIndex:
    def __init__(self, num_buckets, bucket_size):
        self.num_buckets = num_buckets  # NB
        self.bucket_size = bucket_size  # FR
        self.buckets = [Bucket(bucket_size) for _ in range(num_buckets)]
        self.total_collisions = 0
        self.total_overflows = 0

    def hash_function(self, key):
        return hash(key) % self.num_buckets

    def insert(self, key, page_number):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        collision, overflow_event = bucket.insert(key, page_number)
        if collision:
            self.total_collisions += 1
        if overflow_event:
            self.total_overflows += 1

    def search(self, key):
  
        index = self.hash_function(key)
        bucket = self.buckets[index]
        cost = 1  

        for entry in bucket.entries:
            cost += 1
            if entry is not None and entry["key"] == key:
                return entry, cost
        for entry in bucket.overflow:
            cost += 1
            if entry["key"] == key:
                return entry, cost
        return None, cost

def load_data(file_path):

    try:
        with open(file_path, 'r') as f:
            data = [line.strip() for line in f if line.strip()]
        print(f"[INFO] Arquivo '{file_path}' carregado com {len(data)} registros.")
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar o arquivo: {e}. Usando dataset de demonstração.")
        data = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    return data

def build_pages(data, page_size):

    pages = []
    total_records = len(data)
    num_pages = math.ceil(total_records / page_size)
    for i in range(num_pages):
        start = i * page_size
        end = start + page_size
        page = Page(i, data[start:end])
        pages.append(page)
    print(f"[INFO] Dados divididos em {len(pages)} páginas (tamanho de página = {page_size}).")
    if pages:
        print("[INFO] Primeira página:", pages[0])
        print("[INFO] Última página:", pages[-1])
    return pages

def build_index(pages, bucket_size):

    NR = sum(len(page.records) for page in pages)
    FR = bucket_size
    NB = math.ceil(NR / FR) + 1 
    index = HashIndex(NB, FR)
    for page in pages:
        for record in page.records:
            index.insert(record, page.number)
    print(f"[INFO] Índice construído com {NB} buckets. Total de registros: {NR}")
    print(f"[INFO] Total de colisões: {index.total_collisions}, Total de overflows: {index.total_overflows}")
    return index

def search_with_index(index, key):

    start_time = time.time()
    result, cost = index.search(key)
    elapsed = time.time() - start_time
    return result, cost, elapsed

def table_scan(pages, key):

    start_time = time.time()
    pages_scanned = 0
    found_page = None
    for page in pages:
        pages_scanned += 1
        if key in page.records:
            found_page = page
            break
    elapsed = time.time() - start_time
    return found_page, pages_scanned, elapsed


def main():
    data_file = "indice_HASH/words.txt"  
    try:
        page_size = int(input("Informe o tamanho da página (número de registros por página): "))
    except Exception:
        page_size = 50
        print(f"[INFO] Valor inválido. Usando tamanho da página = {page_size}")

    try:
        bucket_size = int(input("Informe o tamanho do bucket (número de registros por bucket): "))
    except Exception:
        bucket_size = 2
        print(f"[INFO] Valor inválido. Usando tamanho do bucket = {bucket_size}")

    data = load_data(data_file)
    pages = build_pages(data, page_size)

    index = build_index(pages, bucket_size)

    NR = len(data)
    collision_rate = (index.total_collisions / NR) * 100 if NR else 0
    overflow_rate = (index.total_overflows / NR) * 100 if NR else 0
    print(f"Taxa de colisões: {collision_rate:.2f}%")
    print(f"Taxa de overflows: {overflow_rate:.2f}%\n")

    while True:
        key = input("Digite a chave para busca (ou 'sair' para encerrar): ").strip()
        if key.lower() == "sair":
            break

        result_index, cost_index, time_index = search_with_index(index, key)
        if result_index:
            print(f"[ÍNDICE] Chave '{key}' encontrada na página {result_index['page']} (custo: {cost_index} acessos, tempo: {time_index:.6f}s)")
        else:
            print(f"[ÍNDICE] Chave '{key}' não encontrada (custo: {cost_index} acessos, tempo: {time_index:.6f}s)")

        found_page, pages_scanned, time_scan = table_scan(pages, key)
        if found_page:
            print(f"[TABLE SCAN] Chave '{key}' encontrada na página {found_page.number} (páginas lidas: {pages_scanned}, tempo: {time_scan:.6f}s)")
        else:
            print(f"[TABLE SCAN] Chave '{key}' não encontrada (páginas lidas: {pages_scanned}, tempo: {time_scan:.6f}s)")

        diff = time_scan - time_index
        print(f"Diferença de tempo (Table Scan - Índice): {diff:.6f}s\n")


main()
