from collections import Counter
import json
import datetime

class RelatorioQueimadas:
    """
    Classe para geração de relatórios estatísticos do sistema de combate a queimadas
    """
    def __init__(self, central):
        self.central = central
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def estatisticas_gerais(self):
        """
        Gera estatísticas gerais do sistema
        """
        chamadas_atendidas = self.central.chamadas_atendidas
        equipes = self.central.equipes
        areas = self.central.obter_status_areas()
        
        tipos_vegetacao = [chamada['prioridade'] for chamada in chamadas_atendidas]
        media_prioridade = sum(tipos_vegetacao) / len(tipos_vegetacao) if tipos_vegetacao else 0
        
        status_areas = Counter([area['status'] for area in areas])
        
        acoes_realizadas = []
        for chamada in chamadas_atendidas:
            acoes_realizadas.extend(chamada['acao'])
        
        contagem_acoes = Counter(acoes_realizadas)
        
        equipes_disponiveis = sum(1 for eq in equipes if eq.disponivel)
        
        estatisticas = {
            "data_relatorio": self.timestamp,
            "chamadas_atendidas": len(chamadas_atendidas),
            "media_prioridade": round(media_prioridade, 2),
            "status_areas": dict(status_areas),
            "top_acoes": contagem_acoes.most_common(3),
            "equipes_disponiveis": equipes_disponiveis,
            "total_equipes": len(equipes)
        }
        
        return estatisticas
    
    def gerar_relatorio_texto(self):
        """
        Gera um relatório em formato de texto
        """
        stats = self.estatisticas_gerais()
        
        relatorio = [
            "========================================",
            "  RELATÓRIO DO SISTEMA DE COMBATE A QUEIMADAS",
            f"  {stats['data_relatorio']}",
            "========================================",
            "",
            f"Total de chamadas atendidas: {stats['chamadas_atendidas']}",
            f"Prioridade média: {stats['media_prioridade']}",
            "",
            "Status das áreas:",
        ]
        
        for status, count in stats['status_areas'].items():
            relatorio.append(f"  - {status}: {count}")
        
        relatorio.append("")
        relatorio.append("Ações mais frequentes:")
        
        for acao, count in stats['top_acoes']:
            relatorio.append(f"  - {acao}: {count}")
        
        relatorio.append("")
        relatorio.append(f"Equipes disponíveis: {stats['equipes_disponiveis']} de {stats['total_equipes']}")
        relatorio.append("")
        
        if stats['chamadas_atendidas'] > 0:
            chamadas = self.central.chamadas_atendidas
            relatorio.append("Resumo das chamadas atendidas:")
            
            for i, chamada in enumerate(chamadas, 1):
                relatorio.append(f"  {i}. ID: {chamada['ocorrencia_id']}")
                relatorio.append(f"     Prioridade: {chamada['prioridade']:.2f}")
                relatorio.append(f"     Equipe: {chamada['equipe']['nome']}")
                relatorio.append(f"     Tempo de deslocamento: {chamada['tempo_estimado']} minutos")
                relatorio.append("")
        
        relatorio.append("========================================")
        
        return "\n".join(relatorio)
    
    def salvar_relatorio_json(self, arquivo="relatorio_queimadas.json"):
        """
        Salva o relatório em formato JSON
        """
        stats = self.estatisticas_gerais()
        chamadas = [
            {
                "id": c['ocorrencia_id'],
                "prioridade": c['prioridade'],
                "equipe": c['equipe']['nome'],
                "tempo": c['tempo_estimado'],
                "acoes": len(c['acao'])
            }
            for c in self.central.chamadas_atendidas
        ]
        
        dados = {
            "estatisticas": stats,
            "chamadas": chamadas
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        return arquivo
from collections import Counter
import json
import datetime

class RelatorioQueimadas:
    """
    Classe para geração de relatórios estatísticos do sistema de combate a queimadas
    """
    def __init__(self, central):
        self.central = central
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def estatisticas_gerais(self):
        """
        Gera estatísticas gerais do sistema
        """
        chamadas_atendidas = self.central.chamadas_atendidas
        equipes = self.central.equipes
        areas = self.central.obter_status_areas()
        
        tipos_vegetacao = [chamada['prioridade'] for chamada in chamadas_atendidas]
        media_prioridade = sum(tipos_vegetacao) / len(tipos_vegetacao) if tipos_vegetacao else 0
        
        status_areas = Counter([area['status'] for area in areas])
        
        acoes_realizadas = []
        for chamada in chamadas_atendidas:
            acoes_realizadas.extend(chamada['acao'])
        
        contagem_acoes = Counter(acoes_realizadas)
        
        equipes_disponiveis = sum(1 for eq in equipes if eq.disponivel)
        
        estatisticas = {
            "data_relatorio": self.timestamp,
            "chamadas_atendidas": len(chamadas_atendidas),
            "media_prioridade": round(media_prioridade, 2),
            "status_areas": dict(status_areas),
            "top_acoes": contagem_acoes.most_common(3),
            "equipes_disponiveis": equipes_disponiveis,
            "total_equipes": len(equipes)
        }
        
        return estatisticas
    
    def gerar_relatorio_texto(self):
        """
        Gera um relatório em formato de texto
        """
        stats = self.estatisticas_gerais()
        
        relatorio = [
            "========================================",
            "  RELATÓRIO DO SISTEMA DE COMBATE A QUEIMADAS",
            f"  {stats['data_relatorio']}",
            "========================================",
            "",
            f"Total de chamadas atendidas: {stats['chamadas_atendidas']}",
            f"Prioridade média: {stats['media_prioridade']}",
            "",
            "Status das áreas:",
        ]
        
        for status, count in stats['status_areas'].items():
            relatorio.append(f"  - {status}: {count}")
        
        relatorio.append("")
        relatorio.append("Ações mais frequentes:")
        
        for acao, count in stats['top_acoes']:
            relatorio.append(f"  - {acao}: {count}")
        
        relatorio.append("")
        relatorio.append(f"Equipes disponíveis: {stats['equipes_disponiveis']} de {stats['total_equipes']}")
        relatorio.append("")
        
        if stats['chamadas_atendidas'] > 0:
            chamadas = self.central.chamadas_atendidas
            relatorio.append("Resumo das chamadas atendidas:")
            
            for i, chamada in enumerate(chamadas, 1):
                relatorio.append(f"  {i}. ID: {chamada['ocorrencia_id']}")
                relatorio.append(f"     Prioridade: {chamada['prioridade']:.2f}")
                relatorio.append(f"     Equipe: {chamada['equipe']['nome']}")
                relatorio.append(f"     Tempo de deslocamento: {chamada['tempo_estimado']} minutos")
                relatorio.append("")
        
        relatorio.append("========================================")
        
        return "\n".join(relatorio)
    
    def salvar_relatorio_json(self, arquivo="relatorio_queimadas.json"):
        """
        Salva o relatório em formato JSON
        """
        stats = self.estatisticas_gerais()
        chamadas = [
            {
                "id": c['ocorrencia_id'],
                "prioridade": c['prioridade'],
                "equipe": c['equipe']['nome'],
                "tempo": c['tempo_estimado'],
                "acoes": len(c['acao'])
            }
            for c in self.central.chamadas_atendidas
        ]
        
        dados = {
            "estatisticas": stats,
            "chamadas": chamadas
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        return arquivo
