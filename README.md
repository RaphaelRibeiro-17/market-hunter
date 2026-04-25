# 🔍 Market Hunter

Ferramenta de pesquisa de mercado para identificar produtos campeões — físicos, digitais e afiliados.

## O que faz

- Busca produtos com alto volume de vendas no Mercado Livre
- Pontua cada produto com um **Score de Oportunidade**
- Classifica como: físico, digital ou afiliável
- Gera relatório HTML profissional com os melhores achados

## Como usar

```bash
# 1. Clone o repositório
git clone https://github.com/RaphaelRibeiro-17/market-hunter.git
cd market-hunter

# 2. Crie ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute
python market_hunter.py
```

## Score de Oportunidade

| Faixa | Classificação |
|---|---|
| 80–100 | 🔥 Produto Campeão |
| 60–79 | ✅ Boa Oportunidade |
| 40–59 | ⚠️ Oportunidade Média |
| 0–39 | ❌ Evitar |

## Autor
Raphael Ribeiro — [@RaphaelRibeiro-17](https://github.com/RaphaelRibeiro-17)
