# app.py
from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Conectar ao banco de dados e inserir os dados
        connection = sqlite3.connect('teela.db')
        cursor = connection.cursor()

        # Aqui você pode fazer a verificação do usuário
        cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            return "Login bem-sucedido!"
        else:
            return "E-mail ou senha incorretos."

    # Renderiza o formulário de login
    return render_template_string(open('login.html').read())

if __name__ == '__main__':
    app.run(debug=True)
