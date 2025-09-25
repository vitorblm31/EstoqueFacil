import streamlit as st
import pandas as pd
import altair as alt
from abc import ABC, abstractmethod
from collections import deque

# ====================
# Domínio
# ====================
class Produto:
    def __init__(self, setor, fileira, prateleira, preco):
        if setor <= 0:
            raise ValueError("Setor deve ser positivo")
        if fileira <= 0:
            raise ValueError("Fileira deve ser positiva")
        if prateleira <= 0:
            raise ValueError("Prateleira deve ser positiva")
        if preco < 0:
            raise ValueError("Preço não pode ser negativo")

        self._setor = setor
        self._fileira = fileira
        self._prateleira = prateleira
        self._preco = preco

    def get_setor(self):
        return self._setor

    def get_fileira(self):
        return self._fileira

    def get_prateleira(self):
        return self._prateleira

    def get_preco(self):
        return self._preco

    def descricao(self):
        return f"{self.__class__.__name__}"


class ProdutoEletronico(Produto):
    def __init__(self, setor, fileira, prateleira, preco, garantia=12):
        super().__init__(setor, fileira, prateleira, preco)
        self._garantia = garantia

    def descricao(self):
        return f"Produto Eletrônico (garantia {self._garantia} meses)"


class ProdutoPerecivel(Produto):
    def __init__(self, setor, fileira, prateleira, preco, validade=30):
        super().__init__(setor, fileira, prateleira, preco)
        self._validade = validade

    def descricao(self):
        return f"Produto Perecível (validade {self._validade} dias)"


# ====================
# Interfaces
# ====================
class IRepositorioProduto(ABC):
    @abstractmethod
    def buscar(self, nome: str) -> Produto: ...


class IPagamento(ABC):
    @abstractmethod
    def pagar(self, valor: float) -> bool: ...


# ====================
# Implementações
# ====================
class RepositorioMemoria(IRepositorioProduto): #Hash
    def __init__(self, produtos: dict):
        self._produtos = {k.lower(): v for k, v in produtos.items()}

    def buscar(self, nome: str) -> Produto:
        return self._produtos.get(nome.lower())


class PagamentoDinheiro(IPagamento):
    def pagar(self, valor: float) -> bool:
        return True if valor >= 0 else False


# ====================
# Algoritmo de Pesquisa em Largura (BFS)
# ====================
def bfs_estoque(estoque, inicio, destino):
    """
    estoque: dict representando conexões do depósito
    inicio: ponto inicial (ex: "Setor 1")
    destino: ponto final (ex: "Produto: Cadeira")
    """
    visitados = set()
    fila = deque([[inicio]])

    while fila:
        caminho = fila.popleft()
        no = caminho[-1]

        if no == destino:
            return caminho

        if no not in visitados:
            vizinhos = estoque.get(no, [])
            for v in vizinhos:
                novo_caminho = list(caminho)
                novo_caminho.append(v)
                fila.append(novo_caminho)

            visitados.add(no)

    return None


# ====================
# Algoritmo de Pesquisa em Profundidade (DFS - Recursivo) Recursão
# ====================
def dfs_estoque(estoque, atual, destino, visitados=None, caminho=None):
    if visitados is None:
        visitados = set()
    if caminho is None:
        caminho = []

    caminho.append(atual)
    visitados.add(atual)

    if atual == destino:
        return caminho

    for vizinho in estoque.get(atual, []):
        if vizinho not in visitados:
            resultado = dfs_estoque(estoque, vizinho, destino, visitados, caminho.copy())
            if resultado:
                return resultado

    return None


# ====================
# Aplicação
# ====================
class ServicoCompra:
    def __init__(self, repo: IRepositorioProduto, pagamento: IPagamento):
        self._repo = repo
        self._pagamento = pagamento

    def mostrar_info(self, nome: str):
        return self._repo.buscar(nome)

    def comprar(self, nome: str, qtd: int) -> float:
        produto = self._repo.buscar(nome)
        if not produto:
            raise LookupError(f"Produto '{nome}' não encontrado.")
        if qtd <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        total = produto.get_preco() * qtd
        if self._pagamento.pagar(total):
            return total
        else:
            raise RuntimeError("Pagamento não autorizado")


# ====================
# Dados de exemplo
# ====================
produtos = {
    'Cadeira': Produto(12, 34, 36, 249.90),
    'Mesa': Produto(4, 28, 7, 499.99),
    'Livro': ProdutoPerecivel(10, 15, 20, 39.90, validade=365),
    'Caneta': Produto(2, 8, 1, 2.50),
    'Monitor': ProdutoEletronico(14, 27, 6, 899.99, garantia=24),
    'Mouse': ProdutoEletronico(1, 3, 5, 89.90),
    'Camera': ProdutoEletronico(16, 10, 21, 1199.90)
}

repo = RepositorioMemoria(produtos)
pagamento = PagamentoDinheiro()
servico = ServicoCompra(repo, pagamento)

# Exemplo de grafo do estoque (para BFS e DFS)
estoque_grafo = {
    "Entrada": ["Setor 1", "Setor 2"],
    "Setor 1": ["Fileira A", "Fileira B"],
    "Setor 2": ["Fileira C"],
    "Fileira A": ["Prateleira 1"],
    "Fileira B": ["Prateleira 2"],
    "Fileira C": ["Prateleira 3"],
    "Prateleira 1": ["Produto: Cadeira"],
    "Prateleira 2": ["Produto: Mesa"],
    "Prateleira 3": ["Produto: Livro"]
}

# ====================
# Streamlit App
# ====================
st.title("🛒 Estoque Fácil 2.0")

# Gráfico de preços
st.subheader("📊 Comparação de preços dos produtos")
df_precos = pd.DataFrame({
    "Produto": list(produtos.keys()),
    "Preço": [p.get_preco() for p in produtos.values()]
})
chart = alt.Chart(df_precos).mark_bar().encode(
    x="Produto",
    y="Preço",
    tooltip=["Produto", "Preço"]
)
st.altair_chart(chart, use_container_width=True)

# Seleção de produto
opcao = st.selectbox("Selecione um produto:", list(produtos.keys()))
produto = servico.mostrar_info(opcao)

if produto:
    st.subheader("📍 Localização do Produto")
    st.write(f"**Setor:** {produto.get_setor()}")
    st.write(f"**Fileira:** {produto.get_fileira()}")
    st.write(f"**Prateleira:** {produto.get_prateleira()}")
    st.write(f"**Preço unitário:** R$ {produto.get_preco():.2f}")
    st.write(f"**Descrição:** {produto.descricao()}")

    st.subheader("🔎 Pesquisa em Largura (BFS)")
    caminho_bfs = bfs_estoque(estoque_grafo, "Entrada", f"Produto: {opcao}")
    if caminho_bfs:
        st.write("➡️ Caminho encontrado (BFS):")
        st.write(" → ".join(caminho_bfs))
    else:
        st.warning("Produto não está mapeado no grafo do estoque (BFS).")

    st.subheader("🔎 Pesquisa em Profundidade (DFS - Recursiva)")
    caminho_dfs = dfs_estoque(estoque_grafo, "Entrada", f"Produto: {opcao}")
    if caminho_dfs:
        st.write("➡️ Caminho encontrado (DFS):")
        st.write(" → ".join(caminho_dfs))
    else:
        st.warning("Produto não está mapeado no grafo do estoque (DFS).")

    st.subheader("💳 Compra")
    quantidade = st.number_input("Quantas unidades deseja comprar?", min_value=1, step=1)

    if st.button("Finalizar compra"):
        try:
            total = servico.comprar(opcao, quantidade)
            st.success(f"✅ Compra realizada com sucesso! Total: R$ {total:.2f}")
        except Exception as e:
            st.error(f"Erro: {str(e)}")
else:
    st.warning("Produto não encontrado.")
