class Database:
    def __init__(self, path="words.txt"):
        self.path = path
        self.data = self.load_archive()

    def load_archive(self):
        """Carrega o arquivo de palavras."""
        try:
            with open(self.path, "r") as file:
                return file.read().split('\n')
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.path}' não encontrado.")
            return ""

    def get_size(self):
        """Retorna o tamanho dos dados carregados."""
        return len(self.data)

    def get_index(self, key: int) -> str:
        return self.data[key]
    
    def get_interval(self, start: int, end: int) -> list:
        return self.data[start:end]