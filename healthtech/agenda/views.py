from rest_framework.views import APIView
from .serializers import AgendaSerializer
from rest_framework import status
from rest_framework.response import Response

from auth_health.src.utils.validar_permissoes import validar_permissoes
from agenda.models import Agenda
from paciente.models import PerfilPaciente
from agenda.serializers import AgendaSerializer


# Create your views here.


class AgendaFindByEspecialidadeView(APIView):
    """
    Api consulta de agendamentos disponiveis por especialidade
    """

    def get(self, request, especialidade):
        """
        Api para obter informacoes de agendamentos por especialidade
        """
        try:
            informacoes_token = validar_permissoes(
                request=request, role='paciente')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)
        try:
            agenda = Agenda.objects.filter(
                especialidade=especialidade, status='disponivel')
            serializer = AgendaSerializer(instance=agenda, many=True)
            if not agenda:
                return Response(data={"message": "Nenhum agendamento disponivel."}, status=status.HTTP_404_NOT_FOUND)
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={"message": "Erro ao realizar consulta"}, status=status.HTTP_404_NOT_FOUND)


class AgendaReservarView(APIView):
    """
    Api para reservar agendamento
    """

    def post(self, request, uuid):
        """
        Api para realizar reserva de agendamento disponivel
        """
        try:
            informacoes_token = validar_permissoes(
                request=request, role='paciente')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)

        agenda = Agenda.objects.get(uuid=uuid)

        if agenda.status != "disponivel":
            return Response(data={"message": "Não é possível reserva uma agenda que não esteja com status 'disponível'."}, status=status.HTTP_404_NOT_FOUND)
        
        paciente = PerfilPaciente.objects.get(uuid=informacoes_token['uuid_user'])
        agenda.status = 'aguardando_confirmacao'
        agenda.uuid_paciente = informacoes_token['uuid_user']
        agenda.nome_paciente = paciente.nome
        agenda.save()
        serializer = AgendaSerializer(instance=agenda)
        return Response(data=serializer.data, status=status.HTTP_200_OK)