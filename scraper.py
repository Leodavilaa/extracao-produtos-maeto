import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from time import sleep

site = "https://www.lojamaeto.com/"

def configurar_webdriver():
    options = Options()
    # options.add_argument("--headless=new")  # Ative se quiser rodar sem abrir janela
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def rolar_ate_carregar_todos(driver, tempo_espera=5):
    ultimo_altura = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Rola até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(tempo_espera)

        # Espera e pega a nova altura
        nova_altura = driver.execute_script("return document.body.scrollHeight")

        # Se a altura não mudou, acabou de carregar
        if nova_altura == ultimo_altura:
            break

        ultimo_altura = nova_altura

def buscar_produtos(termo):
    driver = configurar_webdriver()
    wait = WebDriverWait(driver, 20)
    driver.get(site)

    try:
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(termo)
        search_box.submit()

        wait.until(EC.presence_of_element_located((By.ID, "list-infinity-scroll")))
    except Exception as e:
        print(f"[ERRO] Produtos não carregaram ou campo de busca falhou: {e}")
        driver.quit()
        return []
    
    rolar_ate_carregar_todos(driver)

    produtos_links = driver.find_elements(By.CSS_SELECTOR, "a.grid-card-link.url-image")
    links = [elem.get_attribute("href") for elem in produtos_links]

    produtos = []

    for link in tqdm(links, desc="Extraindo produtos"):
        try:
            driver.get(link)
            print(f"[DEBUG] Acessando: {link}")
            wait.until(EC.presence_of_element_located((By.XPATH, '//h1')))
            sleep(5)

            sku = driver.find_element(By.XPATH, '//span[@class="sku-active"]').text
                 
            titulo_completo = driver.find_element(By.XPATH, '//h1[@class="product-title"]/span').text
            titulo = titulo_completo.split('(')[0].strip()

            try:
                preco = driver.find_element(By.XPATH, '//*[@id="product-price-info"]/div[4]/div/div/div/div/div[2]/span[2]/span').text
            except:
                preco = ""

            try:
                preco_pix = driver.find_element(By.XPATH, '//span[@id="pixChangePrice"]').text
            except:
                preco_pix = ""

            try:
                valor_parcela = driver.find_element(By.XPATH, '//span[@class="installments-amount"]').text
            except:
                valor_parcela = ""
            
            try:
                num_parcelas = driver.find_element(By.XPATH, '//div[@id="mainProductParcel"]//span[contains(text(), "x")]').text
            except:
                num_parcelas = ""

            try:
                wait.until(EC.presence_of_element_located((By.ID, "product-description-table-attributes")))
                nomes = driver.find_elements(By.XPATH, '//td[@class="attribute-name"]')
                valores = driver.find_elements(By.XPATH, '//td[@class="attribute-value"]')
                info_tecnica = "\n".join(
                    f"{nome.text.strip()}: {valor.text.strip()}"
                    for nome, valor in zip(nomes, valores)
                )
            except:
                info_tecnica = ""

            produtos.append({
                "sku": sku,
                "titulo": titulo,
                "preco": preco,
                "preco_pix": preco_pix,
                "num_parcelas": num_parcelas,
                "valor_parcela": valor_parcela,
                "info_tecnica": info_tecnica
            })

        except Exception as e:
            print(f"[ERRO] Falha ao capturar produto {link}: {e}")
            continue

    driver.quit()
    salvar_no_banco(produtos)
    return produtos

def salvar_no_banco(produtos):
    if not produtos:
        print("[AVISO] Nenhum produto para salvar.")
        return

    print(f"[INFO] Salvando {len(produtos)} produtos no banco de dados...")

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

    for p in produtos:
        try:
            print(f"  Gravando produto SKU: {p['sku']}")
            cursor.execute("""
                INSERT INTO produtos (sku, titulo, preco, preco_pix, valor_parcela, num_parcelas, info_tecnica)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(sku) DO UPDATE SET
                    titulo=excluded.titulo,
                    preco=excluded.preco,
                    preco_pix=excluded.preco_pix,
                    valor_parcela=excluded.valor_parcela,
                    num_parcelas=excluded.num_parcelas,
                    info_tecnica=excluded.info_tecnica
            """, (
                p["sku"], p["titulo"], p["preco"], p["preco_pix"],
                p["valor_parcela"], p["num_parcelas"], p["info_tecnica"]
            ))
        except Exception as e:
            print(f"[ERRO] Falha ao salvar SKU {p['sku']}: {e}")

    conn.commit()
    conn.close()
    print("[INFO] Produtos salvos com sucesso.")

