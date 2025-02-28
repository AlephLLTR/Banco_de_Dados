def h(value):
    return hash(value) % 10

cont_overflow = 0
def overflow(bucket, key, pagina):
    global cont_overflow
    cont_overflow += 1
    bucket.append({"key": key,
                   "pagina": pagina})
    bucket.append(None)


bucket = [[None] * 2 for _ in range(10)]
print(bucket)

def hash_bucket(key, pagina):
    i = h(key)

    for j in range(len(bucket[i])):
        if bucket[i][j] == None:
            bucket[i][j] = {"key": key,
                            "pagina": pagina}
            break

        elif j == len(bucket[i]) - 1:
            overflow(bucket[i], key, pagina)

n_pag = int(input())

memoria = []
pagina = []

with open('indice_HASH/words.txt', 'r') as arquivo:
    
    for linha in arquivo:
        
        pagina.append(linha.strip())

        if len(pagina) == n_pag:
            memoria.append(pagina)
            pagina = []
    
    if pagina:
        memoria.append(pagina)

print(memoria)
print("-"*100, "\n")

for i in range(len(memoria)):
    for j in range(len(memoria[i])):
        hash_bucket(memoria[i][j], i)

print(bucket)

print("Overflow: ", cont_overflow, "\n")

while True:
    word = input("procure por uma palavra: ")

    index = h(word)  
    bucket_atual = bucket[index]  

    if bucket_atual:
        for item in bucket_atual:
            if item and item.get("key") == word: 
                print(item["pagina"])  
                break
    else:
        print("Bucket vazio ou inexistente.")