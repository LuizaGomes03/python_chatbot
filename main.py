import os
import logging
from typing import List
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

def format_response(texts: List[str]) -> jsonify:
    return jsonify({"fulfillmentMessages": [{"text": {"text": texts}}]})

@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    data = request.get_json()

    # Verificar a estrutura recebida
    logger.info(f"Recebido JSON: {data}")

    action = data['queryResult'].get('action', 'Unknown Action')
    parameters = data['queryResult'].get('parameters', {})

    # Extrair callback_data corretamente da requisição do Telegram
    callback_data = data['originalDetectIntentRequest']['payload']['data']['callback_query'].get('data')

    # Usando logs ao invés de print
    logger.info(f"action: {action}")
    logger.info(f"callback_data: {callback_data}")

    # Tratar diferentes ações baseadas na intent detectada
    if action == 'defaultWelcomeIntent':
        response = format_response(['Hi, how can I help you today?'])

    elif action == 'input.welcome':
        response = format_response(['testando resposta', 'apareceu aii?'])

    elif action == 'teste.action':
        if callback_data == 'Contato_Poupatempo':
            response = format_response(['Você pode entrar em contato pelo telefone: (XX) XXXX-XXXX.'])
        elif callback_data == 'Endereço':
            response = format_response(['Nosso endereço é: Rua Exemplo, 123 - Cidade - Estado.'])
        elif callback_data == 'Horário de funcionamento do Poupatempo':
            response = format_response(['O horário de funcionamento é: 8h às 18h de segunda a sexta.'])
        else:
            logger.warning(f'callback_data não reconhecido: {callback_data}')
            response = format_response(['Nenhuma opção válida foi selecionada.'])

    elif action == 'shopping.action':
        if callback_data == 'Contato_Shopping':
            response = format_response(['Você pode entrar em contato pelo telefone: (XX) XXXX-XXXX.'])
        elif callback_data == 'Endereço':
            response = format_response(['Nosso endereço é: Rua Exemplo, 123 - Cidade - Estado.'])
        elif callback_data == 'Horario de funcionamento do shopping':
            response = format_response(['O horário de funcionamento é: 8h às 18h de segunda a sexta.'])
        else:
            logger.warning(f'callback_data não reconhecido: {callback_data}')
            response = format_response(['Nenhuma opção válida foi selecionada.'])

    elif action == 'acessibilidade.action':
        if callback_data == 'Acessibilidade Shopping':
            response = format_response(['Você pode entrar em contato pelo telefone: (XX) XXXX-XXXX.'])
        elif callback_data == 'Acessibilidade Poupatempo':
            response = format_response(['Nosso endereço é: Rua Exemplo, 123 - Cidade - Estado.'])
        else:
            logger.warning(f'callback_data não reconhecido: {callback_data}')
            response = format_response(['Nenhuma opção válida foi selecionada.'])


    elif action == 'inputUnknown':
        response = format_response(['Sorry, I did not understand that clearly.'])

    else:
        response = format_response([f'No handler for the action name {action}.'])

    return response

if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)
