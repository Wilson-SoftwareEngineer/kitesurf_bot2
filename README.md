# 🏄‍♂️ Kitesurf Bot Brasil

Um bot do Telegram que fornece informações sobre condições de vento em tempo real para spots de kitesurf no Brasil.

## 🎯 Funcionalidades

- 🌬️ **Dados de Vento em Tempo Real**: Acesso a informações atualizadas de velocidade, rajadas e direção do vento
- 📍 **Geolocalização**: Busca automática de coordenadas de praias através do nome
- 🗺️ **Spots Populares**: Lista de praias e spots recomendados para kitesurf
- 📱 **Interface Telegram**: Acesso fácil através do Telegram

## 📋 Pré-requisitos

- Python 3.8+
- Token do Telegram Bot (obtenha em [@BotFather](https://t.me/botfather))
- Conexão com internet

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Wilson-SoftwareEngineer/kitesurf_bot2.git
cd kitesurf_bot2
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```
MEU_TOKEN=seu_token_do_telegram_aqui
```

## 📦 Dependências

- `python-telegram-bot==20.7` - Biblioteca oficial do Telegram Bot API
- `python-dotenv==1.0.0` - Carregamento de variáveis de ambiente
- `requests==2.31.0` - Requisições HTTP
- `geopy==2.4.0` - Geolocalização e conversão de coordenadas

## 💻 Como Usar

### Iniciar o bot
```bash
python main.py
```

### Comandos disponíveis
- `/start` - Mensagem de boas-vindas
- `/help` - Ajuda detalhada
- `/spots` - Lista de spots populares

### Exemplo de uso
1. Abra o Telegram e localize o bot
2. Digite `/start` para iniciar
3. Digite o nome da praia e estado (ex: "Jericoacoara, Ceará")
4. Receba as condições de vento em tempo real

## 🌊 Spots Populares

Alguns dos principais spots de kitesurf no Brasil:
- **Ceará**: Jericoacoara, Camocim, Taiba, Cumbuco
- **Piauí**: Barra Grande, Atalaia
- **Rio Grande do Norte**: Genipabu, Galinhos
- **São Paulo**: Ubatuba, Itanhaém
- **Bahia**: Camaçari, Jaguaripe

## 🌤️ Interpretação dos Dados

### Velocidade do Vento
- **< 12 nós**: Vento fraco 😴
- **12-28 nós**: Condição ideal 🚀
- **> 28 nós**: Vento forte ☢️

## 🔌 API Utilizada

- **Open-Meteo**: Dados meteorológicos gratuitos
- **Nominatim**: Geolocalização e geocodificação

## 📝 Estrutura do Projeto

```
kitesurf_bot2/
├── main.py              # Arquivo principal
├── requirements.txt     # Dependências do projeto
├── .env                 # Variáveis de ambiente
├── .gitignore          # Arquivos a ignorar no Git
└── README.md           # Este arquivo
```

## 🛠️ Desenvolvimento

### Adicionar novo spot
Edite a função `spots_command()` em `main.py` para incluir novos spots.

### Modificar lógica do vento
A interpretação das condições de vento está em `start()` e `help_command()`.

## 🐛 Troubleshooting

### Bot não conecta
- Verifique se o token está correto em `.env`
- Certifique-se de que tem conexão com internet

### Localização não encontrada
- Verifique a ortografia do local
- Use formato "Cidade, Estado"

### Timeout na API
- A API pode estar lenta, tente novamente em alguns segundos
- Verifique sua conexão com internet

## 📄 Licença

Este projeto está disponível sob a licença MIT.

## ✉️ Contato

Para sugestões ou reportar problemas, abra uma issue no repositório.

---

**Aloha! Bom vento! 🏄‍♂️**
