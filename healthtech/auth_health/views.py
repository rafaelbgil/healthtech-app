from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AuthSerializer
from rest_framework import status
from rest_framework.response import Response

from auth_health.src.external.cognito.cognito_auth import CognitoAuth
# Create your views here.


class AuthView(APIView):
    """
    Api para autenticacao de usuario medico ou paciente
    """
    def post(self, request):
        """
        Api de autenticacao
        """
        
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            print('serializer valido')
            try:
                retorno_auth = CognitoAuth().autenticar(login=serializer.data['login'], senha=serializer.data['password'])
                return Response(data=retorno_auth, status=status.HTTP_200_OK)
            except:
                return Response(data={'Usuario ou senha invalidos'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'Usuario ou senha invalidos'}, status=status.HTTP_401_UNAUTHORIZED)
