# TODO: Incluir qtd de páginas lidas


import time
from math import ceil
from Database import Database
from Bucket import Bucket
import Hash
import Statistics
DB: Database = Database()

PAGE_LIST: list[list] = []
BUCKET_LIST: list[Bucket] = []

def create_pages(keys_per_page: int):
    total_pages = ceil(DB.get_size()/keys_per_page)
    for i in range(total_pages):
        PAGE_LIST.append(DB.get_interval(keys_per_page*i, keys_per_page*i+keys_per_page))

def create_buckets(keys_per_bucket: int):
    total_buckets = ceil(DB.get_size()/keys_per_bucket)
    for i in range(total_buckets):
        BUCKET_LIST.append(Bucket(keys_per_bucket))

def store_keys():
    for page in PAGE_LIST:
        for key in page:
            hash_value = Hash.Hash_1(key, len(BUCKET_LIST))
            BUCKET_LIST[hash_value].insert_reference(key, PAGE_LIST.index(page))

def search_key_hash(key: str):
    key_hash = Hash.Hash_1(key, len(BUCKET_LIST))
    return BUCKET_LIST[key_hash].get_key(key)

def table_search(key: str):
    for page in PAGE_LIST:
        for k in page:
            if k == key:
                return PAGE_LIST.index(page)
    return None


def execute_setup():
    print(f'Inicializando Banco de Dados')
    keys_pages: int = int(input('Quantas páginas? '))
    keys_buckets: int = int(input('Quantos buckets? '))
    create_pages(keys_pages)
    create_buckets(keys_buckets)
    store_keys()
    executeCMD()

def executeCMD():
    RUNNING: bool = True
    while RUNNING:
        
        print(f'''Database
Colisões: [{Statistics.collisions * 100/DB.get_size() :.2f}%]
Overflow: [{Statistics.overflow * 100/DB.get_size() :.2f}%]


1 - Buscar por Hash
2 - Buscar por Table
3 - Sair''')

        menu_option: int = int(input('Selecione uma opção. '))
        if menu_option == 1:
            key: str = input('HASH SEARCH: Qual chave você deseja obter? ')
            
            START_TIME = time.time()
            print(search_key_hash(key))
            
            END_TIME = time.time()
            print(f'Tempo total do HASH SEARCH: {(END_TIME - START_TIME):.6f} ')
            executeCMD()

        elif menu_option == 2:
            key: str = input('TABLE SEARCH: Qual chave você deseja obter? ')

            START_TIME = time.time()
            print(table_search(key))
            
            END_TIME = time.time()
            print(f'Tempo total do TABLE SEARCH: {(END_TIME - START_TIME):.6f} ')
            executeCMD()
        
        elif menu_option == 3:
            RUNNING = False
            print('Encerrando...')
        
execute_setup()



# palavra = 'Alan'

# create_pages(100)
# create_buckets(10)
# store_keys()

# print(f'Colisões: {Statistics.collisions * 100/DB.get_size() :.2f}%')
# print(f'Overflow: {Statistics.overflow * 100/DB.get_size() :.2f}%')

# START_TIME = time.time()
# print(search_key_hash(palavra))
# END_TIME = time.time()
# print(f'searchkeyhash: {(END_TIME - START_TIME):.6f}')



# START_TIME = time.time()
# print(table_search(palavra))
# END_TIME = time.time()
# print(f'tablesearch: {(END_TIME - START_TIME) :.6f} ')