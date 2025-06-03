# Pilha para registrar ações
class Stack:
    """
    Implementação da estrutura de dados Pilha (LIFO - Last In First Out)
    Utilizada para registrar ações realizadas em cada missão
    """
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Adiciona um item ao topo da pilha"""
        self.items.append(item)
    
    def pop(self):
        """Remove e retorna o item do topo da pilha"""
        return self.items.pop() if self.items else None
    
    def is_empty(self):
        """Verifica se a pilha está vazia"""
        return len(self.items) == 0
    
    def __repr__(self):
        return str(self.items)

# Lista ligada para status das áreas
class AreaNode:
    """
    Nó da lista ligada que representa uma área afetada
    """
    def __init__(self, nome, status):
        self.nome = nome
        self.status = status
        self.next = None

class AreaLinkedList:
    """
    Lista ligada para gerenciar áreas afetadas com status dinâmico
    (ativo, contido, resolvido)
    """
    def __init__(self):
        self.head = None
    
    def atualizar_status(self, nome, status):
        """Atualiza o status de uma área ou adiciona se não existir"""
        node = self.head
        while node:
            if node.nome == nome:
                node.status = status
                return
            node = node.next
        
        # Área não encontrada, adicionar no início
        novo = AreaNode(nome, status)
        novo.next = self.head
        self.head = novo
    
    def get_status(self, nome):
        """Retorna o status atual de uma área"""
        node = self.head
        while node:
            if node.nome == nome:
                return node.status
            node = node.next
        return None
    
    def listar_areas(self):
        """Retorna todas as áreas e seus status"""
        areas = []
        node = self.head
        while node:
            areas.append({"nome": node.nome, "status": node.status})
            node = node.next
        return areas
    
    def __repr__(self):
        node = self.head
        out = []
        while node:
            out.append(f"{node.nome}: {node.status}")
            node = node.next
        return ' -> '.join(out)

# Árvore para hierarquia
class TreeNode:
    """
    Nó da árvore que representa hierarquia da região:
    Estado → Município → Zona Rural/Parque
    """
    def __init__(self, nome, tipo="estado"):
        self.nome = nome
        self.tipo = tipo  # "estado", "municipio", "zona"
        self.filhos = []
    
    def adicionar_filho(self, filho):
        """Adiciona um filho ao nó atual"""
        self.filhos.append(filho)
        return filho
    
    def buscar_no(self, nome):
        """Busca recursivamente um nó pelo nome"""
        if self.nome == nome:
            return self
            
        for filho in self.filhos:
            resultado = filho.buscar_no(nome)
            if resultado:
                return resultado
        
        return None
    
    def __repr__(self):
        return f"{self.nome} ({self.tipo})"
