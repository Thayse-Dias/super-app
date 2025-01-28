import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from PIL import Image
import re
import bcrypt
import sqlite3
from tkinter import Tk

class Application:
    def __init__(self):
        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.janela_login()
        self.janela.mainloop()
      
    def tema(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def tela(self):    
        self.janela.geometry("700x400")
        self.janela.title("Teela")
        self.janela.resizable(False, False)
        self.janela.configure(fg_color="white")
        
    def janela_login(self):
       
        login_frame = ctk.CTkFrame(master=self.janela, width=360, height=390, fg_color="white")
        login_frame.pack(side="right")
        
        img_path = "Logomarca1.jpg"  
        img = Image.open(img_path)
        img = img.resize((230, 230), Image.LANCZOS) 
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(270, 270))

        img_label = ctk.CTkLabel(master=self.janela, image=img_ctk, text="")
        img_label.place(x=50, y=60)
        
        label_tt = ctk.CTkLabel(master=login_frame, text="Faça seu Login", font=("Century Gothic bold", 20))
        label_tt.place(x=105, y=20)

        self.email_entry = ctk.CTkEntry(master=login_frame, placeholder_text="E-mail do Usuário", width=310, 
                                      font=("Century Gothic bold", 14))
        self.email_entry.place(x=25, y=80)
        
        username_label = ctk.CTkLabel(master=login_frame, text="*O campo e-mail é de caráter obrigatório.", text_color="black", 
                                    font=("Century Gothic bold", 11))
        username_label.place(x=25, y=110)

        self.password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Senha do Usuário", show="*", width=310, 
                                    font=("Century Gothic bold", 14))
        self.password_entry.place(x=25, y=160)

        password_label = ctk.CTkLabel(master=login_frame, text="*O campo senha de usuário é de caráter obrigatório.", text_color="black", 
                                    font=("Century Gothic bold", 11))
        password_label.place(x=25, y=190)

        checkbox = ctk.CTkCheckBox(master=login_frame, text="Lembrar-me")
        checkbox.place(x=25, y=230)
        
        login_Button = ctk.CTkButton(master=self.janela, text="Entrar", width=310, command=self.login)
        login_Button.place(x=365, y=280)

        register_label = ctk.CTkLabel(master=login_frame, text="Não possue conta?")
        register_label.place(x=25, y=320)
        
        register_button = ctk.CTkButton(master=login_frame, text="Cadastre-se", width=150, 
                                        fg_color="green", hover_color="#2D9334", command=self.tela_register)
        register_button.place(x=175, y=320)

    def tela_register(self):
        login_frame = self.janela.children.get('!ctkframe')
        login_frame.pack_forget()

        register_frame = ctk.CTkFrame(master=self.janela, width=350, height=396, fg_color="white")
        register_frame.pack(side="right") 
        
        label_tt = ctk.CTkLabel(master=register_frame, text="Cadastro de Usuário", font=("Century Gothic bold", 20))
        label_tt.place(x=90, y=10)
        
        span = ctk.CTkLabel(master=register_frame, text="*Preencha todos os campos com dados corretos", font=("Century Gothic bold", 11))
        span.place(x=25, y=50)
        
        self.register_username_entry = ctk.CTkEntry(master=register_frame, placeholder_text="Nome do Usuário", width=300, 
                                      font=("Century Gothic bold", 14))
        self.register_username_entry.place(x=25, y=90)
        
        self.register_email_entry = ctk.CTkEntry(master=register_frame, placeholder_text="E-mail do Usuário", width=300, 
                                    font=("Century Gothic bold", 14))
        self.register_email_entry.place(x=25, y=130)
        
        self.register_password_entry = ctk.CTkEntry(master=register_frame, placeholder_text="Senha do Usuário", show="*", width=300, 
                                    font=("Century Gothic bold", 14))
        self.register_password_entry.place(x=25, y=170)
        
        self.register_confirme_entry = ctk.CTkEntry(master=register_frame, placeholder_text="Confirme sua senha", show="*", width=300, 
                                    font=("Century Gothic bold", 14))
        self.register_confirme_entry.place(x=25, y=210)

        back_Button = ctk.CTkButton(master=register_frame, text="Voltar", width=140, fg_color="gray", 
                                    command=lambda: self.back(register_frame, login_frame))
        back_Button.place(x=25, y=285)
       
        save_Button = ctk.CTkButton(master=register_frame, text="Salvar", width=140, command=self.save_user)
        save_Button.place(x=185, y=285)
            
        checkbox = ctk.CTkCheckBox(master=register_frame, text="Aceito todos os Termos e Política", 
                                   font=("Century Gothic bold", 10))
        checkbox.place(x=25, y=350)
        
    def back(self, register_frame, login_frame):
        register_frame.pack_forget()
        login_frame.pack(side="right")

    def save_user(self):
        username = self.register_username_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        conf_password = self.register_confirme_entry.get()

        if not username or not email or not password or not conf_password:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        if password != conf_password:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro", "Formato de e-mail inválido.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conexao = sqlite3.connect("Sistema.db")
        cursor = conexao.cursor()
    
        try:
            cursor.execute("INSERT INTO users (Username, Email, Password) VALUES (?, ?, ?)", (username, email, hashed_password))
            conexao.commit() 
            messagebox.showinfo(title="Estado do Cadastro", message="Parabéns! Usuário cadastrado com sucesso.") 
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "E-mail já cadastrado.")
        finally:
            conexao.close()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Erro", "Por favor, preencha ambos os campos.")
            return

        conexao = sqlite3.connect("Sistema.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM users WHERE Email=?", (email,))
        user = cursor.fetchone()
        conexao.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
            self.janela.withdraw()
            ordem_servico = OrdemDeServico()
            ordem_servico.mainloop()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos.")
    
class OrdemDeServico(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Ordens de Serviço")
        self.geometry("750x500")

        self.janela_os = ctk.CTkFrame(self)
        self.janela_os.pack(pady=20, padx=20, fill="both", expand=True)

        label_os = ctk.CTkLabel(master=self.janela_os, text="Bem-vindo à Ordem de Serviço", font=("Century Gothic bold", 20))
        label_os.pack(pady=20)

        self.visualizar_button = ctk.CTkButton(master=self.janela_os, text="Lista de Chamados", command=self.visualizar_ordens, fg_color="green")
        self.visualizar_button.place(x=25, y=350)

        data_atual = datetime.now().strftime("%d/%m/%Y")
        self.entry_data_atual = ctk.CTkEntry(master=self.janela_os, width=300, font=("Century Gothic bold", 12))
        self.entry_data_atual.place(x=25, y=90)
        self.entry_data_atual.insert(0, data_atual)
        
        self.entry_local_atendimento = ctk.CTkEntry(master=self.janela_os, placeholder_text="Local de Atendimento", width=300, text_color="black",
                                                    font=("Century Gothic bold", 12))
        self.entry_local_atendimento.place(x=375, y=90)
        
        self.entry_descricao_servico = ctk.CTkEntry(master=self.janela_os, placeholder_text="Descrição do Serviço", width=650, text_color="black",
                                                     font=("Century Gothic bold", 12))
        self.entry_descricao_servico.place(x=25, y=130)
        
        label_setor = ctk.CTkLabel(master=self.janela_os, text="Setor:")
        label_setor.place(x=25, y=170)
        self.setor_var = ctk.StringVar(value="Ger.Operacional")
        self.menu_setor = ctk.CTkOptionMenu(master=self.janela_os, variable=self.setor_var,
                                             values=["Ger.Operacional", "Recepção", "Governança", "Manutenção", "A&B", "Eventos", "TI"])
        self.menu_setor.place(x=25, y=200)
        
        label_prioridade = ctk.CTkLabel(master=self.janela_os, text="Prioridade:")
        label_prioridade.place(x=25, y=250)
        
        self.prioridade_var = ctk.StringVar(value="Urgente")
        self.menu_prioridade = ctk.CTkOptionMenu(master=self.janela_os, variable=self.prioridade_var,
                                     values=["Sem urgência", "Urgente", "Avaliação"])
        self.menu_prioridade.place(x=25, y=280)
        
        label_observacoes = ctk.CTkLabel(master=self.janela_os, text="Observações:")
        label_observacoes.place(x=220, y=170)

        self.entry_observacoes = ctk.CTkEntry(master=self.janela_os, width=460, height=180, font=("arial", 14))
        self.entry_observacoes.place(x=220, y=200)

        clean_Button = ctk.CTkButton(master=self.janela_os, text="Limpar Dados", width=140, fg_color="gray", command=self.limpar_ordem)
        clean_Button.place(x=380, y=410)
        
        service_Button = ctk.CTkButton(master=self.janela_os, text="Salvar", width=140, command=self.salvar_ordem)
        service_Button.place(x=540, y=410)

    def salvar_ordem(self):
        data_atual = self.entry_data_atual.get()
        local_atendimento = self.entry_local_atendimento.get()
        descricao_servico = self.entry_descricao_servico.get()
        setor = self.setor_var.get()
        prioridade = self.prioridade_var.get()
        observacoes = self.entry_observacoes.get()

        conexao = sqlite3.connect("Sistema.db")
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO chamados (data_atual, local_atendimento, descricao_servico, setor, prioridade, observacoes) VALUES (?, ?, ?, ?, ?, ?)", 
                       (data_atual, local_atendimento, descricao_servico, setor, prioridade, observacoes))

        conexao.commit()
        conexao.close()

        messagebox.showinfo(title="Estado do Cadastro", message="Parabéns! Ordem de serviço gerada com sucesso.")
    
    def limpar_ordem(self):
        self.entry_local_atendimento.delete(0, tk.END)
        self.entry_descricao_servico.delete(0, tk.END)
        self.setor_var.set('Ger.Operacional')  
        self.prioridade_var.set('Urgente')
        self.entry_observacoes.delete(0, tk.END)

        messagebox.showinfo(title="Limpar Dados", message="Todos os campos foram limpos.") 

    def visualizar_ordens(self):
        self.janela_visualizar = ctk.CTkToplevel(self)
        self.janela_visualizar.geometry("800x450")
        self.janela_visualizar.title("Lista de Chamados")

        label_titulo = ctk.CTkLabel(master=self.janela_visualizar, text="Lista de Chamados Solicitados", font=("Century Gothic bold", 18))
        label_titulo.pack(pady=10)

        frame = ctk.CTkFrame(self.janela_visualizar)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Criando a Treeview
        self.tree = ttk.Treeview(frame, columns=("ID", "Data", "Local", "Descrição", "Setor", "Prioridade", "Observações"), show="headings")

        # Definindo os cabeçalhos
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Local", text="Local")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Setor", text="Setor")
        self.tree.heading("Prioridade", text="Prioridade")
        self.tree.heading("Observações", text="Observações")

        # Configurando as colunas
        self.tree.column("ID", width=30)
        self.tree.column("Data", width=80)
        self.tree.column("Local", width=100)
        self.tree.column("Descrição", width=150)
        self.tree.column("Setor", width=100)
        self.tree.column("Prioridade", width=70)
        self.tree.column("Observações", width=150)

        # Adicionando a Treeview ao frame
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Adicionando uma barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botão para fechar a janela
        close_button = ctk.CTkButton(master=self.janela_visualizar, text="Fechar", command=self.janela_visualizar.destroy)
        close_button.pack(pady=10)

        # Carregar as ordens de serviço
        self.carregar_ordens()

    def carregar_ordens(self):
        conexao = sqlite3.connect("Sistema.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM chamados")
        ordens = cursor.fetchall()

        # Limpa a Treeview antes de adicionar as novas ordens
        for i in self.tree.get_children():
            self.tree.delete(i)

        for ordem in ordens:
            # Adiciona cada ordem como uma nova linha na Treeview
            self.tree.insert("", "end", values=ordem)

        conexao.close()

# Criar a base de dados
conexao = sqlite3.connect("Sistema.db")
cursor = conexao.cursor()

# Criar tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)""")

# Criar tabela de chamados
cursor.execute("""
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data_atual TEXT NOT NULL,
    local_atendimento TEXT NOT NULL,
    descricao_servico TEXT NOT NULL,
    setor TEXT NOT NULL,
    prioridade TEXT NOT NULL,  
    observacoes TEXT NOT NULL  
)""")

try:
    cursor.execute("ALTER TABLE chamados ADD COLUMN oficina TEXT")
except sqlite3.OperationalError:
    pass  # A coluna já existe

conexao.commit()
conexao.close()

if __name__ == "__main__":
    Application()


    