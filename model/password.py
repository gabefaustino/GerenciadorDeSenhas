# Importa as bibliotecas necessárias
from datetime import datetime
from pathlib import Path

# Classe base para outras classes que representam "tabelas no banco de dados"
# Esta classe fornece métodos comuns, como `save` e `get`, para persistência de dados
class BaseModel:
    # Define o diretório base do projeto e o diretório de banco de dados
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    # Método `save` salva os dados da instância em um arquivo de texto
    def save(self):
        # Define o caminho do arquivo com o nome da classe, simulando uma tabela
        table_path = Path(self.DB_DIR / f'{self.__class__.__name__}.txt')
        
        # Cria o arquivo, caso ele não exista
        if not table_path.exists():
            table_path.touch()
        
        # Abre o arquivo em modo de anexação (append) e escreve os dados da instância
        with open(table_path, 'a') as arq:  # modo a = append -> adiciona ao conteúdo existente
            arq.write("|".join(list(map(str, self.__dict__.values()))))  # Converte os valores dos atributos para string e junta com "|"
            arq.write('\n')  # Insere uma nova linha após cada registro

    # Método de classe `get` para recuperar todos os registros salvos
    @classmethod
    def get(cls):
        # Define o caminho do arquivo, baseado no nome da classe
        table_path = Path(cls.DB_DIR / f'{cls.__name__}.txt')

        # Cria o arquivo se ele não existir (para evitar erros ao tentar abrir)
        if not table_path.exists():
            table_path.touch()
        
        # Lê o conteúdo do arquivo
        with open(table_path, 'r') as arq:  # modo r = read
            x = arq.readlines()  # Lê todas as linhas do arquivo, onde cada linha representa um registro
        
        results = []  # Lista para armazenar cada registro como um dicionário
        atributos = vars(cls()).keys()  # Obtém os nomes dos atributos da classe para facilitar o mapeamento

        # Itera sobre cada linha para converter em dicionário
        for i in x:
            split_v = i.strip().split('|')  # Divide os valores da linha pelo separador "|"
            tmp_dict = dict(zip(atributos, split_v))  # Mapeia os atributos aos valores de cada linha
            results.append(tmp_dict)  # Adiciona o dicionário à lista de resultados

        return results  # Retorna todos os registros como uma lista de dicionários

# Classe Password herda de BaseModel, ganhando os métodos `save` e `get`
class Password(BaseModel):
    # Inicializa os atributos de uma nova instância de Password
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain  # Domínio associado à senha (ex: nome do site ou app)
        self.password = password  # A senha em si
        self.create_at = datetime.now().isoformat()  # Data e hora da criação no formato ISO
        self.expire = 1 if expire else 0  # Define se a senha expira (1 para True, 0 para False)
