"""
Buscador de Produtos — consulta APIs públicas para encontrar produtos campeões
Fonte principal: Mercado Livre API (gratuita, sem necessidade de login)
"""

import requests
import time
from typing import List, Dict


class BuscadorProdutos:
    """
    Busca produtos em marketplaces públicos usando APIs abertas.
    Nenhuma autenticação necessária para pesquisa básica.
    """

    ML_API = "https://api.mercadolibre.com"
    ML_SITE = "MLB"  # Brasil

    def buscar_mercado_livre(self, termo: str, limite: int = 20) -> List[Dict]:
        """
        Busca produtos no Mercado Livre pela API pública oficial.
        Retorna lista de produtos com métricas de vendas.
        """
        print(f"\n🔍 Buscando '{termo}' no Mercado Livre...")

        url = f"{self.ML_API}/sites/{self.ML_SITE}/search"
        params = {
            "q": termo,
            "limit": limite,
            "sort": "relevance"
        }

        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            dados = resp.json()
        except Exception as e:
            print(f"   ⚠️ Erro ao buscar no ML: {e}")
            return []

        produtos = []
        for item in dados.get("results", []):
            produto = {
                "id": item.get("id", ""),
                "titulo": item.get("title", ""),
                "preco": item.get("price", 0),
                "moeda": item.get("currency_id", "BRL"),
                "vendas": item.get("sold_quantity", 0),
                "disponivel": item.get("available_quantity", 0),
                "condicao": item.get("condition", ""),
                "frete_gratis": item.get("shipping", {}).get("free_shipping", False),
                "url": item.get("permalink", ""),
                "thumbnail": item.get("thumbnail", ""),
                "loja": item.get("official_store_name", "Vendedor Individual"),
                "fonte": "Mercado Livre",
                "termo_busca": termo
            }
            produtos.append(produto)
            time.sleep(0.1)  # respeitar rate limit

        print(f"   ✅ {len(produtos)} produtos encontrados")
        return produtos

    def buscar_multiplos_termos(self, termos: List[str], limite_por_termo: int = 10) -> List[Dict]:
        """
        Busca vários termos de uma vez e consolida os resultados.
        """
        todos = []
        for termo in termos:
            resultados = self.buscar_mercado_livre(termo, limite=limite_por_termo)
            todos.extend(resultados)
            time.sleep(0.5)

        # Remove duplicatas pelo ID
        vistos = set()
        unicos = []
        for p in todos:
            if p["id"] not in vistos:
                vistos.add(p["id"])
                unicos.append(p)

        return unicos
