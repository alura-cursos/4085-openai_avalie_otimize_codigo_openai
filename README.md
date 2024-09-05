#<img width="996" alt="Capa4085" src="https://github.com/user-attachments/assets/a248c5af-8f71-4756-b6e7-2d426b8e7314">

Code Interpreter: Performance e Co-Programação com a OpenAI

## ⚙️ Configuração do Ambiente

### Criando e Ativando o Ambiente Virtual

**Windows:**
```bash
python -m venv curso_otimizacao
source curso_otimizacao/Scripts/activate
```

**Mac/Linux:**
```bash
python3 -m venv curso_otimizacao
source curso_otimizacao/bin/activate
```

### Instalação das Bibliotecas

```bash
pip install -r requirements.txt
```

### Configuração da Chave de API da OpenAI

Para utilizar o Code Interpreter da OpenAI, é necessário configurar a chave de API:

1. Crie um arquivo `.env` no diretório raiz do projeto.
2. Insira a sua chave de API no arquivo `.env` usando o seguinte formato:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Substitua `your_openai_api_key_here` pela sua chave de API da OpenAI.

### Configuração do .gitignore

Para garantir que o arquivo `.env` e as pastas de cache do Python não sejam incluídos no controle de versão, adicione um arquivo `.gitignore` com o seguinte conteúdo:

```
.env
**/__pycache__/
**/curso_otimizacao
```

Esse arquivo `.gitignore` ajudará a manter a segurança da sua chave de API e a evitar o versionamento de arquivos temporários desnecessários.
