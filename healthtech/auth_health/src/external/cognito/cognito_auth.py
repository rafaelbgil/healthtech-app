import boto3
from os import environ
import hmac, hashlib, base64
import jwt



class CognitoAuth():
    def __init__(self) -> None:
        self.aws_client = boto3.client('cognito-idp')

    
    def autenticar(self, login: str, senha: str) -> dict:
        client_id = environ.get('COGNITO_CLIENT_ID')
        message = bytes(login + client_id, 'utf-8')
        key = bytes(environ.get('COGNITO_CLIENT_SECRET'), 'utf-8')
        secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()
        try:
            return self.aws_client.initiate_auth(
                ClientId=client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    "USERNAME": login,
                    "PASSWORD": senha,
                    "SECRET_HASH": secret_hash
                }
            )

        except:
            raise Exception('Usuario ou senha invalidos')
    
    def validar_token(self, token: str):
        try:
            token_validado = self.aws_client.get_user(AccessToken=token)
            #obtendo e-mail
            email = ''
            for registro in token_validado['UserAttributes']:
                if registro['Name'] == 'email':
                    email = registro['Value']

            token_decodificado = jwt.decode(token, options={"verify_signature": False})
            print(token_decodificado)
            informacoes = {
                "username" : token_validado['Username'],
                "email" : email,
                "uuid_user" : token_decodificado['sub'],
                "grupos" : token_decodificado['cognito:groups'],
                "token" : token
            }
        except Exception as e:
            raise Exception('Token invalido')
        return informacoes
