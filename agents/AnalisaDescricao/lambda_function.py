import boto3
import os
from langchain.chat_models import ChatOpenAI
from shared.utils import get_openai_api_key

def lambda_handler(event, context):
    description = event.get("description")
    if not description:
        return {"status": "error", "message": "Descrição não fornecida"}
    
    try:
        api_key = get_openai_api_key()
        llm = ChatOpenAI(api_key=api_key, temperature=0.7)
        response = llm.predict(f"Analise a descrição: {description} e retorne requisitos estruturados.")

        if not response or not isinstance(response, str):
            return {"status": "error", "message": "Falha ao gerar requisitos"}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao processar descrição: {str(e)}"}

    # Salva no DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('DYNAMODB_TABLE'))
    table.put_item(Item={"SystemID": event['SystemID'], "Requirements": response})

    return {"status": "success", "Requirements": response}

