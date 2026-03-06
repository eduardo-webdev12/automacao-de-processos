# 🚗 AutoDesativar - Automação de Desativação de Veículos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-yellow.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

## 📋 Sobre o Projeto

Este projeto automatiza o processo de desativação em massa de veículos no sistema ABM M3 Risk. O script realiza login, navega até a seção de veículos e processa uma lista de placas, desativando-as automaticamente e lidando com popups de confirmação.

### 🎯 Funcionalidades

- ✅ Login automático no sistema
- ✅ Navegação pelos menus (Cadastros → Veículos)
- ✅ Leitura de placas a partir de arquivo CSV
- ✅ Formatação automática de placas (ABC-1234)
- ✅ Pesquisa individual de cada veículo
- ✅ Seleção inteligente de checkboxes
- ✅ Clique no botão "Desativar"
- ✅ Tratamento automático de popups de confirmação
- ✅ Múltiplas estratégias para garantir o clique no "Sim"
- ✅ Geração de relatórios de sucesso/erro
- ✅ Sistema robusto de fallbacks e tratamento de exceções

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Arquivo CSV com as placas a serem processadas

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/autodesativar.git
cd autodesativar

Tratamento de exceções: Continua processando mesmo após erros individuais

Logs detalhados: Acompanhamento passo a passo da execução

Instale as dependências:

bash
pip install pandas selenium webdriver-manager

Prepare seu arquivo CSV com as placas:

csv
placa
ABC1234
XYZ5678
DEF9012

Configuração
Edite as variáveis no início do script:

python
URL = "http://abm.m3risk.com.br/home"
LOGIN = "seu.email@empresa.com"
SENHA = "sua_senha"

Execução
bash
python autodesativar.py

autodesativar/
│
├── autodesativar.py          # Script principal
├── placas.csv                 # Arquivo de entrada com as placas
├── placas_sucesso.csv         # Relatório de placas desativadas
├── placas_erro.csv            # Relatório de placas com erro
└── README.md                   # Documentação

🔧 Como Funciona
Fluxo de Execução
Login → Acesso ao sistema com credenciais

Navegação → Menu Cadastros → Veículos → Botão Enviar

Processamento → Para cada placa no CSV:

Digita a placa no campo de pesquisa

Aguarda o filtro

Seleciona o checkbox correspondente

Clica em "Desativar"

Confirma no popup (clica em "Sim")

Aguarda processamento

Relatórios → Gera arquivos CSV com resultados

🛡️ Recursos de Robustez
Múltiplos seletores: Tenta diferentes formas de encontrar elementos

Fallbacks: Se uma estratégia falha, outra é tentada

JavaScript injection: Cliques via JS quando métodos convencionais falham

Tratamento de exceções: Continua processando mesmo após erros individuais

Logs detalhados: Acompanhamento passo a passo da execução

📊 Exemplo de Saída
text
Carregando placas do CSV...
10 placas carregadas
Fazendo login...
Login realizado com sucesso

[1/10] Processando placa: ABC-1234
----------------------------------------
Placa ABC-1234 digitada no campo de pesquisa
Checkbox específico da placa selecionado
Botão Desativar clicado
Popup de confirmação detectado
Botão Sim clicado
✓ Placa ABC-1234 desativada com sucesso

===== RESULTADO FINAL =====
Total de placas processadas: 10
Sucesso: 10
Erro: 0
Taxa de sucesso: 100.0%

⚠️ Observações Importantes
O script foi desenvolvido para o sistema ABM M3 Risk específico da empresa

Recomenda-se testar com poucas placas antes de executar em larga escala

O tempo de espera entre ações pode ser ajustado conforme necessidade

🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para:

Reportar bugs

Sugerir melhorias

Enviar pull requests

Desenvolvido para otimizar processos repetitivos

## 🎨 Dicas extras:

1. *"Status: Ativo"*

2. *informações de contato*: https://www.linkedin.com/in/eduardo-de-lima-melo/

3. *Versão do código**:(v1.0.0)
