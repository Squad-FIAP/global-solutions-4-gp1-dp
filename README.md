# Sistema Inteligente de Combate a Queimadas

Sistema em Python que implementa um centro de controle inteligente para organização e gestão de combate a focos de incêndio em florestas e áreas de vegetação.

## Estruturas de Dados Utilizadas

- **Fila (Queue)**: Organiza chamadas de emergência por ordem de chegada
- **Heap**: Reorganiza os chamados por prioridade, baseado na severidade e tipo de vegetação
- **Pilha (Stack)**: Registra o histórico de ações realizadas por equipe em cada missão
- **Lista Ligada**: Gerencia áreas afetadas com status dinâmico (ativo, contido, resolvido)
- **Árvore**: Representa a hierarquia de regiões (Estado → Município → Zona Rural/Parque)
- **Grafo**: Representa o mapa com locais conectados por estradas, para cálculo de rotas otimizadas

## Organização do Código

O projeto está estruturado nos seguintes arquivos:

- **estruturas.py**: Implementação das estruturas de dados básicas (Pilha, Lista Ligada, Árvore)
- **algoritmos.py**: Implementação dos algoritmos de cálculo de prioridade e caminhos mínimos
- **modelos.py**: Classes que representam os elementos do sistema (Chamada, Equipe, Região)
- **central.py**: Classe principal que gerencia todo o sistema
- **main.py**: Demonstração do funcionamento do sistema

## Funcionamento

1. O sistema recebe chamadas de emergência, cada uma com informações sobre o local, severidade e tipo de vegetação.
2. As chamadas são organizadas em uma fila de prioridade (heap) com base na severidade e tipo de vegetação.
3. Para cada chamada, o sistema designa a equipe disponível mais adequada.
4. O sistema calcula a rota mais eficiente até o local do incêndio usando o algoritmo de Dijkstra.
5. Com base nas características do incêndio, o sistema sugere ações apropriadas.
6. O status das áreas afetadas é registrado e atualizado.

## Uso Básico

```python
# Importa a central de queimadas
from central import CentralQueimadas

# Cria um mapa (grafo) representando estradas e locais
mapa = {
    "Base Central": {"Zona Norte": 10, "Mata Alta": 12},
    "Zona Norte": {"Mata Alta": 7},
    "Mata Alta": {"Zona Norte": 7}
}

# Inicializa a central
central = CentralQueimadas(mapa)

# Adiciona equipes
central.adicionar_equipe({
    'id': 1, 
    'nome': 'Equipe Alfa', 
    'local': 'Base Central',
    'especialidade': 'combate terrestre'
})

# Recebe chamados
central.receber_chamada({
    'id': 1, 
    'local': 'Zona Norte', 
    'severidade': 4, 
    'tipo_vegetacao': 'cerrado', 
    'clima': 'seco'
})

# Organiza por prioridade e atende chamados
central.organizar_prioridade()
resultado = central.atender_proxima_chamada()
print(resultado)
```

## Execução

Para executar o sistema de demonstração, execute o arquivo `main.py`:

```
python3 main.py
```
