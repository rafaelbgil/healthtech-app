from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AuthSerializer
from rest_framework import status
from rest_framework.response import Response
from medico.models import PerfilMedico
from paciente.models import PerfilPaciente

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
            try:
                if serializer.data['login'][0].isnumeric():
                    PerfilPaciente.objects.get(email=serializer.data['email'])
                else:
                    print('passou aqui')
                    PerfilMedico.objects.get(email=serializer.data['email'])

                retorno_auth = CognitoAuth().autenticar(
                    login=serializer.data['login'], senha=serializer.data['password'])
                print(retorno_auth)
                return Response(data=retorno_auth, status=status.HTTP_200_OK)
            except Exception as e:
                print(e.__str__())
                return Response(data={'Usuario ou senha invalidos'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'Usuario ou senha invalidos'}, status=status.HTTP_401_UNAUTHORIZED)
