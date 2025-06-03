import heapq

# Constantes para cálculo de prioridade
PESOS_VEGETACAO = {
    'cerrado': 1.2,
    'mata_atlantica': 1.5,
    'pantanal': 2.0,
    'amazonia': 1.8,
    'caatinga': 1.3
}

def calcular_prioridade(chamada):
    """
    Calcula a prioridade de atendimento de um chamado
    prioridade = severidade * peso_vegetacao
    """
    peso = PESOS_VEGETACAO.get(chamada['tipo_vegetacao'], 1.0)
    
    # Fatores adicionais que podem influenciar na prioridade
    if chamada.get('clima') == 'seco':
        severidade_ajustada = chamada['severidade'] * 1.1  # 10% a mais se o clima estiver seco
    else:
        severidade_ajustada = chamada['severidade']
    
    return severidade_ajustada * peso

def calcular_menor_caminho(grafo, origem, destino):
    """
    Implementação do algoritmo de Dijkstra para encontrar o caminho mais curto
    entre dois pontos em um grafo ponderado
    
    Args:
        grafo: dicionário representando o grafo {nó: {vizinho: peso, ...}, ...}
        origem: nó de origem
        destino: nó de destino
        
    Returns:
        (caminho, custo): tupla com a lista do caminho e o custo total
    """
    # Fila de prioridade para os nós a serem visitados: (custo, nó, caminho)
    fila = [(0, origem, [origem])]
    visitados = set()
    
    while fila:
        custo, atual, caminho = heapq.heappop(fila)
        
        # Se chegamos ao destino, retornamos o caminho e o custo
        if atual == destino:
            return caminho, custo
        
        # Evita revisitar nós
        if atual in visitados:
            continue
            
        visitados.add(atual)
        
        # Para cada vizinho, calcula o custo e adiciona à fila
        for vizinho, peso in grafo.get(atual, {}).items():
            if vizinho not in visitados:
                novo_caminho = caminho + [vizinho]
                novo_custo = custo + peso
                heapq.heappush(fila, (novo_custo, vizinho, novo_caminho))
    
    # Caso não encontre caminho
    return None, float('inf')

def sugerir_acoes(chamada):
    """
    Sugere ações baseadas nas características do chamado
    
    Args:
        chamada: dicionário com informações do chamado
        
    Returns:
        lista de ações recomendadas
    """
    acoes = []
    
    # Base: todas as chamadas precisam dessas ações
    acoes.append("Avaliação inicial da situação")
    
    # Adiciona ações específicas baseadas na vegetação
    if chamada['tipo_vegetacao'] == 'cerrado':
        acoes.append("Criar aceiro")
        acoes.append("Aplicar técnica de contra-fogo controlado")
    elif chamada['tipo_vegetacao'] == 'pantanal':
        acoes.append("Verificar áreas alagadas próximas")
        acoes.append("Proteger fauna local")
        acoes.append("Usar técnicas de combate para áreas úmidas")
    elif chamada['tipo_vegetacao'] == 'mata_atlantica':
        acoes.append("Proteção prioritária de espécies endêmicas")
        acoes.append("Aplicar barreira de contenção")
    
    # Adiciona ações específicas baseadas na severidade
    if chamada['severidade'] >= 4:
        acoes.append("Solicitar reforço aéreo")
        acoes.append("Estabelecer perímetro de segurança ampliado")
    
    # Adiciona ações específicas baseadas no clima
    if chamada.get('clima') == 'seco':
        acoes.append("Monitorar mudanças no vento")
        acoes.append("Preparar pontos de abastecimento de água")
    
    # Ação de finalização
    acoes.append("Monitoramento pós-contenção")
    
    return acoes
