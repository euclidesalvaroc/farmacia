import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

PRODUTOS = {
    "1": {"nome": "Paracetamol", "preco": 500},
    "2": {"nome": "Amoxicilina", "preco": 1200},
    "3": {"nome": "Vitamina C", "preco": 800},
    "4": {"nome": "Ibuprofeno", "preco": 650},
}


COR_AZUL = "#1e40af"
COR_VERDE = "#059669"
COR_VERMELHO = "#dc2626"
COR_FUNDO = "#f1f5f9"
COR_TEXTO = "#1e293b"
COR_BRANCO = "#ffffff"


class AppFarmacia(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Farmácia — Sistema de Faturação B2B")
        self.geometry("880x520")
        self.minsize(760, 480)
        self.configure(bg=COR_FUNDO)

        self.carrinho = []  # cada item: {"nome": str, "preco": float, "qtd": int}

        self._construir_estilo()
        self._construir_cabecalho()
        self._construir_corpo()
        self._construir_rodape()

    # ------------------------------------------------------------------ UI

    def _construir_estilo(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure(
            "Azul.TButton",
            background=COR_AZUL,
            foreground=COR_BRANCO,
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        estilo.map("Azul.TButton", background=[("active", "#1c3a9e")])

        estilo.configure(
            "Verde.TButton",
            background=COR_VERDE,
            foreground=COR_BRANCO,
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        estilo.map("Verde.TButton", background=[("active", "#047857")])

        estilo.configure(
            "Vermelho.TButton",
            background=COR_VERMELHO,
            foreground=COR_BRANCO,
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        estilo.map("Vermelho.TButton", background=[("active", "#b91c1c")])

    def _construir_cabecalho(self):
        cabecalho = tk.Frame(self, bg=COR_AZUL, height=64)
        cabecalho.pack(fill="x", side="top")
        cabecalho.pack_propagate(False)

        tk.Label(
            cabecalho,
            text="Farmácia — Faturação B2B",
            bg=COR_AZUL,
            fg=COR_BRANCO,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=20)

        tk.Label(
            cabecalho,
            text="Venda por ID → carrinho → fatura",
            bg=COR_AZUL,
            fg="#dbeafe",
            font=("Segoe UI", 10),
        ).pack(side="right", padx=20)

    def _construir_corpo(self):
        corpo = tk.Frame(self, bg=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=16, pady=16)
        corpo.columnconfigure(0, weight=1)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        # ---- Coluna esquerda: catálogo -----------------------------------
        painel_catalogo = tk.LabelFrame(
            corpo, text="Catálogo", bg=COR_BRANCO, fg=COR_TEXTO,
            font=("Segoe UI", 10, "bold"), padx=10, pady=10,
        )
        painel_catalogo.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.tabela_produtos = ttk.Treeview(
            painel_catalogo, columns=("id", "produto", "preco"),
            show="headings", height=10,
        )
        self.tabela_produtos.heading("id", text="ID")
        self.tabela_produtos.heading("produto", text="Produto")
        self.tabela_produtos.heading("preco", text="Preço (Kz)")
        self.tabela_produtos.column("id", width=40, anchor="center")
        self.tabela_produtos.column("produto", width=180)
        self.tabela_produtos.column("preco", width=100, anchor="e")
        self.tabela_produtos.pack(fill="both", expand=True)

        for pid, info in PRODUTOS.items():
            self.tabela_produtos.insert(
                "", "end", iid=pid,
                values=(pid, info["nome"], f"{info['preco']:,.0f}".replace(",", ".")),
            )

        linha_qtd = tk.Frame(painel_catalogo, bg=COR_BRANCO)
        linha_qtd.pack(fill="x", pady=(10, 0))
        tk.Label(linha_qtd, text="Quantidade:", bg=COR_BRANCO, fg=COR_TEXTO).pack(side="left")
        self.var_qtd = tk.IntVar(value=1)
        tk.Spinbox(linha_qtd, from_=1, to=999, textvariable=self.var_qtd, width=6).pack(
            side="left", padx=8
        )
        ttk.Button(
            linha_qtd, text="Adicionar ao Carrinho ➜", style="Azul.TButton",
            command=self.adicionar_ao_carrinho,
        ).pack(side="right")

        # ---- Coluna direita: carrinho -------------------------------------
        painel_carrinho = tk.LabelFrame(
            corpo, text="Carrinho / Fatura", bg=COR_BRANCO, fg=COR_TEXTO,
            font=("Segoe UI", 10, "bold"), padx=10, pady=10,
        )
        painel_carrinho.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.tabela_carrinho = ttk.Treeview(
            painel_carrinho, columns=("produto", "qtd", "preco", "subtotal"),
            show="headings", height=10,
        )
        self.tabela_carrinho.heading("produto", text="Produto")
        self.tabela_carrinho.heading("qtd", text="Qtd")
        self.tabela_carrinho.heading("preco", text="Preço")
        self.tabela_carrinho.heading("subtotal", text="Subtotal")
        self.tabela_carrinho.column("produto", width=150)
        self.tabela_carrinho.column("qtd", width=50, anchor="center")
        self.tabela_carrinho.column("preco", width=90, anchor="e")
        self.tabela_carrinho.column("subtotal", width=100, anchor="e")
        self.tabela_carrinho.pack(fill="both", expand=True)

        acoes_carrinho = tk.Frame(painel_carrinho, bg=COR_BRANCO)
        acoes_carrinho.pack(fill="x", pady=(10, 0))
        ttk.Button(
            acoes_carrinho, text="Remover Selecionado", style="Vermelho.TButton",
            command=self.remover_selecionado,
        ).pack(side="left")
        ttk.Button(
            acoes_carrinho, text="Limpar Carrinho", style="Vermelho.TButton",
            command=self.limpar_carrinho,
        ).pack(side="left", padx=8)

    def _construir_rodape(self):
        rodape = tk.Frame(self, bg=COR_FUNDO)
        rodape.pack(fill="x", padx=16, pady=(0, 16))

        self.var_total = tk.StringVar(value="Total: 0 Kz")
        tk.Label(
            rodape, textvariable=self.var_total, bg=COR_FUNDO, fg=COR_TEXTO,
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        ttk.Button(
            rodape, text="Emitir Fatura", style="Verde.TButton",
            command=self.emitir_fatura,
        ).pack(side="right")

    # ------------------------------------------------------------- Lógica

    def adicionar_ao_carrinho(self):
        selecao = self.tabela_produtos.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecciona um produto no catálogo primeiro.")
            return

        pid = selecao[0]
        info = PRODUTOS[pid]
        qtd = max(1, self.var_qtd.get())

        for item in self.carrinho:
            if item["nome"] == info["nome"]:
                item["qtd"] += qtd
                break
        else:
            self.carrinho.append({"nome": info["nome"], "preco": info["preco"], "qtd": qtd})

        self._actualizar_tabela_carrinho()

    def remover_selecionado(self):
        selecao = self.tabela_carrinho.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecciona um item do carrinho para remover.")
            return
        indice = self.tabela_carrinho.index(selecao[0])
        del self.carrinho[indice]
        self._actualizar_tabela_carrinho()

    def limpar_carrinho(self):
        if not self.carrinho:
            return
        if messagebox.askyesno("Confirmar", "Limpar todos os itens do carrinho?"):
            self.carrinho.clear()
            self._actualizar_tabela_carrinho()

    def _actualizar_tabela_carrinho(self):
        self.tabela_carrinho.delete(*self.tabela_carrinho.get_children())
        total = 0
        for item in self.carrinho:
            subtotal = item["preco"] * item["qtd"]
            total += subtotal
            self.tabela_carrinho.insert(
                "", "end",
                values=(
                    item["nome"],
                    item["qtd"],
                    f"{item['preco']:,.0f}".replace(",", "."),
                    f"{subtotal:,.0f}".replace(",", "."),
                ),
            )
        self.var_total.set(f"Total: {total:,.0f}".replace(",", ".") + " Kz")

    def emitir_fatura(self):
        if not self.carrinho:
            messagebox.showwarning("Atenção", "O carrinho está vazio.")
            return

        total = sum(item["preco"] * item["qtd"] for item in self.carrinho)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")

        linhas = [
            "=" * 34,
            "        FATURA DE VENDA",
            "=" * 34,
            f"Data: {agora}",
            "-" * 34,
        ]
        for item in self.carrinho:
            subtotal = item["preco"] * item["qtd"]
            linhas.append(f"{item['nome']} x{item['qtd']}: {subtotal:,.0f} Kz".replace(",", "."))
        linhas.append("-" * 34)
        linhas.append(f"TOTAL A PAGAR: {total:,.0f} Kz".replace(",", "."))
        linhas.append("=" * 34)
        texto_fatura = "\n".join(linhas)

        self._mostrar_janela_fatura(texto_fatura)

    def _mostrar_janela_fatura(self, texto_fatura):
        janela = tk.Toplevel(self)
        janela.title("Fatura Emitida")
        janela.configure(bg=COR_BRANCO)
        janela.geometry("360x420")

        tk.Label(
            janela, text="✓ Venda finalizada com sucesso!", bg=COR_VERDE, fg=COR_BRANCO,
            font=("Segoe UI", 11, "bold"), pady=10,
        ).pack(fill="x")

        caixa_texto = tk.Text(janela, font=("Courier New", 10), bg=COR_FUNDO, relief="flat")
        caixa_texto.insert("1.0", texto_fatura)
        caixa_texto.configure(state="disabled")
        caixa_texto.pack(fill="both", expand=True, padx=12, pady=12)

        botoes = tk.Frame(janela, bg=COR_BRANCO)
        botoes.pack(fill="x", padx=12, pady=(0, 12))

        ttk.Button(
            botoes, text="Guardar .txt", style="Azul.TButton",
            command=lambda: self._guardar_fatura_txt(texto_fatura),
        ).pack(side="left")
        ttk.Button(
            botoes, text="Nova Venda", style="Verde.TButton",
            command=lambda: (self._nova_venda(), janela.destroy()),
        ).pack(side="right")

    def _guardar_fatura_txt(self, texto_fatura):
        nome_ficheiro = f"fatura-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        with open(nome_ficheiro, "w", encoding="utf-8") as f:
            f.write(texto_fatura)
        messagebox.showinfo("Guardado", f"Fatura guardada como {nome_ficheiro}")

    def _nova_venda(self):
        self.carrinho.clear()
        self._actualizar_tabela_carrinho()


if __name__ == "__main__":
    app = AppFarmacia()
    app.mainloop()
