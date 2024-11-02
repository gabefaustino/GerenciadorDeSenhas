import string, secrets  #ascii e valores aleatórios
import hashlib  #transforma valor em hash (crypto "one-a-way")
import base64   #forma padrão de comunicação entre sistemas para envio e recebimento de dados
from pathlib import Path #biblioteca que auxilia a manipular diretórios
from cryptography.fernet import Fernet, InvalidToken #cryptography permite trabalhar com criptografia em python



class FernetHasher:
    #Constantes
    #caracterezes possíveis: de a - z minúsculos e maiúsculos
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    #BASE_DIR se refere a raiz do projeto
    #__file__ caminho da raiz do SO até o arquivo atual
    #.resolve() caminho absoluto
    #.parent -> cd ..
    #encontra o caminho da pasta keys (Gerenciador de Senhas)
    BASE_DIR = Path(__file__).resolve().parent.parent
    #atribui caminho da pasta 'keys', pasta que quero salvar a chave criada pelo usuário
    KEY_DIR = BASE_DIR / 'keys'

    #Método construtor __init__
    #é chamado quando instanciamos uma nova classe
    #self é para métodos de instância (cls é para métodos de classe)
    #self referencia a própria classe
    
    def __init__(self, key):
        #se a chave não estiver em bytes
        if not isinstance(key, bytes):
            key = key.encode()
        #criando uma variável que não é a mesma em todas as classes
        #para cada usuário que for utilizar, vai ter uma instância de fernet diferente, porque cada um vai ter a sua chave
        self.fernet = Fernet(key)


    @classmethod
    #todo método de classe precisa de um "cls", para informar que é um método de classe
    def _get_random_string(cls, lenght = 25):
        string = ''
        for i in range(lenght):
            #string recebe 25 valores (for-lenght) aleatórios dentre os possíveis na RANDOM_STRING_CHARS
            #para acessar variável de classe, utliza o cls.[variável]
            string += secrets.choice(cls.RANDOM_STRING_CHARS)
        
        return string
    
    
    @classmethod
    #archive=False -> se não for passado nada, o arquivo não vai ser salvo
    def create_key(cls, archive=False):
        #recebe o valor aleatório gerado no método _get_random_string
        value = cls._get_random_string()
        #precisamos transformar esse valor em uma hash (criptografia one-way)
        #transforma em um sha256
            #sha256: algoritmo de hash, um dos mais conhecidos e usados atualmente
            #sha256 espera um valor em byte, logo value.encode('utf-8') -> armazena valor em memória como byte, não mais como string
        #.digest() converte novamente para string
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        #converte o valor da hash em base64
            #base64 é a forma padrão de comunicação entre sistemas binários, quando se busca e envia dados
            #esse base64 vai ser a senha
        key = base64.b64encode(hasher)

        #se quiser salvar, archive == True
        if archive:
            return key, cls.archive_key(key)
        else:
            return key, None

    @classmethod
    def archive_key(cls, key):
        #cria arquivo key.key
        file = 'key.key'
        #se já existir um arquivo chamado key.key, chama a função de strings aleatórias para criar um novo arquivo
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(lenght=5)}.key'
        #with: gerenciador de contexto, onde tenho um arquivo aberto
        #/ concatena com o nome do meu arquivo
        #wb -> modo de abertura. w = write; b = binário
        #as nomeie como arq
        with open(cls.KEY_DIR / 'key.txt', 'wb') as arq:
            arq.write(key)

        return cls.KEY_DIR / file
    
    def encrypt(self, value):
        #encrypt só funciona se for em bytes, logo, verificar se value está em bytes
        if not isinstance(value, bytes):
            #encoda para bytes
            value = value.encode()
        return self.fernet.encrypt(value)
    
    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        
        try:
            return self.fernet.decrypt(value).decode()
        #se o erro for específico InvalidToken, chame-o de "e"
        except InvalidToken as e:
            return "Token Inválido"