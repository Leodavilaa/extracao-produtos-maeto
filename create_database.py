import sqlite3

def criar_banco():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            sku TEXT PRIMARY KEY,
            titulo TEXT,
            preco TEXT,
            preco_pix TEXT,
            valor_parcela TEXT,
            num_parcelas TEXT,
            info_tecnica TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso.")

if __name__ == "__main__":
    criar_banco()
