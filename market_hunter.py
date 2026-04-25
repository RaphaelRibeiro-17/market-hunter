"""
Market Hunter — Pesquisa de Mercado Automatizada
Identifica produtos campeões em marketplaces públicos

Uso:
    python market_hunter.py

O relatório HTML será salvo na pasta /dados
"""

import os
from datetime import datetime
from modulos.buscador_produtos import BuscadorProdutos
from modulos.pontuador import PontuadorOportunidades
from modulos.relatorio import GeradorRelatorio


def main():
    print("=" * 55)
    print("🔍 MARKET HUNTER — Pesquisa de Mercado")
    print("=" * 55)

    # -------------------------------------------------------
    # 🎯 CONFIGURE AQUI os produtos/nichos que quer analisar
    # -------------------------------------------------------
    TERMOS_DE_BUSCA = [
        "curso online",
        "ebook",
        "suplemento",
        "produto digital",
        "infoproduto",
    ]
    # -------------------------------------------------------

    buscador = BuscadorProdutos()
    pontuador = PontuadorOportunidades()
    relatorio = GeradorRelatorio()

    # 1. Buscar produtos
    print("\n📡 Iniciando buscas...")
    produtos_brutos = buscador.buscar_multiplos_termos(
        TERMOS_DE_BUSCA, limite_por_termo=15
    )
    print(f"\n✅ Total bruto coletado: {len(produtos_brutos)} produtos")

    if not produtos_brutos:
        print("\n❌ Nenhum produto encontrado. Verifique sua conexão.")
        return

    # 2. Pontuar e classificar
    print("\n📊 Calculando scores de oportunidade...")
    produtos_pontuados = pontuador.pontuar_lista(produtos_brutos)

    # 3. Mostrar top 10 no terminal
    print("\n" + "=" * 55)
    print("🏆 TOP 10 PRODUTOS POR SCORE")
    print("=" * 55)
    for i, p in enumerate(produtos_pontuados[:10], 1):
        print(f"{i:>2}. [{p['score']:>3}/100] {p['classificacao']}")
        print(f"     {p['titulo'][:60]}")
        print(f"     R$ {p['preco']:.2f} | Vendas: {p['vendas']} | {p['url']}")
        print()

    # 4. Gerar relatório HTML
    print("\n🖨️ Gerando relatório HTML...")
    os.makedirs("dados", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = f"dados/relatorio_{timestamp}.html"

    html = relatorio.gerar_html(produtos_pontuados, TERMOS_DE_BUSCA)
    relatorio.salvar(html, caminho)

    print("\n✅ Tudo pronto! Abra o arquivo HTML no navegador para ver o relatório completo.")
    print(f"   📂 {caminho}")
    print("=" * 55)


if __name__ == "__main__":
    main()
