import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def converter_horario_para_minutos(horario):
    """Converte um horario no formato HH:MM para a quantidade de minutos do dia."""
    partes = horario.split(":")

    if len(partes) != 2:
        raise ValueError("Use o formato HH:MM.")

    hora = int(partes[0])
    minuto = int(partes[1])

    if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
        raise ValueError("Horario invalido.")

    return hora * 60 + minuto


def converter_minutos_para_horario(minutos):
    """Converte minutos do dia para o formato HH:MM."""
    hora = minutos // 60
    minuto = minutos % 60
    return f"{hora:02d}:{minuto:02d}"


def criar_cliente(nome, inicio_texto, fim_texto, observacao):
    """Valida os dados digitados e cria o dicionario de um cliente."""
    nome = nome.strip()
    observacao = observacao.strip()

    if nome == "":
        raise ValueError("O nome do cliente nao pode ficar vazio.")

    inicio = converter_horario_para_minutos(inicio_texto.strip())
    fim = converter_horario_para_minutos(fim_texto.strip())

    if inicio >= fim:
        raise ValueError("O horario de inicio deve ser menor que o horario de fim.")

    return {
        "nome": nome,
        "inicio": inicio,
        "fim": fim,
        "observacao": observacao,
    }


def gerar_clientes_aleatorios(quantidade):
    """Gera clientes ficticios com horarios aleatorios validos."""
    clientes = []
    bairros = [
        "Centro",
        "Bairro Norte",
        "Bairro Sul",
        "Avenida Principal",
        "Condominio Azul",
        "Proximo ao mercado",
        "Rua das Flores",
        "Sala comercial",
    ]

    for numero in range(1, quantidade + 1):
        inicio = random.randint(8 * 60, 17 * 60)
        duracao = random.choice([30, 45, 60, 90, 120])
        fim = inicio + duracao

        if fim > 18 * 60:
            fim = 18 * 60

        cliente = {
            "nome": f"Cliente {numero:02d}",
            "inicio": inicio,
            "fim": fim,
            "observacao": random.choice(bairros),
        }
        clientes.append(cliente)

    return clientes


def aplicar_interval_scheduling(clientes):
    """
    Aplica o algoritmo guloso de Interval Scheduling.

    O algoritmo ordena os clientes pelo menor horario de termino. Depois escolhe
    o primeiro cliente possivel e continua selecionando apenas os clientes cujo
    horario de inicio seja maior ou igual ao fim do ultimo cliente escolhido.
    Essa regra maximiza a quantidade de intervalos nao sobrepostos.
    """
    clientes_ordenados = sorted(clientes, key=lambda cliente: cliente["fim"])
    agenda = []
    ultimo_fim = -1

    for cliente in clientes_ordenados:
        if cliente["inicio"] >= ultimo_fim:
            agenda.append(cliente)
            ultimo_fim = cliente["fim"]

    clientes_escolhidos = set(id(cliente) for cliente in agenda)
    clientes_fora = []

    for cliente in clientes:
        if id(cliente) not in clientes_escolhidos:
            clientes_fora.append(cliente)

    return agenda, clientes_fora


class AplicacaoAgenda:
    """Interface grafica simples para cadastrar clientes e calcular a agenda."""

    def __init__(self, janela):
        self.janela = janela
        self.clientes = []

        self.janela.title("Agenda de Visitas - Interval Scheduling")
        self.janela.geometry("900x620")
        self.janela.minsize(760, 520)

        self.configurar_estilo()
        self.criar_interface()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f5f5f5")
        estilo.configure("Titulo.TLabel", background="#f5f5f5", font=("Arial", 16, "bold"))
        estilo.configure("Subtitulo.TLabel", background="#f5f5f5", font=("Arial", 11, "bold"))
        estilo.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        estilo.configure("TButton", font=("Arial", 10), padding=6)
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def criar_interface(self):
        quadro_principal = ttk.Frame(self.janela, padding=16)
        quadro_principal.pack(fill="both", expand=True)

        titulo = ttk.Label(
            quadro_principal,
            text="Agenda de Visitas - Interval Scheduling",
            style="Titulo.TLabel",
        )
        titulo.pack(anchor="w")

        quadro_formulario = ttk.LabelFrame(quadro_principal, text="Cadastrar cliente", padding=12)
        quadro_formulario.pack(fill="x", pady=(14, 10))

        quadro_formulario.columnconfigure(1, weight=1)
        quadro_formulario.columnconfigure(3, weight=1)

        ttk.Label(quadro_formulario, text="Nome:").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)
        self.entrada_nome = ttk.Entry(quadro_formulario)
        self.entrada_nome.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=4)

        ttk.Label(quadro_formulario, text="Inicio (HH:MM):").grid(row=0, column=2, sticky="w", padx=(0, 6), pady=4)
        self.entrada_inicio = ttk.Entry(quadro_formulario, width=12)
        self.entrada_inicio.grid(row=0, column=3, sticky="w", pady=4)

        ttk.Label(quadro_formulario, text="Fim (HH:MM):").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=4)
        self.entrada_fim = ttk.Entry(quadro_formulario, width=12)
        self.entrada_fim.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=4)

        ttk.Label(quadro_formulario, text="Endereco/observacao:").grid(row=1, column=2, sticky="w", padx=(0, 6), pady=4)
        self.entrada_observacao = ttk.Entry(quadro_formulario)
        self.entrada_observacao.grid(row=1, column=3, sticky="ew", pady=4)

        quadro_botoes = ttk.Frame(quadro_formulario)
        quadro_botoes.grid(row=2, column=0, columnspan=4, sticky="e", pady=(8, 0))

        ttk.Button(quadro_botoes, text="Cadastrar cliente", command=self.cadastrar_cliente).pack(side="left", padx=4)
        ttk.Button(quadro_botoes, text="Gerar clientes", command=self.gerar_clientes).pack(side="left", padx=4)
        ttk.Button(quadro_botoes, text="Limpar campos", command=self.limpar_campos).pack(side="left", padx=4)
        ttk.Button(quadro_botoes, text="Calcular melhor agenda", command=self.calcular_agenda).pack(side="left", padx=4)
        ttk.Button(quadro_botoes, text="Sair", command=self.janela.destroy).pack(side="left", padx=4)

        ttk.Label(quadro_principal, text="Clientes cadastrados", style="Subtitulo.TLabel").pack(anchor="w", pady=(8, 4))

        colunas_clientes = ("nome", "inicio", "fim", "observacao")
        self.tabela_clientes = ttk.Treeview(
            quadro_principal,
            columns=colunas_clientes,
            show="headings",
            height=8,
        )
        self.tabela_clientes.heading("nome", text="Cliente")
        self.tabela_clientes.heading("inicio", text="Inicio")
        self.tabela_clientes.heading("fim", text="Fim")
        self.tabela_clientes.heading("observacao", text="Endereco/observacao")
        self.tabela_clientes.column("nome", width=180)
        self.tabela_clientes.column("inicio", width=80, anchor="center")
        self.tabela_clientes.column("fim", width=80, anchor="center")
        self.tabela_clientes.column("observacao", width=360)
        self.tabela_clientes.pack(fill="both", expand=True)

        ttk.Label(quadro_principal, text="Resultado", style="Subtitulo.TLabel").pack(anchor="w", pady=(12, 4))

        self.texto_resultado = tk.Text(
            quadro_principal,
            height=10,
            wrap="word",
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#111111",
        )
        self.texto_resultado.pack(fill="both", expand=True)
        self.texto_resultado.insert("1.0", "Cadastre clientes e clique em 'Calcular melhor agenda'.")
        self.texto_resultado.configure(state="disabled")

    def cadastrar_cliente(self):
        """Adiciona um cliente na lista e atualiza a tabela da interface."""
        try:
            cliente = criar_cliente(
                self.entrada_nome.get(),
                self.entrada_inicio.get(),
                self.entrada_fim.get(),
                self.entrada_observacao.get(),
            )
        except ValueError as erro:
            messagebox.showerror("Erro no cadastro", str(erro))
            return

        self.clientes.append(cliente)
        self.atualizar_tabela_clientes()
        self.limpar_campos()
        messagebox.showinfo("Cadastro", "Cliente cadastrado com sucesso.")

    def gerar_clientes(self):
        """Gera 50 clientes ficticios e adiciona na lista atual."""
        novos_clientes = gerar_clientes_aleatorios(50)
        self.clientes.extend(novos_clientes)
        self.atualizar_tabela_clientes()
        self.mostrar_resultado("Foram gerados 50 clientes com horarios aleatorios.")
        messagebox.showinfo("Gerar clientes", "50 clientes foram gerados com sucesso.")

    def limpar_campos(self):
        self.entrada_nome.delete(0, tk.END)
        self.entrada_inicio.delete(0, tk.END)
        self.entrada_fim.delete(0, tk.END)
        self.entrada_observacao.delete(0, tk.END)
        self.entrada_nome.focus()

    def atualizar_tabela_clientes(self):
        for item in self.tabela_clientes.get_children():
            self.tabela_clientes.delete(item)

        for cliente in self.clientes:
            self.tabela_clientes.insert(
                "",
                tk.END,
                values=(
                    cliente["nome"],
                    converter_minutos_para_horario(cliente["inicio"]),
                    converter_minutos_para_horario(cliente["fim"]),
                    cliente["observacao"] if cliente["observacao"] else "-",
                ),
            )

    def calcular_agenda(self):
        """Calcula e exibe a melhor agenda de visitas na area de resultado."""
        if len(self.clientes) == 0:
            messagebox.showwarning("Agenda", "Cadastre pelo menos um cliente.")
            return

        agenda, clientes_fora = aplicar_interval_scheduling(self.clientes)
        linhas = []

        linhas.append("MELHOR AGENDA DE VISITAS")
        linhas.append("")

        for indice, cliente in enumerate(agenda, start=1):
            inicio = converter_minutos_para_horario(cliente["inicio"])
            fim = converter_minutos_para_horario(cliente["fim"])
            observacao = cliente["observacao"] if cliente["observacao"] else "-"
            linhas.append(f"{indice}. {cliente['nome']} | {inicio} - {fim} | {observacao}")

        linhas.append("")
        linhas.append(f"Quantidade maxima de visitas possiveis: {len(agenda)}")
        linhas.append("")

        if len(clientes_fora) > 0:
            linhas.append("CLIENTES QUE FICARAM DE FORA")
            for cliente in clientes_fora:
                inicio = converter_minutos_para_horario(cliente["inicio"])
                fim = converter_minutos_para_horario(cliente["fim"])
                linhas.append(f"- {cliente['nome']} | {inicio} - {fim}")
        else:
            linhas.append("Nenhum cliente ficou de fora da agenda.")

        self.mostrar_resultado("\n".join(linhas))

    def mostrar_resultado(self, texto):
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert("1.0", texto)
        self.texto_resultado.configure(state="disabled")


def executar_aplicacao():
    janela = tk.Tk()
    AplicacaoAgenda(janela)
    janela.mainloop()


if __name__ == "__main__":
    executar_aplicacao()
