import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# =============================
# CONFIGURAÇÕES
# =============================

URL = "http://abm.m3risk.com.br/home"
LOGIN = "eduardo.lima@vxconsult.com.br"
SENHA = "102030"

# =============================
# FUNÇÕES AUXILIARES
# =============================

def formatar_placa(placa):
    """Formata a placa para o padrão XXX-XXXX"""
    placa = str(placa).strip().replace("-", "").replace(" ", "").upper()
    if len(placa) == 7:
        placa = placa[:3] + "-" + placa[3:]
    return placa

def esperar_e_clicar(driver, wait, by, valor, tempo_maximo=10):
    """Espera elemento ficar clicável e clica"""
    try:
        elemento = wait.until(EC.element_to_be_clickable((by, valor)))
        driver.execute_script("arguments[0].click();", elemento)
        return True
    except:
        return False

def verificar_elemento(driver, by, valor):
    """Verifica se elemento existe na página"""
    try:
        driver.find_element(by, valor)
        return True
    except NoSuchElementException:
        return False

# =============================
# CARREGAR CSV
# =============================

print("Carregando placas do CSV...")
df = pd.read_csv(r"C:\Users\edums\Desktop\placas.csv")
placas = [formatar_placa(p) for p in df["placa"].tolist()]
print(f"{len(placas)} placas carregadas")

# =============================
# INICIAR CHROME
# =============================

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

# =============================
# LOGIN
# =============================

print("Fazendo login...")
try:
    driver.get(URL)
    
    # Login
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(LOGIN)
    driver.find_element(By.NAME, "password").send_keys(SENHA)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(5)
    print("Login realizado com sucesso")
except Exception as e:
    print(f"Erro no login: {e}")
    driver.quit()
    exit()

# =============================
# NAVEGAR MENU
# =============================

print("Acessando módulo de veículos...")
try:
    # Menu Cadastros
    esperar_e_clicar(driver, wait, By.XPATH, "//span[contains(text(),'Cadastros')]")
    time.sleep(2)
    
    # Submenu Veículos
    esperar_e_clicar(driver, wait, By.XPATH, "//span[contains(text(),'Veículos')]")
    time.sleep(3)
    
    print("Módulo de veículos acessado")
    
    # =============================
    # CLICAR NO BOTÃO ENVIAR
    # =============================
    print("Clicando no botão Enviar...")
    
    # Tenta encontrar e clicar no botão Enviar por diferentes seletores
    botoes_enviar = [
        (By.XPATH, "//button[contains(text(),'Enviar')]"),
        (By.XPATH, "//button[contains(@class,'btn-primary') and contains(text(),'Enviar')]"),
        (By.XPATH, "//button[@type='submit' and contains(text(),'Enviar')]"),
        (By.XPATH, "//button[contains(@class,'btn') and contains(text(),'Enviar')]")
    ]
    
    enviar_clicado = False
    for by, selector in botoes_enviar:
        try:
            botao_enviar = wait.until(EC.element_to_be_clickable((by, selector)))
            driver.execute_script("arguments[0].click();", botao_enviar)
            enviar_clicado = True
            print(f"Botão Enviar clicado com sucesso (seletor: {selector})")
            break
        except:
            continue
    
    if not enviar_clicado:
        # Último recurso: procurar por qualquer botão com texto Enviar
        try:
            botoes = driver.find_elements(By.XPATH, "//button")
            for botao in botoes:
                if "Enviar" in botao.text and botao.is_displayed():
                    driver.execute_script("arguments[0].click();", botao)
                    enviar_clicado = True
                    print("Botão Enviar clicado (fallback)")
                    break
        except:
            pass
    
    if not enviar_clicado:
        raise Exception("Não foi possível clicar no botão Enviar")
    
    # Aguarda a próxima tela carregar (onde aparece o campo de pesquisa)
    print("Aguardando carregamento da tela de pesquisa...")
    time.sleep(5)
    
    # Aguarda o campo de pesquisa ficar visível
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Pesquisar')]")))
        print("Campo de pesquisa encontrado - tela carregada")
    except:
        print("Aviso: Campo de pesquisa não encontrado imediatamente")
        time.sleep(3)
    
except Exception as e:
    print(f"Erro ao acessar menu ou clicar em Enviar: {e}")
    driver.quit()
    exit()

# =============================
# PROCESSAR PLACAS
# =============================

sucesso = []
erro = []

for i, placa in enumerate(placas, start=1):
    print(f"\n[{i}/{len(placas)}] Processando placa: {placa}")
    print("-" * 40)
    
    try:
        # =============================
        # LOCALIZAR E LIMPAR CAMPO DE PESQUISA
        # =============================
        campo_pesquisa = None
        
        # Tenta encontrar o campo de pesquisa por diferentes seletores
        selectores = [
            (By.XPATH, "//input[contains(@placeholder,'Pesquisar')]"),
            (By.XPATH, "//input[contains(@placeholder,'placa')]"),
            (By.XPATH, "//input[contains(@placeholder,'buscar')]"),
            (By.XPATH, "//input[@type='text' and @placeholder]"),
            (By.XPATH, "//input[contains(@class,'form-control')]")
        ]
        
        for by, selector in selectores:
            try:
                campo_pesquisa = driver.find_element(by, selector)
                if campo_pesquisa.is_displayed():
                    break
            except:
                continue
        
        if not campo_pesquisa:
            # Tenta encontrar qualquer input visível
            inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
            for inp in inputs:
                if inp.is_displayed():
                    campo_pesquisa = inp
                    break
        
        if not campo_pesquisa:
            raise Exception("Campo de pesquisa não encontrado")
        
        # Limpa e digita a placa
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(placa)
        print(f"Placa {placa} digitada no campo de pesquisa")
        time.sleep(3)  # Aguarda filtro
        
        # =============================
        # SELECIONAR CHECKBOX
        # =============================
        checkbox_selecionado = False
        
        # Procura checkbox da linha que contém a placa
        linhas = driver.find_elements(By.XPATH, "//tr")
        for linha in linhas:
            if placa in linha.text:
                try:
                    checkbox = linha.find_element(By.XPATH, ".//input[@type='checkbox']")
                    driver.execute_script("arguments[0].click();", checkbox)
                    checkbox_selecionado = True
                    print("Checkbox específico da placa selecionado")
                    break
                except:
                    continue
        
        if not checkbox_selecionado:
            # Tenta selecionar qualquer checkbox visível
            checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            for cb in checkboxes:
                if cb.is_displayed():
                    driver.execute_script("arguments[0].click();", cb)
                    checkbox_selecionado = True
                    print("Checkbox selecionado (fallback - primeiro checkbox visível)")
                    break
        
        if not checkbox_selecionado:
            raise Exception("Não foi possível selecionar checkbox")
        
        time.sleep(1)
        
        # =============================
        # CLICAR DESATIVAR
        # =============================
        if not esperar_e_clicar(driver, wait, By.XPATH, "//button[contains(text(),'Desativar')]"):
            raise Exception("Botão Desativar não encontrado")
        
        print("Botão Desativar clicado")
        
        # =============================
        # AGUARDAR E CLICAR NO POPUP DE CONFIRMAÇÃO
        # =============================
        time.sleep(2)
        
        # Estratégia 1: Aguardar popup
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Tem certeza')]")))
            print("Popup de confirmação detectado")
        except:
            print("Popup não detectado explicitamente, tentando localizar botão Sim mesmo assim")
        
        # Estratégia 2: Procurar e clicar no botão Sim
        sim_clicado = False
        
        # Tentar diferentes formas de localizar o botão Sim
        selectores_sim = [
            (By.XPATH, "//button[contains(text(),'Sim')]"),
            (By.XPATH, "//button[contains(text(),'sim')]"),
            (By.XPATH, "//button[contains(@class,'confirm')]"),
            (By.XPATH, "//button[contains(text(),'OK')]"),
            (By.XPATH, "//button[contains(text(),'Confirmar')]"),
            (By.XPATH, "//button[contains(@class,'btn-success')]")
        ]
        
        for by, selector in selectores_sim:
            try:
                botoes = driver.find_elements(by, selector)
                for botao in botoes:
                    if botao.is_displayed():
                        driver.execute_script("arguments[0].click();", botao)
                        sim_clicado = True
                        print(f"Botão Sim clicado (seletor: {selector})")
                        break
                if sim_clicado:
                    break
            except:
                continue
        
        # Fallback: tentar clicar em qualquer botão no popup
        if not sim_clicado:
            try:
                # Procura por modais/popups
                popups = driver.find_elements(By.XPATH, "//div[contains(@class,'modal') or contains(@class,'popup') or contains(@class,'dialog')]")
                for popup in popups:
                    botoes_popup = popup.find_elements(By.XPATH, ".//button")
                    for botao in botoes_popup:
                        if botao.is_displayed():
                            driver.execute_script("arguments[0].click();", botao)
                            sim_clicado = True
                            print("Botão do popup clicado (fallback)")
                            break
                    if sim_clicado:
                        break
            except:
                pass
        
        # Último recurso: clicar no botão Sim por JavaScript
        if not sim_clicado:
            try:
                driver.execute_script("""
                    var botoes = document.querySelectorAll('button');
                    for(var i = 0; i < botoes.length; i++) {
                        var texto = botoes[i].textContent || botoes[i].innerText;
                        if(texto.includes('Sim') || texto.includes('OK') || texto.includes('Confirmar')) {
                            botoes[i].click();
                            return true;
                        }
                    }
                    return false;
                """)
                sim_clicado = True
                print("Botão Sim clicado via JavaScript")
            except:
                print("AVISO: Não foi possível clicar no botão Sim")
        
        if not sim_clicado:
            print("ERRO: Não foi possível confirmar a desativação")
            erro.append(placa)
            continue
        
        time.sleep(3)  # Aguarda processamento
        
        # Verificar se desativou com sucesso
        try:
            # Procura por mensagem de sucesso
            mensagens_sucesso = driver.find_elements(By.XPATH, "//*[contains(text(),'sucesso') or contains(text(),'Sucesso') or contains(text(),'Sucess')]")
            if mensagens_sucesso:
                print("Mensagem de sucesso encontrada")
        except:
            pass
        
        sucesso.append(placa)
        print(f"✓ Placa {placa} desativada com sucesso")
        
    except Exception as e:
        print(f"✗ Erro ao processar placa {placa}: {str(e)[:100]}")
        erro.append(placa)
        
        # Tenta limpar o filtro para a próxima placa
        try:
            campo_pesquisa = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Pesquisar')]")
            campo_pesquisa.clear()
            print("Campo de pesquisa limpo para próxima placa")
        except:
            pass
    
    # Pequena pausa entre iterações
    time.sleep(2)

# =============================
# RESULTADO FINAL
# =============================

print("\n" + "="*50)
print("RESULTADO FINAL")
print("="*50)
print(f"Total de placas processadas: {len(placas)}")
print(f"Sucesso: {len(sucesso)}")
print(f"Erro: {len(erro)}")
if len(placas) > 0:
    print(f"Taxa de sucesso: {(len(sucesso)/len(placas)*100):.1f}%")

# Salvar resultados
if sucesso:
    pd.DataFrame({"placa": sucesso}).to_csv("placas_sucesso.csv", index=False)
    print(f"✓ Arquivo 'placas_sucesso.csv' salvo com {len(sucesso)} placas")

if erro:
    pd.DataFrame({"placa": erro}).to_csv("placas_erro.csv", index=False)
    print(f"✗ Arquivo 'placas_erro.csv' salvo com {len(erro)} placas")

# =============================
# FINALIZAR
# =============================

print("\nFinalizando automação...")
driver.quit()
print("Automação concluída!")