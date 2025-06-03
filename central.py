import heapq
from collections import deque
from estruturas import AreaLinkedList
from algoritmos import calcular_prioridade, calcular_menor_caminho, sugerir_acoes
from modelos import Chamada, Equipe, RegiaoBrasil

class CentralQueimadas:
    """
    Classe principal que gerencia o sistema de combate a queimadas
    """
    def __init__(self, mapa, equipes=None):
        """
        Inicializa a Central de Queimadas
        
        Args:
            mapa: dicionário representando o grafo de locais e estradas
            equipes: lista de equipes disponíveis
        """
        self.mapa = mapa
        self.equipes = equipes or []
        self.fila_chamadas = deque()  # Fila por ordem de chegada
        self.heap_prioridade = []  # Heap para priorização
        self.areas = AreaLinkedList()  # Status das áreas
        self.regiao = RegiaoBrasil()  # Hierarquia geográfica
        self.chamadas_atendidas = []  # Histórico
    
    def adicionar_equipe(self, equipe):
        """Adiciona uma equipe à central"""
        if isinstance(equipe, dict):
            equipe = Equipe(
                id=equipe['id'], 
                nome=equipe['nome'], 
                local=equipe['local'], 
                especialidade=equipe.get('especialidade')
            )
        self.equipes.append(equipe)
    
    def receber_chamada(self, chamada):
        """Recebe uma nova chamada de emergência e adiciona à fila"""
        if isinstance(chamada, dict):
            chamada = Chamada.from_dict(chamada)
        self.fila_chamadas.append(chamada)
    
    def organizar_prioridade(self):
        """Reorganiza os chamados por prioridade utilizando um heap"""
        self.heap_prioridade = []
        
        for chamada in self.fila_chamadas:
            prioridade = calcular_prioridade(chamada.to_dict())
            chamada.prioridade = prioridade
            # Negativo pois heapq é um min-heap e queremos um max-heap
            heapq.heappush(self.heap_prioridade, (-prioridade, chamada))
    
    def atender_proxima_chamada(self):
        """Atende a próxima chamada de maior prioridade"""
        if not self.heap_prioridade:
            return None
            
        if not any(equipe.disponivel for equipe in self.equipes):
            return {"erro": "Todas as equipes estão ocupadas"}
        
        _, chamada = heapq.heappop(self.heap_prioridade)
        
        # Encontra a primeira equipe disponível
        equipe = next((eq for eq in self.equipes if eq.disponivel), None)
        if not equipe:
            # Recolocar a chamada no heap
            heapq.heappush(self.heap_prioridade, (-chamada.prioridade, chamada))
            return {"erro": "Sem equipes disponíveis"}
        
        # Marca a equipe como indisponível
        equipe.disponivel = False
        
        # Calcula o melhor caminho
        caminho, tempo = calcular_menor_caminho(self.mapa, equipe.local, chamada.local)
        
        # Se não encontrou caminho, cria um caminho direto (para fins de demonstração)
        if not caminho:
            caminho = [equipe.local, chamada.local]
            tempo = 30  # tempo estimado padrão
            
        # Sugere ações para esta ocorrência
        acoes = sugerir_acoes(chamada.to_dict())
        
        # Registra as ações na pilha da equipe
        for acao in acoes:
            equipe.registrar_acao(acao)
        
        # Atualiza o status da área
        self.areas.atualizar_status(chamada.local, "controle em andamento")
        
        # Formata o resultado
        resultado = {
            'ocorrencia_id': chamada.id,
            'prioridade': chamada.prioridade,
            'equipe': equipe.to_dict(),
            'acao': acoes,
            'rota': caminho,
            'tempo_estimado': tempo,
            'status_area': "controle em andamento"
        }
        
        # Atualiza a localização da equipe
        equipe.local = chamada.local
        
        # Adiciona ao histórico de atendimentos
        self.chamadas_atendidas.append(resultado)
        
        return resultado
    
    def atender_todas_chamadas(self):
        """Atende todas as chamadas pendentes"""
        resultados = []
        
        # Organiza as chamadas por prioridade
        self.organizar_prioridade()
        
        # Atende cada chamada na ordem de prioridade
        while self.heap_prioridade:
            resultado = self.atender_proxima_chamada()
            if resultado and not resultado.get('erro'):
                resultados.append(resultado)
        
        return resultados
    
    def liberar_equipe(self, equipe_id):
        """Marca uma equipe como disponível novamente"""
        for equipe in self.equipes:
            if equipe.id == equipe_id:
                equipe.disponivel = True
                return True
        return False
    
    def atualizar_status_area(self, local, status):
        """Atualiza o status de uma área"""
        self.areas.atualizar_status(local, status)
        
    def obter_status_areas(self):
        """Retorna o status de todas as áreas"""
        return self.areas.listar_areas()
    
    def estatisticas(self):
        """Retorna estatísticas de atendimento"""
        total_chamadas = len(self.chamadas_atendidas)
        areas_por_status = {}
        areas = self.areas.listar_areas()
        
        for area in areas:
            status = area['status']
            areas_por_status[status] = areas_por_status.get(status, 0) + 1
        
        return {
            'total_chamadas_atendidas': total_chamadas,
            'areas_por_status': areas_por_status
        }
