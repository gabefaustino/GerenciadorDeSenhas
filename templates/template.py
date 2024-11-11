# Importa as bibliotecas necessárias para manipulação de caminho de arquivos e configuração de sistema
import sys
import os

# Adiciona o caminho absoluto do diretório do projeto ao PATH para permitir a importação de módulos de outros diretórios
sys.path.append(os.path.abspath(os.curdir))

# Importa a classe Password para gerenciar a criação e recuperação de senhas
# Importa FernetHasher para a funcionalidade de criptografia de senhas
from model.password import Password
from views.password_views import FernetHasher

# Solicita ao usuário uma ação e utiliza a instrução `match` (Python 3.10+)
action = input('Digite 1 para salvar uma nova senha ou 2 para ver uma senha existente: ')
match action:
    # Caso o usuário escolha '1', o programa entra no fluxo de salvar uma nova senha
    case '1':
        # Checa se existem senhas salvas. Se não houver nenhuma, cria uma chave para criptografia
        if len(Password.get()) == 0:
            key, path = FernetHasher.create_key(archive=True)  # Gera e armazena uma nova chave
            print('Sua chave foi criada. Salve-a com cuidado, pois sem ela não poderá recuperar suas senhas.')
            print(f'Chave: {key.decode("utf-8")}')
            if path:
                print('Chave salva em um arquivo. Lembre-se de removê-lo após transferi-lo com segurança.')
                print(f'Caminho: {path}')
        else:
            # Caso já haja senhas, solicita que o usuário insira a chave existente para evitar conflito
            key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')
        
        # Coleta as informações da senha e o domínio a ser salvo
        domain = input('Domínio: ')
        password = input('Digite a senha: ')
        
        # Criptografa a senha com a chave fornecida pelo usuário
        fernet = FernetHasher(key)
        p1 = Password(domain=domain, password=fernet.encrypt(password).decode('utf-8'))
        
        # Salva a senha criptografada usando o método `save` da classe Password
        p1.save()

    # Caso o usuário escolha '2', o programa entra no fluxo de recuperação de senha
    case '2':
        domain = input('Domínio: ')  # Recebe o domínio para busca da senha
        key = input('Key: ')  # Solicita a chave de criptografia do usuário
        
        # Inicializa o objeto de criptografia com a chave fornecida
        fernet = FernetHasher(key)
        data = Password.get()  # Recupera todas as senhas salvas
        password = ''  # Variável para armazenar a senha descriptografada
        
        # Percorre todos os registros para encontrar o domínio desejado
        for i in data:
            if domain in i['domain']:
                # Descriptografa a senha ao encontrar o domínio correspondente
                password = fernet.decrypt(i['password'])
        
        # Exibe a senha ou uma mensagem de erro caso o domínio não seja encontrado
        if password:
            print(f'Sua senha: {password}')
        else:
            print('Nenhuma senha encontrada para esse domínio.')
