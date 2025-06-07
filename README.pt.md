# Aplicação de Conversão de Texto em Fala (TTS)

Esta aplicação converte texto em fala usando Next-gen Kaldi. Possui um backend FastAPI que fornece uma API para um frontend Vue.js.

## Estrutura do Projeto

```
Testupavois/
├── backend/          # Arquivos específicos do backend
│   ├── __init__.py   # Marca o backend como um pacote Python
│   ├── app.py        # Aplicação backend FastAPI (fornece API)
│   ├── model.py      # Gerencia o carregamento e inferência dos modelos TTS
│   └── requirements.txt # Dependências Python para o backend
├── frontend/         # Aplicação frontend Vue.js
│   ├── src/          # Código fonte do Vue, incluindo apiService.ts e App.vue
│   ├── public/
│   ├── package.json    # Dependências e scripts do frontend
│   └── vite.config.js  # Configuração do Vite
├── Dockerfile        # Para construir a imagem Docker
├── README.md         # Versão em Inglês deste arquivo
└── README.pt.md      # Este arquivo (Português)
```

## Executando a Aplicação

Existem duas maneiras de executar esta aplicação: usando Docker para o backend ou executando tanto o backend quanto o frontend localmente.

### Opção 1: Usando Docker (para API Backend)

Este método executa o backend FastAPI em um contêiner Docker. O frontend Vue.js ainda precisará ser executado localmente, conforme descrito na 'Opção 2'.

**Pré-requisitos:**
*   [Docker](https://docs.docker.com/get-docker/) instalado no seu sistema.

**Passos:**

1.  **Construa a imagem Docker:**
    Abra um terminal no diretório raiz do projeto (`Testupavois/`) e execute:
    ```bash
    docker build -t tts-app .
    ```

2.  **Execute o contêiner Docker:**
    ```bash
    docker run -p 8000:8000 tts-app
    ```

3.  **Acesse a API do backend:**
    A API do backend FastAPI estará disponível em `http://localhost:8000`.
    Você pode acessar a documentação interativa da API (Swagger UI) em `http://localhost:8000/docs`.
    O frontend Vue.js (executado localmente) se conectará a esses endpoints da API.

### Opção 2: Executando Localmente (Backend e Frontend)

**Pré-requisitos:**
*   Python 3.9 ou superior
*   Node.js (versão 20.x recomendada, conforme Dockerfile) e npm
*   `wget` (para baixar `espeak-ng-data` se não estiver presente da compilação Docker)
*   `pip` para Python 3 (gerenciador de pacotes Python). Se não estiver instalado, em sistemas Debian/Ubuntu, você pode instalá-lo com: `sudo apt update && sudo apt install python3-pip`

**Configuração do Backend (Python - FastAPI):**

1.  **Navegue até o diretório raiz do projeto:**
    ```bash
    cd /path/to/Testupavois
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```
    *Nota: O `venv` pode ser criado dentro do diretório `backend/` ou na raiz do projeto. Ajuste os caminhos conforme necessário.*

3.  **Instale as dependências do backend:**
    Certifique-se de que `backend/requirements.txt` inclui `fastapi`, `uvicorn[standard]`, `python-multipart`, `soundfile`, `sherpa-onnx`, e `huggingface_hub`. (Gradio deve ser removido).
    ```bash
    python3 -m pip install -r backend/requirements.txt
    ```

4.  **Execute a aplicação backend:**
    Navegue para a raiz do projeto se ainda não estiver lá. O script `backend/app.py` (quando executado como parte do módulo `backend.app`) tentará baixar `espeak-ng-data` na primeira execução, se não estiver presente.
    A partir da raiz do projeto (`Testupavois/`), execute:
    ```bash
    python3 -m uvicorn backend.app:app --reload --port 8000
    ```
    O backend FastAPI estará em execução. Você pode acessar:
    *   Os endpoints da API em `http://localhost:8000/api/...`
    *   A documentação interativa da API (Swagger UI) em `http://localhost:8000/docs`.

**Configuração do Frontend (Vue.js - Vite):**

O frontend Vue.js no diretório `frontend/` fornece uma interface de usuário customizada para a funcionalidade TTS.

1.  **Navegue até o diretório do frontend:**
    ```bash
    cd /path/to/Testupavois/frontend
    ```

2.  **Instale as dependências do frontend:**
    ```bash
    npm install
    ```

3.  **Inicie o servidor de desenvolvimento do frontend:**
    ```bash
    npm run dev
    ```
    Isso normalmente iniciará o frontend em uma porta diferente (por exemplo, `http://localhost:5173`). Este frontend está configurado para fazer requisições para o backend FastAPI rodando em `http://localhost:8000`.

## Como Funciona

O backend é construído com Python usando FastAPI. O arquivo `backend/app.py` configura a aplicação FastAPI e define endpoints de API (ex: para listar idiomas, modelos e realizar TTS). A lógica principal de TTS e o carregamento de modelos estão em `backend/model.py`, utilizando `sherpa-onnx` e modelos pré-treinados baixados via `huggingface_hub`.

A aplicação baixa `espeak-ng-data`, necessário para alguns modelos TTS, durante a primeira execução do `backend/app.py` ou ao construir a imagem Docker.

O frontend é uma aplicação Vue.js construída com Vite. Ele fornece uma interface de usuário com controles para seleção de idioma e modelo, entrada de texto e reprodução de áudio, interagindo com o backend FastAPI através dos endpoints `/api` definidos.
