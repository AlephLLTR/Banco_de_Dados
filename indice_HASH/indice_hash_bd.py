def h(value):
    return hash(value) % 10

bucket = [[None] * 2 for _ in range(10)]
print(bucket)

def hash_bucket(key, pagina):
    i = h(key)

    if bucket[i][0] == None:
        bucket[i][0] = {"key": key,
                        "pagina": pagina}
    elif bucket[i][1] == None:
        bucket[i][1] = {"key": key,
                        "pagina": pagina}
    else:
        # implementar overflow aqui
        print("overflow")

n_pag = int(input())

memoria = []
pagina = []

with open('words.txt', 'r') as arquivo:
    
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