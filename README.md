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
