from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MedicoAgendaSerializer
from rest_framework import status
from rest_framework.response import Response

from auth_health.src.utils.validar_permissoes import validar_permissoes
from medico.src.domain.usecase.agenda import AgendaMedico
from agenda.models import Agenda
from django.db.models import Q
from medico.models import PerfilMedico
from agenda.serializers import AgendaSerializer
# Create your views here.


class MedicoAgendaView(APIView):
    """
    Api gerenciamento de agenda do medico
    """

    def get(self, request):
        """
        Lista agendamentos do médico
        """
        try:
            informacoes_token = validar_permissoes(
                request=request, role='medico')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)

        lista_agendamentos = Agenda.objects.filter(
            uuid_medico=informacoes_token['uuid_user'])

        agenda_serializar = AgendaSerializer(lista_agendamentos, many=True)

        return Response(data=agenda_serializar.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Criar agendamento disponivel
        """
        serializer = MedicoAgendaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            informacoes_token = validar_permissoes(
                request=request, role='medico')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)

        lista_agendamentos = Agenda.objects.filter(uuid_medico=informacoes_token['uuid_user']).filter(
            Q(status="disponivel") | Q(status="aguardando_confirmacao") | Q(status="confirmada"))

        agenda_medico = AgendaMedico()
        agenda_disponivel = agenda_medico.validar_data_disponivel(
            data_inicio=request.data['data_inicio'], agendamentos_cadastrados=lista_agendamentos)

        if not agenda_disponivel:
            return Response(data={"erro": "Já existe um agendamento nesse horario"})

        medico = PerfilMedico.objects.get(uuid=informacoes_token['uuid_user'])

        agenda = Agenda()
        agenda.data_inicio = agenda_disponivel[0]
        agenda.data_fim = agenda_disponivel[1]
        agenda.uuid_medico = medico.uuid
        agenda.nome_medico = medico.nome
        agenda.valor_consulta = medico.valor_consulta
        agenda.especialidade = medico.especialidade

        agenda_serializer = AgendaSerializer(instance=agenda)

        try:
            agenda.save()
            return Response(data=agenda_serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data="nao foi possivel cadastrar agenda", status=status.HTTP_400_FORBIDDEN)


class MedicoAgendaDetalhesView(APIView):
    """
    Api gerenciamento de agenda do medico
    """

    def get(self, request, uuid):
        """
        Api para obter informacoes de agendamento
        """
        try:
            informacoes_token = validar_permissoes(
                request=request, role='medico')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)
        try:
            agenda = Agenda.objects.get(
                uuid=uuid, uuid_medico=informacoes_token['uuid_user'])
            serializer = AgendaSerializer(instance=agenda)
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={"message": "Consulta nao encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Api para alterar agendamento
        """
        try:
            informacoes_token = validar_permissoes(
                request=request, role='medico')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)
        try:
            agenda = Agenda.objects.get(
                uuid=uuid, uuid_medico=informacoes_token['uuid_user'])
            
            if agenda.status != 'disponivel':
                return Response(data={"message": "Só é possível alterar agendas que se encontram com o status 'disponivel'."}, status=status.HTTP_400_BAD_REQUEST)

            lista_agendamentos = Agenda.objects.filter(uuid_medico=informacoes_token['uuid_user']).filter(Q(status="disponivel") | Q(status="confirmada") | Q(status="aguardando_confirmacao")).filter(~Q(uuid=uuid))

            agenda_medico=AgendaMedico()
            agenda_disponivel=agenda_medico.validar_data_disponivel(
                data_inicio=request.data['data_inicio'], agendamentos_cadastrados=lista_agendamentos)

            if not agenda_disponivel:
                return Response(data={"erro": "Já existe um agendamento nesse horario"})

            agenda.data_inicio=agenda_disponivel[0]
            agenda.data_fim=agenda_disponivel[1]
            agenda.save()
            serializer=AgendaSerializer(instance=agenda)
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={"message": "Consulta nao encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Api para cancelar agendamento
        """
        try:
            informacoes_token=validar_permissoes(
                request=request, role='medico')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)
        try:
            agenda=Agenda.objects.get(
                uuid=uuid, uuid_medico=informacoes_token['uuid_user'])
            if agenda.status == 'cancelada' or agenda.status == 'realizada':
                return Response(data={"message": "Nao e possivel alterar status de agendas finalizadas ou canceladas"}, status=status.HTTP_400_BAD_REQUEST)

            agenda.status='cancelada'
            agenda.save()
            serializer=AgendaSerializer(instance=agenda)
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={"message": "Consulta nao encontrada"}, status=status.HTTP_404_NOT_FOUND)


class MedicoAgendaConfirmarView(APIView):
    def post(self, request, uuid):
        """
        Api para confirmar agendamento
        """
        try:
            informacoes_token=validar_permissoes(
                request=request, role='medico')
        except Exception as e:
            return Response(data=e.__str__(), status=status.HTTP_403_FORBIDDEN)
        try:
            agenda=Agenda.objects.get(
                uuid=uuid, uuid_medico=informacoes_token['uuid_user'])
            if agenda.status != 'aguardando_confirmacao':
                return Response(data={"message": "Só é possível alterar o status para consulta confirmada após algum cliente solicitar agenda."}, status=status.HTTP_400_BAD_REQUEST)

            agenda.status='confirmada'
            agenda.save()
            serializer=AgendaSerializer(instance=agenda)
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={"message": "Consulta nao encontrada"}, status=status.HTTP_404_NOT_FOUND)
