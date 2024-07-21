from rest_framework import status
from rest_framework.response import Response

from auth_health.src.external.cognito.cognito_auth import CognitoAuth

def validar_permissoes(request, role: str = 'medico'):
    try:
        if 'Bearer' in request.META.get('HTTP_AUTHORIZATION'):
                header = request.META.get('HTTP_AUTHORIZATION')
                token = header.split(" ")[1]
                try:
                    cognito_cliente = CognitoAuth()
                    token_validado = cognito_cliente.validar_token(token)
                    if role not in token_validado['grupos']:
                        raise Exception(f'Permissao invalida, nao possui a role {role}')
                    else:
                         return token_validado
                except:
                    raise Exception('Token invalido')
    except:
        raise Exception('Token invalido ou ausente')