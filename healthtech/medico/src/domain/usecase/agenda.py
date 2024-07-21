import datetime

class AgendaMedico:
    @staticmethod
    def validar_data_disponivel(data_inicio: datetime.datetime | str, agendamentos_cadastrados: list = None) -> bool:
        if not isinstance(data_inicio, datetime.datetime):
            data_inicio = datetime.datetime.fromisoformat(data_inicio)
        data_inicio_timestamp = int(data_inicio.timestamp())
        data_fim_timestamp = data_inicio_timestamp + 3000

        for agendamento in agendamentos_cadastrados:
            #verifica se esta no formato dateutil e converte para timestamp
            if isinstance(agendamento['data_inicio'],datetime.datetime):
                agendamento['data_inicio'] = int(agendamento['data_inicio'].timestamp())
            if isinstance(agendamento['data_fim'],datetime.datetime):
                agendamento['data_fim'] = int(agendamento['data_fim'].timestamp())

            if data_inicio_timestamp >= agendamento['data_inicio'] and data_inicio_timestamp <= agendamento['data_fim']:
                return False
            if data_fim_timestamp >= agendamento['data_inicio'] and data_fim_timestamp <= agendamento['data_fim']:
                return False 
            
        return True