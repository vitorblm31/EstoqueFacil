# 🛒 Estoque Fácil 2.0

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)

**Estoque Fácil** é um aplicativo interativo de gestão de estoque focado na aplicação prática de conceitos avançados de Ciência da Computação, como Programação Orientada a Objetos (POO) e algoritmos de travessia em grafos. Através de uma interface web intuitiva, o sistema permite gerenciar produtos, visualizar métricas de preço e traçar as melhores rotas físicas dentro de um armazém simulado.

## 🚀 Principais Funcionalidades

* **Visualização Dinâmica de Dados:** Gráficos interativos comparando os preços dos produtos em estoque.
* **Sistema de Roteamento (Pathfinding):** Implementação de algoritmos de Busca em Largura (BFS) e Busca em Profundidade (DFS) para encontrar o caminho exato da entrada do armazém até a prateleira do produto.
* **Catálogo Detalhado:** Sistema de busca de produtos exibindo setor, fileira, prateleira, preço e características específicas (como validade ou garantia).
* **Simulação de Checkout:** Fluxo de carrinho de compras validando quantidades e autorização de pagamento.

## 🧠 Arquitetura e Conceitos Aplicados

Este projeto foi construído com foco em boas práticas de engenharia de software e estrutura de dados:

* **Programação Orientada a Objetos (POO):** Uso de Herança (`ProdutoEletronico`, `ProdutoPerecivel`), Encapsulamento de atributos e Classes Abstratas/Interfaces (`IRepositorioProduto`, `IPagamento`).
* **Estrutura de Dados:** * Uso de **Dicionários (Hash Maps)** para armazenamento e recuperação rápida de produtos em memória na classe `RepositorioMemoria`.
  * Representação do layout do armazém como um **Grafo** para navegação.
  * Uso de **Filas (Deques)** e **Sets** para otimização dos algoritmos de busca.
* **Algoritmos em Grafos:** Implementação iterativa (BFS) e recursiva (DFS) para varredura de nós no estoque.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Web:** Streamlit
* **Manipulação de Dados:** Pandas
* **Visualização:** Altair
