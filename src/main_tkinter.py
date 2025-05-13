# interface gráfica simples para o sistema de caixa eletrônicot
import tkinter as tk
from tkinter import ttk, messagebox
from autenticacao import registrar_usuario_logica, autenticar_usuario
from operacoes import consultar_saldo, sacar, depositar, extrato, transferir

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco Python")
        self.root.geometry("400x400")
        self.current_user = None
        self.criar_tela_login()

    def limpar_tela(self):
        """Remove todos os widgets da tela."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------ TELA DE LOGIN ------------------
    def criar_tela_login(self):
        self.limpar_tela()
        ttk.Label(self.root, text="Banco Python", font=("Arial", 16)).pack(pady=20)
        
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        
        # Campos de entrada
        ttk.Label(frame, text="Número da Conta:").grid(row=0, column=0, padx=5, pady=5)
        self.conta_entry = ttk.Entry(frame)
        self.conta_entry.grid(row=0, column=1)
        
        ttk.Label(frame, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
        self.senha_entry = ttk.Entry(frame, show="*")
        self.senha_entry.grid(row=1, column=1)
        
        # Botões
        botoes_frame = ttk.Frame(self.root)
        botoes_frame.pack(pady=20)
        
        ttk.Button(botoes_frame, text="Entrar", command=self.fazer_login).pack(side=tk.LEFT, padx=10)
        ttk.Button(botoes_frame, text="Registrar", command=self.criar_tela_registro).pack(side=tk.LEFT, padx=10)
        ttk.Button(botoes_frame, text="Sair", command=self.root.destroy).pack(side=tk.LEFT, padx=10)

    def fazer_login(self):
        """Autentica o usuário e abre o menu principal."""
        try:
            conta = self.conta_entry.get().strip()
            senha = self.senha_entry.get().strip()
            autenticar_usuario(conta, senha)
            self.current_user = conta
            self.criar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ------------------ TELA DE REGISTRO ------------------
    def criar_tela_registro(self):
        self.limpar_tela()
        ttk.Label(self.root, text="Cadastro de Nova Conta", font=("Arial", 14)).pack(pady=10)
        
        campos = [
            ("Nome Completo", "nome"),
            ("E-mail", "email"),
            ("CPF (XXX.XXX.XXX-XX)", "cpf"),
            ("Telefone ((XX) 9XXXX-XXXX)", "telefone"),
            ("Data de Nascimento (DD/MM/AAAA)", "data_nasc"),
            ("Senha (4 dígitos)", "senha"),
            ("Confirme a Senha", "confirm_senha")
        ]
        
        self.entries = {}
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        
        for idx, (label, key) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=idx, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(frame)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.entries[key] = entry
        
        botoes_frame = ttk.Frame(self.root)
        botoes_frame.pack(pady=10)
        
        ttk.Button(botoes_frame, text="Cadastrar", command=self.registrar).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Voltar", command=self.criar_tela_login).pack(side=tk.LEFT, padx=5)

    def registrar(self):
        """Processa o registro de um novo usuário."""
        try:
            numero_conta = registrar_usuario_logica(
                nome=self.entries["nome"].get(),
                email=self.entries["email"].get(),
                cpf=self.entries["cpf"].get(),
                telefone=self.entries["telefone"].get(),
                data_nasc=self.entries["data_nasc"].get(),
                senha=self.entries["senha"].get(),
                confirmacao_senha=self.entries["confirm_senha"].get()
            )
            messagebox.showinfo("Sucesso", f"Conta {numero_conta} criada com sucesso!")
            self.criar_tela_login()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ------------------ MENU PRINCIPAL ------------------
    def criar_menu_principal(self):
        self.limpar_tela()
        ttk.Label(self.root, text=f"Bem-vindo, {self.current_user}", font=("Arial", 12)).pack(pady=10)
        
        operacoes = [
            ("Consultar Saldo", self.consultar_saldo),
            ("Realizar Saque", self.tela_saque),
            ("Fazer Depósito", self.tela_deposito),
            ("Ver Extrato", self.ver_extrato),
            ("Transferir", self.tela_transferencia),
            ("Sair", self.criar_tela_login)
        ]
        
        for texto, comando in operacoes:
            ttk.Button(self.root, text=texto, command=comando).pack(pady=3)

    # ------------------ OPERAÇÕES ------------------
    def consultar_saldo(self):
        """Exibe o saldo atual em uma caixa de diálogo."""
        try:
            saldo = consultar_saldo(self.current_user)
            messagebox.showinfo("Saldo", f"Saldo atual: R$ {saldo:.2f}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def tela_saque(self):
        """Abre a tela de saque."""
        self.criar_tela_operacao("Saque", self.executar_saque)

    def tela_deposito(self):
        """Abre a tela de depósito."""
        self.criar_tela_operacao("Depósito", self.executar_deposito)

    def criar_tela_operacao(self, titulo: str, comando):
        """Template para telas de operações (saque/depósito)."""
        self.limpar_tela()
        ttk.Label(self.root, text=titulo, font=("Arial", 12)).pack(pady=10)
        
        ttk.Label(self.root, text="Valor:").pack()
        self.valor_entry = ttk.Entry(self.root)
        self.valor_entry.pack(pady=5)
        
        ttk.Button(self.root, text="Confirmar", command=comando).pack(pady=5)
        ttk.Button(self.root, text="Voltar", command=self.criar_menu_principal).pack()

    def executar_saque(self):
        """Executa a operação de saque."""
        try:
            valor = float(self.valor_entry.get())
            sacar(self.current_user, valor)
            messagebox.showinfo("Sucesso", "Saque realizado com sucesso!")
            self.criar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def executar_deposito(self):
        """Executa a operação de depósito."""
        try:
            valor = float(self.valor_entry.get())
            depositar(self.current_user, valor)
            messagebox.showinfo("Sucesso", "Depósito realizado com sucesso!")
            self.criar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def ver_extrato(self):
        """Exibe o histórico de transações em uma nova janela."""
        try:
            transacoes = extrato(self.current_user)
            janela_extrato = tk.Toplevel(self.root)
            janela_extrato.title("Extrato")
            
            texto = tk.Text(janela_extrato, width=50, height=15)
            texto.pack(padx=10, pady=10)
            
            for transacao in reversed(transacoes):
                texto.insert(tk.END, transacao + "\n")
            texto.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def tela_transferencia(self):
        """Abre a tela de transferência."""
        self.limpar_tela()
        ttk.Label(self.root, text="Transferência", font=("Arial", 12)).pack(pady=10)
        
        ttk.Label(self.root, text="Conta Destino:").pack()
        self.conta_destino_entry = ttk.Entry(self.root)
        self.conta_destino_entry.pack(pady=5)
        
        ttk.Label(self.root, text="Valor (R$):").pack()
        self.valor_transferencia_entry = ttk.Entry(self.root)
        self.valor_transferencia_entry.pack(pady=5)
        
        ttk.Button(self.root, text="Transferir", command=self.executar_transferencia).pack(pady=5)
        ttk.Button(self.root, text="Voltar", command=self.criar_menu_principal).pack()

    def executar_transferencia(self):
        """Executa a transferência entre contas."""
        try:
            destino = self.conta_destino_entry.get().strip()
            valor = float(self.valor_transferencia_entry.get())
            transferir(self.current_user, destino, valor)
            messagebox.showinfo("Sucesso", "Transferência realizada com sucesso!")
            self.criar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()