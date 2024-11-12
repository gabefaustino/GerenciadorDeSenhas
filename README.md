# Gerenciador de Senhas Simples 🔐

Este projeto é um gerenciador de senhas simples que armazena e recupera senhas de maneira segura. Ele utiliza criptografia `Fernet` para proteger as senhas e armazena-as em arquivos de texto, simulando um banco de dados.

## Requistos
- **Python 3.10+**

## Funcionalidades

- **Armazenamento Seguro de Senhas:** Criptografa senhas usando `Fernet` antes de armazená-las.
- **Recuperação de Senhas Criptografadas:** Permite descriptografar e visualizar senhas salvas.
- **Persistência em Arquivo:** Armazena dados em arquivos de texto, simulando um banco de dados.
- **Interface de Usuário Interativa:** Permite ao usuário salvar novas senhas ou recuperar senhas existentes.

### Pré-requisitos

- Certifique-se de ter o Python 3.10+ instalado, pois o código utiliza a estrutura `match`, disponível a partir dessa versão.
- Instale as dependências necessárias, como `cryptography`, usando o comando:
  ```bash
  pip install cryptography

## Funcionamento Geral do Código

### Fluxo de Operações

1. Ao escolher salvar uma nova senha:
   - O usuário fornece uma chave de criptografia, que pode ser gerada automaticamente caso seja a primeira senha salva.
   - A senha e o domínio são coletados e a senha é criptografada com a chave fornecida.
   - A senha criptografada é armazenada no arquivo `Password.txt`.

2. Ao escolher recuperar uma senha:
   - O usuário fornece o domínio e a chave de criptografia.
   - O programa busca o domínio nos registros salvos e tenta descriptografar a senha usando a chave fornecida.
   - A senha é exibida caso o domínio seja encontrado e a chave seja correta.

## Complexidade do Código

Abaixo está a análise de complexidade das principais operações do projeto:

1. **`save`:**  
   - **Complexidade:** O(1)  
   - **Explicação:** O método `save` realiza uma operação de anexação (`append`) em um arquivo. Esta operação é independente do número de linhas no arquivo, pois apenas adiciona dados ao final. Portanto, a complexidade é constante, O(1).

2. **`get`:**  
   - **Complexidade:** O(n)  
   - **Explicação:** O método `get` lê todas as linhas do arquivo para obter os registros armazenados. Como a leitura de todas as linhas depende do número de registros (linhas) no arquivo, a complexidade é linear, O(n), onde `n` é o número de registros armazenados.

3. **Busca de Domínio para Recuperação de Senha:**
   - **Complexidade:** O(n)  
   - **Explicação:** A operação de busca de domínio durante a recuperação da senha envolve percorrer cada registro para localizar o domínio correto. Novamente, esta operação é linear, O(n), pois é necessário verificar cada registro até encontrar uma correspondência ou esgotar todos os registros.

4. **Criptografia e Descriptografia (Fernet):**
   - **Complexidade:** O(k)  
   - **Explicação:** A criptografia e descriptografia com `Fernet` têm complexidade O(k), onde `k` é o tamanho da senha que está sendo criptografada ou descriptografada. Como as senhas tendem a ser curtas, essa complexidade é quase constante para o uso típico.

## Desempenho Geral

- Como o projeto utiliza um "banco de dados" em arquivos de texto, a leitura e a busca em arquivos maiores podem impactar o desempenho. Porém, para um número pequeno a moderado de registros, o desempenho será razoável.
- A complexidade dominante para operações de recuperação é O(n), tornando o projeto viável para uso pessoal ou de pequena escala, mas potencialmente mais lento para grandes volumes de dados.
