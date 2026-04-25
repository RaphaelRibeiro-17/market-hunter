"""
Pontuador de Oportunidades — calcula o Score de Oportunidade de cada produto.
Lógica inspirada no identificacao_oportunidades.py do projeto ia-survey.

Score de 0 a 100 baseado em:
- Volume de vendas (peso 40%)
- Preço na faixa ideal (peso 25%)
- Disponibilidade de estoque (peso 15%)
- Frete grátis (peso 10%)
- Condição do produto (peso 10%)
"""

from typing import List, Dict


class PontuadorOportunidades:

    def calcular_score(self, produto: Dict) -> Dict:
        """Calcula score de 0 a 100 para um produto."""
        score = 0
        detalhes = []

        # --- Vendas (40 pontos) ---
        vendas = produto.get("vendas", 0)
        if vendas >= 500:
            score += 40
            detalhes.append("🔥 Alto volume de vendas (+40)")
        elif vendas >= 100:
            score += 28
            detalhes.append("✅ Bom volume de vendas (+28)")
        elif vendas >= 20:
            score += 15
            detalhes.append("⚠️ Volume de vendas moderado (+15)")
        else:
            score += 5
            detalhes.append("❌ Poucas vendas (+5)")

        # --- Preço ideal (25 pontos) ---
        preco = produto.get("preco", 0)
        if 50 <= preco <= 500:
            score += 25
            detalhes.append("✅ Faixa de preço ideal R$50–R$500 (+25)")
        elif 20 <= preco < 50 or 500 < preco <= 1000:
            score += 15
            detalhes.append("⚠️ Preço aceitável (+15)")
        elif preco > 1000:
            score += 8
            detalhes.append("⚠️ Ticket alto — exige mais confiança (+8)")
        else:
            score += 3
            detalhes.append("❌ Preço muito baixo — margem ruim (+3)")

        # --- Disponibilidade (15 pontos) ---
        disponivel = produto.get("disponivel", 0)
        if disponivel >= 50:
            score += 15
            detalhes.append("✅ Estoque abundante (+15)")
        elif disponivel >= 10:
            score += 10
            detalhes.append("⚠️ Estoque moderado (+10)")
        else:
            score += 3
            detalhes.append("❌ Estoque baixo (+3)")

        # --- Frete grátis (10 pontos) ---
        if produto.get("frete_gratis"):
            score += 10
            detalhes.append("✅ Frete grátis (+10)")
        else:
            detalhes.append("❌ Sem frete grátis (0)")

        # --- Condição (10 pontos) ---
        if produto.get("condicao") == "new":
            score += 10
            detalhes.append("✅ Produto novo (+10)")
        else:
            score += 4
            detalhes.append("⚠️ Produto usado (+4)")

        # --- Classificação ---
        if score >= 80:
            classificacao = "🔥 Produto Campeão"
        elif score >= 60:
            classificacao = "✅ Boa Oportunidade"
        elif score >= 40:
            classificacao = "⚠️ Oportunidade Média"
        else:
            classificacao = "❌ Evitar"

        produto["score"] = score
        produto["classificacao"] = classificacao
        produto["detalhes_score"] = detalhes
        return produto

    def pontuar_lista(self, produtos: List[Dict]) -> List[Dict]:
        """Pontua todos os produtos e ordena do maior para o menor score."""
        pontuados = [self.calcular_score(p) for p in produtos]
        return sorted(pontuados, key=lambda x: x["score"], reverse=True)
