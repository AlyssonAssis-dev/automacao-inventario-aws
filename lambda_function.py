import json
import boto3
import uuid
import urllib.parse

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
tabela = dynamodb.Table('Inventario_Equipamentos')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    response = s3.get_object(Bucket=bucket, Key=key)
    conteudo = response['Body'].read().decode('utf-8')
    linhas = conteudo.split('\n')
    
    for linha in linhas:
        if linha.strip():
            partes = linha.split(',')
            item_formatado = {
                'ID_Equipamentos': str(uuid.uuid4()),
                'Codigo_Ativo': partes[0].strip() if len(partes) > 0 else "N/A",
                'Descricao_Local': partes[1].strip() if len(partes) > 1 else "N/A",
                'Status_Operacional': partes[2].strip() if len(partes) > 2 else "N/A",
                'Tensao_KV': partes[3].strip() if len(partes) > 3 else "N/A",
                'Arquivo_Origem': key
            }
            tabela.put_item(Item=item_formatado)
            
    return {'statusCode': 200, 'body': 'Sucesso'}
