import Statistics

class Bucket:
    def __init__(self, size):
        self.size: int = size
        self.references: dict = {}
        self.OVERFLOW = None

    def insert_reference(self, key: str, value: int):
        if len(self.references) == self.size: #Estamos checando se há uma colisão, aqui ocorre uma colisão
            #Aqui acontece uma COLISÃO
            Statistics.collisions += 1
            if self.OVERFLOW:
                # Se já existir um OVERFLOW, só insere a referência
                self.OVERFLOW.insert_reference(key, value)
            else:
                Statistics.overflow += 1
                # Aqui acontece um OVERFLOW, logo vamos criar um novo bucket em self.OVERFLOW e então vamos armazenar a referência lá 
                self.OVERFLOW = Bucket(self.size)
                self.OVERFLOW.insert_reference(key, value)
        else:
            # Caso haja espaço
            self.references[key] = value

    def get_key(self, key: str):
        for k in self.references:
            if k == key:
                return self.references[key]
        if self.OVERFLOW:
            return self.OVERFLOW.get_key(key)
        return None
        