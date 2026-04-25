"""
Gerador de Relatório HTML — cria um relatório visual com os produtos encontrados.
Estilo visual inspirado no gerar_relatorio.py do projeto ia-survey do Thiago.
"""

from datetime import datetime
from typing import List, Dict


class GeradorRelatorio:

    def gerar_html(self, produtos: List[Dict], termos_buscados: List[str]) -> str:
        """Gera relatório HTML completo com os produtos pontuados."""

        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        campeoes = [p for p in produtos if p["score"] >= 80]
        boas_oportunidades = [p for p in produtos if 60 <= p["score"] < 80]

        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Market Hunter — Relatório</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #0f0f1a; color: #e0e0e0; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 40px; text-align: center; border-bottom: 2px solid #00d4ff; }}
        .header h1 {{ font-size: 2.5em; color: #00d4ff; }}
        .header p {{ color: #aaa; margin-top: 8px; }}
        .resumo {{ display: flex; gap: 20px; padding: 30px; justify-content: center; flex-wrap: wrap; }}
        .card {{ background: #1a1a2e; border-radius: 12px; padding: 24px; text-align: center; min-width: 160px; border: 1px solid #333; }}
        .card .numero {{ font-size: 2.5em; font-weight: bold; color: #00d4ff; }}
        .card .label {{ color: #aaa; margin-top: 6px; font-size: 0.9em; }}
        .secao {{ padding: 20px 30px; }}
        .secao h2 {{ font-size: 1.4em; color: #00d4ff; margin-bottom: 16px; border-bottom: 1px solid #333; padding-bottom: 8px; }}
        .produto {{ background: #1a1a2e; border-radius: 10px; padding: 20px; margin-bottom: 16px; border-left: 4px solid #00d4ff; display: flex; gap: 16px; align-items: flex-start; }}
        .produto.campiao {{ border-left-color: #ff6b35; }}
        .produto img {{ width: 80px; height: 80px; object-fit: cover; border-radius: 8px; background: #333; }}
        .produto-info {{ flex: 1; }}
        .produto-info h3 {{ font-size: 1em; color: #fff; margin-bottom: 8px; }}
        .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold; margin-bottom: 8px; }}
        .badge.campiao {{ background: #ff6b35; color: #fff; }}
        .badge.boa {{ background: #00c853; color: #fff; }}
        .badge.media {{ background: #ffa000; color: #000; }}
        .badge.ruim {{ background: #e53935; color: #fff; }}
        .meta {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: 0.85em; color: #aaa; margin-top: 6px; }}
        .meta span {{ color: #00d4ff; font-weight: bold; }}
        .score-bar {{ background: #333; border-radius: 10px; height: 8px; margin-top: 10px; }}
        .score-fill {{ height: 8px; border-radius: 10px; background: linear-gradient(90deg, #00d4ff, #ff6b35); }}
        .btn {{ display: inline-block; margin-top: 10px; padding: 6px 14px; background: #00d4ff22; border: 1px solid #00d4ff; color: #00d4ff; border-radius: 6px; text-decoration: none; font-size: 0.85em; }}
        .footer {{ text-align: center; padding: 30px; color: #555; border-top: 1px solid #222; margin-top: 30px; }}
    </style>
</head>
<body>

<div class="header">
    <h1>🔍 Market Hunter</h1>
    <p>Relatório gerado em {data_hora} | Termos pesquisados: {', '.join(termos_buscados)}</p>
</div>

<div class="resumo">
    <div class="card"><div class="numero">{len(produtos)}</div><div class="label">Produtos Analisados</div></div>
    <div class="card"><div class="numero" style="color:#ff6b35">{len(campeoes)}</div><div class="label">🔥 Campeões</div></div>
    <div class="card"><div class="numero" style="color:#00c853">{len(boas_oportunidades)}</div><div class="label">✅ Boas Oportunidades</div></div>
    <div class="card"><div class="numero">{max((p['score'] for p in produtos), default=0)}</div><div class="label">Maior Score</div></div>
</div>
"""

        # Seção campeões
        if campeoes:
            html += '<div class="secao"><h2>🔥 Produtos Campeões (Score ≥ 80)</h2>'
            for p in campeoes:
                html += self._card_produto(p, "campiao")
            html += '</div>'

        # Seção boas oportunidades
        if boas_oportunidades:
            html += '<div class="secao"><h2>✅ Boas Oportunidades (Score 60–79)</h2>'
            for p in boas_oportunidades:
                html += self._card_produto(p, "boa")
            html += '</div>'

        # Todos os outros
        outros = [p for p in produtos if p["score"] < 60]
        if outros:
            html += '<div class="secao"><h2>📋 Demais Produtos Analisados</h2>'
            for p in outros[:10]:  # limita para não poluir
                badge = "media" if p["score"] >= 40 else "ruim"
                html += self._card_produto(p, badge)
            html += '</div>'

        html += """
<div class="footer">Market Hunter — Desenvolvido por Raphael Ribeiro | github.com/RaphaelRibeiro-17/market-hunter</div>
</body></html>"""

        return html

    def _card_produto(self, p: Dict, tipo: str) -> str:
        preco_fmt = f"R$ {p['preco']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        score_pct = p['score']
        img = p.get('thumbnail', '')
        loja = p.get('loja', 'Vendedor Individual')

        return f"""
        <div class="produto {tipo if tipo == 'campiao' else ''}">
            <img src="{img}" alt="produto" onerror="this.style.display='none'">
            <div class="produto-info">
                <span class="badge {tipo}">{p['classificacao']}</span>
                <h3>{p['titulo'][:90]}{'...' if len(p['titulo']) > 90 else ''}</h3>
                <div class="meta">
                    <div>Preço: <span>{preco_fmt}</span></div>
                    <div>Vendas: <span>{p['vendas']}</span></div>
                    <div>Estoque: <span>{p['disponivel']}</span></div>
                    <div>Loja: <span>{loja}</span></div>
                    <div>Score: <span>{p['score']}/100</span></div>
                </div>
                <div class="score-bar"><div class="score-fill" style="width:{score_pct}%"></div></div>
                <a href="{p['url']}" target="_blank" class="btn">Ver no Mercado Livre →</a>
            </div>
        </div>"""

    def salvar(self, html: str, caminho: str):
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n📄 Relatório salvo em: {caminho}")
