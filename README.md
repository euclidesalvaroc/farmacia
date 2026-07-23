# Farmácia — Sistema de Faturação B2B

Sistema de faturação para farmácia, com duas formas de correr o mesmo
processo (catálogo → carrinho → fatura): uma versão de terminal e uma
versão com interface gráfica em **Tkinter**.

## Ficheiros

| Ficheiro              | Descrição                                             |
| ---------------------- | ------------------------------------------------------ |
| `main.py`   | Interface gráfica em Tkinter.      |

## Como correr

Precisas apenas de Python 3 instalado — nenhuma dependência externa.

```bash
# Versão com interface gráfica
python main.py
```

Se a versão gráfica der erro `No module named tkinter`, instala o pacote
do sistema (o Tkinter normalmente já vem com o Python no Windows/Mac,
mas em algumas distribuições Linux é separado):

```bash
sudo apt install python3-tk
```

## Interface gráfica — como funciona

1. **Catálogo** (esquerda): lista de produtos com ID e preço.
2. Escolhe um produto, define a **quantidade** e clica em **"Adicionar
   ao Carrinho"**.
3. **Carrinho** (direita): mostra os itens adicionados, com subtotal
   por linha e o total geral em baixo. É possível remover um item
   seleccionado ou limpar o carrinho todo.
4. **"Emitir Fatura"** gera a fatura numa janela separada, com opção de
   **guardar em `.txt`** (fica na mesma pasta do script, com nome
   `fatura-AAAAMMDD-HHMMSS.txt`) ou começar uma **nova venda**.

## Catálogo actual

| ID  | Produto      | Preço (Kz) |
| --- | ------------ | ---------: |
| 1   | Paracetamol  |        500 |
| 2   | Amoxicilina  |      1 200 |
| 3   | Vitamina C   |        800 |
| 4   | Ibuprofeno   |        650 |

Para adicionar produtos, basta editar o dicionário `PRODUTOS` no topo
de cada ficheiro.

## Limitações actuais

- Sem persistência entre sessões (o carrinho reinicia ao fechar o
  programa) — as faturas só ficam guardadas se exportares para `.txt`.
- Sem ligação a base de dados ou stock; é um protótipo de faturação,
  não um sistema de gestão de inventário.
