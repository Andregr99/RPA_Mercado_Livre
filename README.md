# 🚀 **RPA Mercado Livre - Web Scraping Automatizado**

Automação robusta para coleta de dados de produtos no Mercado Livre usando Playwright e MySQL.


## ⚙️ **Funcionalidades**  

✅ **Extração de dados:** Captura informações de cotações diretamente do Mercado Livre.

✅ **Armazenamento de dados:** Armazenamento em MySQL com tratamento de erros.

✅ **Logging estruturado:** Registra eventos e erros durante a execução para facilitar a depuração.

✅ **Organização modular:** Código dividido em módulos específicos para melhor manutenibilidade.

✅ **Tratamento de exceções:** Implementa mecanismos robustos para lidar com erros inesperados.

✅ **Logging:** Sistema completo de logs para monitoramento.


## 🚀 **Tecnologias Utilizadas**

**Python 3.10+** (principal)

**Playwright** (automação web e scraping)

**Pandas** (DataFrames, tratamento de NaN)

**Logging** (rastreamento de execução)

**Banco de Dados MySQL** (mysql-connector-python)

**Gestão de Env** (Python-dotenv)

**Empacotamento** setuptools (setup.py)

## ⚙️ **Instalação e Execução** 

**Pré-requisitos**

Python 3.10 ou superior

MySQL 8+ ou superior(local ou remoto)

Git (para clonar o repositório)

1️⃣ Clone o repositório:

git clone https://github.com/Andregr99/RPA_Mercado_Livre.git

cd rpa_mercado_livre

2️⃣ Crie e ative um ambiente virtual:

python -m venv venv

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

3️⃣ Instale as dependências e o Playwright:

pip install -r requirements.txt

playwright install

pip install mysql-connector-python

pip install -e .

🛢️ Configure o Banco de Dados

Crie um arquivo .env na raiz:

DB_HOST=localhost

DB_USER=root

DB_PASSWORD=

DB_NAME=rpa_mercado_livre

🗃️ Execute o SQL para criar a tabela (apenas uma vez):

CREATE TABLE produtos (

    id INT AUTO_INCREMENT PRIMARY KEY,
    
    nome VARCHAR(255) NOT NULL,
    
    preco DECIMAL(10, 2) NOT NULL,
    
    avaliacao FLOAT,
    
    vendedor VARCHAR(255),
    
    qtd_avaliacoes INT,
    
    data_coleta DATE NOT NULL
);

ℹ️ Suporte ao Playwright

Caso encontre problemas com a instalação do Playwright:

No Windows, execute como Administrador

No Linux, pode ser necessário instalar dependências adicionais:
sudo apt-get install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

