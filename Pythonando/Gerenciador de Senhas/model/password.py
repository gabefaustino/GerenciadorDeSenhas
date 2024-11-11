#Criando um model para representar uma "tabela no banco de dados"

from datetime import datetime
from pathlib import Path


#criando classe que serve de base a todas as classes quer representam tabelas em banco de dados para criar os métodos de save e get
class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    def save(self):
        table_path = Path(self.DB_DIR / f'{self.__class__.__name__}.txt')
        if not table_path.exists():
            table_path.touch()
        
        with open(table_path, 'a') as arq:  #modo a = append -> escreve mais o que já tinha
            arq.write("|".join(list(map(str, self.__dict__.values()))))
            arq.write('\n')
    @classmethod
    def get(cls):
        table_path = Path(cls.DB_DIR / f'{cls.__name__}.txt')

        if not table_path.exists():
            table_path.touch()
        
        with open(table_path, 'r') as arq:  #modo r = read
            x = arq.readlines() #x = variável qualquer. devolve todas as linhas que tem no arquivo
        
        results = []
        atributos = vars(cls()).keys()
        
        for i in x:
            split_v = i.split('|')
            tmp_dict = dict(zip(atributos, split_v))    #cria um dicionário (por linha) unindo (zip) os atributos com os valores de cada linha do banco
            results.append(tmp_dict)    #adiciona o tmp_dict na lista results
        return results


class Password:
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0

