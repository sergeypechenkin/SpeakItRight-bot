import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from telebot import TeleBot
import json
from openai import AzureOpenAI


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if req.method == 'POST':    
        update = req.get_json()
        logging.info(f'POST Update = {update}')

        try:

            if update['message']:

                username = update['message']['from']['first_name']
                user_id = update['message']['from']['id']
                chat_id = update['message']['chat']['id']
                fileprefix = f'{username}_{user_id}'
                logging.log(logging.INFO, f'User {username} with id {user_id} sent a message: {update["message"]["text"]}')
                connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
                blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
                blob_client = blob_service_client.get_blob_client("history", f'{fileprefix}_history.txt')
                
                message_next(chat_id, bot_token,update['message']['text'], fileprefix, blob_client)
                return func.HttpResponse(status_code=200)
        except Exception as e:
                logging.error(f'Oops, we got an exception in http_trigger: {e}')
                return func.HttpResponse(status_code=200)
    else:
        return func.HttpResponse("This is a bot server.", status_code=200)

def message_next(chat_id, bot_token, text, fileprefix,blob_client):
        logging.info(f'Update has a next message = {text}, fileprefix: {fileprefix}')
        bot = TeleBot(bot_token)
        conversation = []
        querry = []
        #combine history and prompt to pass to openai
        if blob_client.exists():
            if text == '/startover':
                blob_client.delete_blob()
                bot.send_message(chat_id, "Okay, let's start over")
                logging.info(f'{fileprefix}_history.txt deleted')
                return func.HttpResponse("This is a bot server.", status_code=200)
            else:
                conversation = blob_client.download_blob().readall().decode('utf-8')
                lines = conversation.split('\n')
                conversation = [json.loads(line) for line in lines]

        conversation.append({"role": "user", "content": text})
        conversation = conversation[-4:]
        with open(f'prompt_english.txt', 'r') as f:
                querry=[{"role": "system", "content": f.read().strip()}]
                querry.extend(conversation)

        logging.info(f'Conversation is ready to pass to openai = {querry}')
        response = get_response(querry)
        bot.send_message(chat_id, response, parse_mode="Markdown")
        conversation.append({"role": "assistant", "content": response})
        conversation = [json.dumps(message) for message in conversation]
        conversation = "\n".join(conversation)
        blob_client.upload_blob(conversation, overwrite=True)

def get_response(conversation):

    logging.info(f'Conversation = {conversation}')
    client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_KEY"),  
    api_version = "2023-09-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation,
)
    
    text = response.choices[0].message.content
    logging.info(f'Response = {text}')
    return text
