from estruturas import Stack, AreaLinkedList, TreeNode

class Equipe:
    """
    Classe que representa uma equipe de combate a incêndios
    """
    def __init__(self, id, nome, local, especialidade=None):
        self.id = id
        self.nome = nome
        self.local = local
        self.especialidade = especialidade
        self.acoes = Stack()
        self.disponivel = True
    
    def registrar_acao(self, acao):
        """Registra uma ação realizada pela equipe"""
        self.acoes.push(acao)
    
    def listar_acoes(self):
        """Retorna a lista de ações realizadas em ordem cronológica"""
        return self.acoes.items.copy()
    
    def to_dict(self):
        """Converte a equipe para um dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'local': self.local,
            'especialidade': self.especialidade,
            'disponivel': self.disponivel
        }

class Chamada:
    """
    Classe que representa uma chamada de emergência
    """
    def __init__(self, id, local, severidade, tipo_vegetacao, clima=None, detalhes=None):
        self.id = id
        self.local = local
        self.severidade = severidade
        self.tipo_vegetacao = tipo_vegetacao
        self.clima = clima
        self.detalhes = detalhes or {}
        self.prioridade = None
    
    @classmethod
    def from_dict(cls, data):
        """Cria uma chamada a partir de um dicionário"""
        return cls(
            id=data['id'],
            local=data['local'],
            severidade=data['severidade'],
            tipo_vegetacao=data['tipo_vegetacao'],
            clima=data.get('clima'),
            detalhes=data.get('detalhes', {})
        )
    
    def to_dict(self):
        """Converte a chamada para um dicionário"""
        return {
            'id': self.id,
            'local': self.local,
            'severidade': self.severidade,
            'tipo_vegetacao': self.tipo_vegetacao,
            'clima': self.clima,
            'prioridade': self.prioridade,
            'detalhes': self.detalhes
        }

class RegiaoBrasil:
    """Classe que representa a hierarquia geográfica de uma região do Brasil"""
    def __init__(self):
        self.root = None
        self._inicializar_regioes()
    
    def _inicializar_regioes(self):
        """Inicializa a árvore hierárquica com alguns estados e municípios"""
        self.root = TreeNode("Brasil", tipo="país")
        
        estado_sp = self.root.adicionar_filho(TreeNode("São Paulo", tipo="estado"))
        estado_mt = self.root.adicionar_filho(TreeNode("Mato Grosso", tipo="estado"))
        estado_am = self.root.adicionar_filho(TreeNode("Amazonas", tipo="estado"))
        
        sp_capital = estado_sp.adicionar_filho(TreeNode("São Paulo", tipo="município"))
        sp_capital.adicionar_filho(TreeNode("Zona Norte", tipo="zona"))
        sp_capital.adicionar_filho(TreeNode("Zona Sul", tipo="zona"))
        campinas = estado_sp.adicionar_filho(TreeNode("Campinas", tipo="município"))
        campinas.adicionar_filho(TreeNode("Mata Santa Genebra", tipo="zona"))
        
        cuiaba = estado_mt.adicionar_filho(TreeNode("Cuiabá", tipo="município"))
        cuiaba.adicionar_filho(TreeNode("Pantanal Norte", tipo="zona"))
        pocone = estado_mt.adicionar_filho(TreeNode("Poconé", tipo="município"))
        pocone.adicionar_filho(TreeNode("Mata Alta", tipo="zona"))
        
        manaus = estado_am.adicionar_filho(TreeNode("Manaus", tipo="município"))
        manaus.adicionar_filho(TreeNode("Reserva Ducke", tipo="zona"))
    
    def buscar_zona(self, nome):
        """Busca uma zona pelo nome"""
        return self.root.buscar_no(nome)
    
    def obter_hierarquia_completa(self, zona_nome):
        """Retorna a hierarquia completa de uma zona (estado -> município -> zona)"""
        no = self.buscar_zona(zona_nome)
        if not no:
            return None
        
        hierarquia = []
        atual = no
        
        while atual and atual.nome != "Brasil":
            hierarquia.append({"nome": atual.nome, "tipo": atual.tipo})
            atual = atual.pai

        hierarquia.reverse()
        return hierarquia
