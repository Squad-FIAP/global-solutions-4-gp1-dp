from central import CentralQueimadas
from modelos import Equipe, Chamada

def main():
    """Função principal de demonstração do sistema"""
    # Mapa de exemplo (grafo representando locais e estradas)
    mapa = {
        "Base Central": {"Zona Norte": 10, "Mata Alta": 12, "Vila Verde": 5},
        "Zona Norte": {"Base Central": 10, "Mata Alta": 7},
        "Vila Verde": {"Base Central": 5, "Mata Alta": 3},
        "Mata Alta": {"Zona Norte": 7, "Vila Verde": 3},
        "Pantanal Norte": {"Base Central": 20, "Reserva Ducke": 30},
        "Reserva Ducke": {"Pantanal Norte": 30}
    }
    
    # Criação da central
    central = CentralQueimadas(mapa)
    
    # Adiciona equipes
    central.adicionar_equipe(Equipe(1, "Equipe Alfa", "Base Central", "combate terrestre"))
    central.adicionar_equipe(Equipe(2, "Equipe Beta", "Base Central", "avaliação aérea"))
    central.adicionar_equipe(Equipe(3, "Equipe Gama", "Vila Verde", "resgate fauna"))
    
    # Recebe chamadas de emergência
    chamadas = [
        {
            "id": 1, 
            "local": "Zona Norte", 
            "severidade": 4, 
            "tipo_vegetacao": "cerrado", 
            "clima": "seco",
            "detalhes": {"risco_habitacoes": True}
        },
        {
            "id": 2, 
            "local": "Mata Alta", 
            "severidade": 5, 
            "tipo_vegetacao": "pantanal", 
            "clima": "seco",
            "detalhes": {"area_estimada": "100ha"}
        },
        {
            "id": 3, 
            "local": "Pantanal Norte", 
            "severidade": 3, 
            "tipo_vegetacao": "pantanal", 
            "clima": "umido"
        },
        {
            "id": 4, 
            "local": "Reserva Ducke", 
            "severidade": 5, 
            "tipo_vegetacao": "amazonia", 
            "clima": "seco"
        }
    ]
    
    for chamada in chamadas:
        central.receber_chamada(chamada)
    
    # Inicia o atendimento de chamadas em ordem de prioridade
    print("===== SISTEMA DE COMBATE A QUEIMADAS =====")
    print("Processando chamadas...")
    
    central.organizar_prioridade()
    
    # Atende cada chamada em ordem de prioridade
    while central.heap_prioridade:
        resultado = central.atender_proxima_chamada()
        if resultado and not resultado.get('erro'):
            print("\n===== CHAMADA ATENDIDA =====")
            print(f"ID da Ocorrência: {resultado['ocorrencia_id']}")
            print(f"Prioridade: {resultado['prioridade']:.2f}")
            print(f"Equipe designada: {resultado['equipe']['nome']}")
            print(f"Rota: {' -> '.join(resultado['rota'])}")
            print(f"Tempo estimado: {resultado['tempo_estimado']} minutos")
            print("Ações a serem tomadas:")
            for i, acao in enumerate(resultado['acao'], 1):
                print(f"  {i}. {acao}")
            print(f"Status da área: {resultado['status_area']}")
            
            # Para fins de demonstração, liberamos a equipe após cada atendimento
            central.liberar_equipe(resultado['equipe']['id'])
            
            # Vamos atualizar o status de algumas áreas conforme o progresso
            if resultado['ocorrencia_id'] == 1:
                central.atualizar_status_area("Zona Norte", "controlado")
            elif resultado['ocorrencia_id'] == 2:
                central.atualizar_status_area("Mata Alta", "em contenção")
        
        elif resultado and resultado.get('erro'):
            print(f"Erro: {resultado['erro']}")
            break
    
    # Estatísticas finais
    print("\n===== ESTATÍSTICAS =====")
    stats = central.estatisticas()
    print(f"Total de chamadas atendidas: {stats['total_chamadas_atendidas']}")
    print("Status das áreas:")
    for status, count in stats['areas_por_status'].items():
        print(f"  {status}: {count} área(s)")
    
    # Status atual de todas as áreas
    print("\n===== STATUS DAS ÁREAS =====")
    print(central.areas)

if __name__ == "__main__":
    main()
