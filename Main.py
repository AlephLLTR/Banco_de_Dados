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

create_pages(100)
create_buckets(10)
store_keys()

print(f'Colisões: {Statistics.collisions * 100/DB.get_size() :.2f}%')
print(f'Overflow: {Statistics.overflow * 100/DB.get_size() :.2f}%')

START_TIME = time.time()
print(search_key_hash('2'))
END_TIME = time.time()
print(f'searchkeyhash: {(END_TIME - START_TIME):.6f}')



START_TIME = time.time()
print(table_search('2'))
END_TIME = time.time()
print(f'tablesearch: {(END_TIME - START_TIME) :.6f} ')


