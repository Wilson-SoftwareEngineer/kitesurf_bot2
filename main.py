import logging
import os
import requests
import html
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. CONFIGURAÇÃO DE LOGS
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. CARREGAR VARIÁVEIS DE AMBIENTE
load_dotenv()
TELEGRAM_TOKEN = os.getenv("MEU_TOKEN")

# 3. CLIENTES EXTERNOS
geolocator = Nominatim(user_agent="kitesurf_brazil_bot", timeout=10)

# 4. FUNÇÃO PARA CONVERTER DIREÇÃO DO VENTO
def wind_direction_to_cardinal(degrees):
    """Converte graus em pontos cardeais"""
    if degrees is None:
        return "N/A"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"]
    idx = round(degrees / 22.5) % 16
    return directions[idx]

# 5. FUNÇÃO PARA OBTER DADOS DO CLIMA
def get_weather(lat, lon):
    """Obtém dados meteorológicos da Open-Meteo API"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"],
        "timezone": "auto"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if 'current' not in data:
            logger.error(f"Dados inválidos da API: {data}")
            return None
            
        return data['current']
    except Exception as e:
        logger.error(f"Erro na requisição do clima: {e}")
    return None

# 6. COMANDOS DO TELEGRAM
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Mensagem de boas-vindas"""
    welcome_text = (
        "🏄‍♂️ *Aloha! Bem-vindo ao Kite Bot Brasil!*\n\n"
        "*Como usar:*\n"
        "Envie o nome da *praia e estado*:\n"
        "• Jericoacoara, Ceará\n"
        "• Barra Grande, Piauí\n"
        "• Atalaia, Sergipe\n\n"
        "*Comandos:*\n"
        "/start - Mensagem inicial\n"
        "/help - Ajuda\n"
        "/spots - Spots populares\n\n"
        "*Condições do vento:*\n"
        "• < 12 nós: Vento fraco 😴\n"
        "• 12-28 nós: Condição ideal 🚀\n"
        "• > 28 nós: Vento forte ☢️"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Ajuda detalhada"""
    help_text = (
        "*❓ AJUDA - KITE BOT BRASIL*\n\n"
        "*📋 COMANDOS:*\n"
        "/start - Inicia o bot\n"
        "/help - Mostra esta mensagem\n"
        "/spots - Lista de spots de kitesurf\n\n"
        "*📍 COMO BUSCAR:*\n"
        "Digite: `Praia, Estado`\n\n"
        "*Exemplos:*\n"
        "• Camocim, Ceará\n"
        "• Taiba, Ceará\n"
        "• Genipabu, Rio Grande do Norte\n"
        "• Ubatuba, São Paulo\n\n"
        "*🌤️ SOBRE OS DADOS:*\n"
        "• Vento em nós (1 nó = 1.852 km/h)\n"
        "• Dados em tempo real\n"
        "• Atualização automática"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def spots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /spots - Lista de spots populares"""
    spots_text = (
        "*🏝️ SPOTS DE KITESURF NO BRASIL*\n\n"
        "*🌅 NORDESTE:*\n"
        "*Ceará:*\n"
        "• Jericoacoara\n"
        "• Preá\n"
        "• Cumbuco\n"
        "• Taiba\n\n"
        "*Rio Grande do Norte:*\n"
        "• São Miguel do Gostoso\n"
        "• Genipabu\n"
        "• Tibau do Sul\n\n"
        "*Piauí:*\n"
        "• Barra Grande\n"
        "• Luis Correia\n\n"
        "• Praia de Macapa\n\n"
        "*🌊 SUL/SUDESTE:*\n"
        "*Santa Catarina:*\n"
        "• Florianópolis\n"
        "• Garopaba\n"
        "• Imbituba\n\n"
        "*São Paulo:*\n"
        "• Ubatuba\n"
        "• Ilha Bela"
    )
    await update.message.reply_text(spots_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa mensagens de texto com nomes de praias"""
    user_input = update.message.text.strip()
    
    if not user_input:
        await update.message.reply_text(
            "Por favor, digite o nome de uma praia.\n"
            "Exemplo: *Praia do Coqueiro, Piauí*",
            parse_mode='Markdown'
        )
        return
    
    chat_id = update.effective_chat.id
    
    # Envia mensagem de processamento
    msg = await context.bot.send_message(
        chat_id=chat_id, 
        text=f"🔍 Buscando: *{user_input[:50]}*...",
        parse_mode='Markdown'
    )
    
    try:
        # Busca a localização
        busca_refinada = f"{user_input[:100]}, Brasil"
        loc = geolocator.geocode(busca_refinada)
        
        # Verifica se encontrou a localização
        if not loc:
            await msg.edit_text(
                "❌ *Local não encontrado!*\n\n"
                "_Dicas para melhorar a busca:_\n"
                "1. Use: `Praia, Estado`\n"
                "2. Verifique a grafia\n"
                "3. Especifique estado\n\n"
                "Use /spots para ver locais populares.",
                parse_mode='Markdown'
            )
            return

        # Obtém dados do clima
        clima = get_weather(loc.latitude, loc.longitude)
        if not clima:
            await msg.edit_text(
                "⚠️ *Erro ao obter dados meteorológicos*\n"
                "Tente novamente em alguns minutos.",
                parse_mode='Markdown'
            )
            return
        
        # Conversão de unidades
        vento_nos = round(clima.get('wind_speed_10m', 0) / 1.852, 1)
        rajada_nos = round(clima.get('wind_gusts_10m', 0) / 1.852, 1)
        direcao = wind_direction_to_cardinal(clima.get('wind_direction_10m'))
        
        # Determina a condição para kitesurf
        if vento_nos < 8:
            status = "😴 Vento MUITO fraco. Não rola velejo hoje."
            emoji = "😴"
        elif 8 <= vento_nos < 12:
            status = "😅 Vento leve. Boa para iniciantes ou foil."
            emoji = "😅"
        elif 12 <= vento_nos <= 25:
            status = "🚀 Condição PERFEITA! Hora de velejar!"
            emoji = "🚀"
        elif 25 < vento_nos <= 30:
            status = "⚡ Vento forte! Experientes apenas, kite pequeno."
            emoji = "⚡"
        else:
            status = "☢️ Vento PERIGOSO! Cuidado extremo necessário."
            emoji = "☢️"
        
        # Formata a resposta final
        endereco_seguro = loc.address[:80]
        
        resposta = (
            f"*🌊 CONDIÇÕES PARA KITESURF*\n"
            f"📍 *Local:* {endereco_seguro}\n"
            f"────────────────────\n"
            f"💨 *Vento Médio:* {vento_nos} nós\n"
            f"🌪️ *Rajadas:* {rajada_nos} nós\n"
            f"🧭 *Direção:* {direcao}\n"
            f"🌡️ *Temperatura:* {clima.get('temperature_2m', 'N/A')}°C\n"
            f"────────────────────\n"
            f"{emoji} *{status}* {emoji}\n\n"
            f"_Dados em tempo real • Atualizado automaticamente_"
        )
        
        await msg.edit_text(resposta, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
        await msg.edit_text(
            "💥 *Erro inesperado*\n\n"
            "Ocorreu um problema técnico.\n"
            "Tente novamente em alguns segundos.",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula erros não tratados"""
    logger.error(f"Erro não tratado: {context.error}")

# 7. INICIALIZAÇÃO DO BOT
def main():
    """Função principal para iniciar o bot"""
    if not TELEGRAM_TOKEN:
        print("❌ ERRO: Variável MEU_TOKEN não encontrada no arquivo .env")
        print("Por favor, crie um arquivo .env com:")
        print("MEU_TOKEN=seu_token_aqui")
        exit(1)
    
    print("=" * 50)
    print("🤖 KITE BOT BRASIL - INICIANDO")
    print("=" * 50)
    print("📍 Geolocalização: Nominatim")
    print("🌤️  Meteorologia: Open-Meteo API")
    print("=" * 50)
    
    try:
        # Cria a aplicação do Telegram com timeouts configurados
        app = ApplicationBuilder() \
            .token(TELEGRAM_TOKEN) \
            .get_updates_read_timeout(30) \
            .get_updates_write_timeout(30) \
            .get_updates_connect_timeout(30) \
            .build()
        
        # Adiciona handlers de comandos
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("spots", spots))
        
        # Adiciona handler para mensagens de texto
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Adiciona handler de erros
        app.add_error_handler(error_handler)
        
        # Inicia o bot
        print("🚀 Bot iniciado com sucesso!")
        print("📲 Disponível no Telegram")
        print("🔄 Modo: Polling")
        print("=" * 50)
        print("Pressione Ctrl+C para encerrar...")
        print("=" * 50)
        
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Falha ao iniciar o bot: {e}")
        print(f"❌ Erro crítico: {e}")
        exit(1)

# 8. PONTO DE ENTRADA
if __name__ == '__main__':
    main()