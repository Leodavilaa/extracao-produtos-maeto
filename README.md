# 🛒 Extração de Produtos - Loja Maeto

Este projeto realiza buscas automatizadas no site da [Loja Maeto](https://www.lojamaeto.com/) e extrai dados dos produtos retornados, 
armazenando as informações em um banco de dados SQLite.

---

## 🔍 Funcionalidades

- Busca de produtos a partir de um termo inserido no terminal.
- Extração automática dos seguintes dados:
  - SKU (identificador único do produto)
  - Título do produto (limpo de códigos adicionais)
  - Preço
  - Preço no PIX
  - Valor da parcela
  - Número de parcelas
  - Informações técnicas do produto
- Armazenamento em banco de dados SQLite (`produtos.db`)
- Atualização automática dos produtos já existentes com base no SKU

---

## 🧰 Tecnologias Utilizadas

- Python 3.8+
- Selenium
- WebDriver Manager
- TQDM
- SQLite3 (integrado ao Python)
- Google Chrome (com ChromeDriver)

---

## ⚙️ Instalação

01.**Clone este repositório:**

```bash
git clone https://github.com/Leodavilaa/extracao-produtos-maeto.git
cd extracao-produtos-maeto

02.**Instale as dependências:**

pip install -r requirements.txt

03.**Execute o script:**

python create_database.py  # Cria o banco de dados
python main.py             # Executa a extração



## 💡 Exemplo de uso

Ao executar o script, será solicitado um termo de busca:

Digite o nome do produto para busca: lampada led
O script navegará automaticamente pelo site, coletará os dados de todos os produtos listados e os armazenará no arquivo produtos.db.

## 📁 Estrutura do Projeto

📦 seu-repositorio/
├── main.py
├── produtos.db
├── requirements.txt
└── README.md

## 📄 Licença

```Este projeto está licenciado sob a MIT License.