#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# Flask Project Generator - Gerador de Projetos Flask Modular
# Criador: Allan José (Al4xs) - code.allan
# Versão: 2.0 (Python - multiplataforma)
# ═══════════════════════════════════════════════════════════════

import sys
import os
import argparse
from pathlib import Path

# ─── Suporte a cores ANSI no Windows ───────────────────────────
def _setup_colors():
    """Ativa cores ANSI no Windows e retorna o dicionário de estilos."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Habilita ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            supports_color = True
        except Exception:
            supports_color = False
    else:
        supports_color = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    if supports_color:
        return {
            "GREEN":   "\033[0;32m",
            "CYAN":    "\033[0;36m",
            "YELLOW":  "\033[1;33m",
            "RED":     "\033[0;31m",
            "BLUE":    "\033[0;34m",
            "MAGENTA": "\033[0;35m",
            "BOLD":    "\033[1m",
            "RESET":   "\033[0m",
        }
    else:
        return {k: "" for k in ["GREEN","CYAN","YELLOW","RED","BLUE","MAGENTA","BOLD","RESET"]}

C = _setup_colors()

# ─── Símbolos ───────────────────────────────────────────────────
CHECKMARK = "✅"
ROCKET    = "🚀"
GEAR      = "⚙️"
DATABASE  = "🗄️"
LOCK      = "🔐"
PAINT     = "🎨"
WARNING   = "⚠️"
ERROR_SYM = "❌"
STAR      = "⭐"
CODE      = "💻"

def c(color, text):
    return f"{C[color]}{text}{C['RESET']}"

def bold(text):
    return f"{C['BOLD']}{text}{C['RESET']}"

# ─── Ajuda ──────────────────────────────────────────────────────
def show_help():
    print()
    print(f"{bold(c('BLUE', '╔════════════════════════════════════════════════════════════════════════╗'))}")
    print(f"{bold(c('BLUE', '║'))}  {ROCKET} {bold(c('GREEN', 'GERADOR DE PROJETOS FLASK MODULAR'))}                             {bold(c('BLUE', '║'))}")
    print(f"{bold(c('BLUE', '║'))}     {CODE} {c('CYAN', 'Criado por: Allan José (Al4xs) - code.allan')}                   {bold(c('BLUE', '║'))}")
    print(f"{bold(c('BLUE', '╚════════════════════════════════════════════════════════════════════════╝'))}")
    print()
    print(f"{bold(c('CYAN', 'USO:'))}")
    print(f"  {c('YELLOW', 'python startproject.py')} {c('GREEN', '<nome_do_projeto>')} [opções]")
    print()
    print(f"{bold(c('CYAN', 'PARÂMETROS:'))}")
    print(f"  {c('GREEN', '<nome_do_projeto>')}      Nome do diretório do projeto ({bold('obrigatório')})")
    print()
    print(f"{bold(c('CYAN', 'OPÇÕES:'))}")
    print(f"  {c('GREEN', '-r')} <rotas>             Lista de rotas separadas por vírgula")
    print(f"                          {c('CYAN', 'Default: home')}")
    print(f"                          {c('CYAN', 'Exemplo: -r home,about,contact')}")
    print()
    print(f"  {c('GREEN', '-D')} <Models>            Ativa banco de dados SQLite com models")
    print(f"                          {c('CYAN', 'Exemplo: -D User,Post,Comment')}")
    print()
    print(f"  {c('GREEN', '--api')}                   Cria projeto em modo API (retorna JSON)")
    print(f"                          {c('CYAN', 'Sem templates HTML, apenas endpoints JSON')}")
    print()
    print(f"  {c('GREEN', '-l, --login')} <rota>      Adiciona sistema de autenticação Flask-Login")
    print(f"                          {c('CYAN', 'Requer -D com pelo menos um model')}")
    print(f"                          {c('CYAN', 'Exemplo: -l login ou --login login')}")
    print()
    print(f"  {c('GREEN', '--tailwind')} <tipo>      Configura Tailwind CSS")
    print(f"                          {c('CYAN', 'cdn')}   - Via CDN (desenvolvimento rápido)")
    print(f"                          {c('CYAN', 'build')} - Com build system (produção)")
    print()
    print(f"  {c('GREEN', '-h, --help')}              Mostra esta mensagem de ajuda")
    print()
    print(f"{bold(c('CYAN', 'EXEMPLOS DE USO:'))}")
    print()
    print(f"  {PAINT} {c('YELLOW', 'Projeto simples:')}")
    print( "     python startproject.py meuapp")
    print(f"     {c('CYAN', '→ Cria projeto com rota home básica')}")
    print()
    print(f"  {PAINT} {c('YELLOW', 'Site com múltiplas páginas:')}")
    print( "     python startproject.py meusite -r home,about,contact")
    print(f"     {c('CYAN', '→ Cria 3 rotas com templates HTML')}")
    print()
    print(f"  {DATABASE} {c('YELLOW', 'Projeto com banco de dados:')}")
    print( "     python startproject.py webapp -r home,produtos -D User,Product")
    print(f"     {c('CYAN', '→ Cria projeto com SQLite e 2 models')}")
    print()
    print(f"  {LOCK} {c('YELLOW', 'App com autenticação:')}")
    print( "     python startproject.py authapp -r home,dashboard -D User --login login")
    print(f"     {c('CYAN', '→ Sistema completo de login/logout')}")
    print()
    print(f"  {PAINT} {c('YELLOW', 'Site moderno com Tailwind:')}")
    print( "     python startproject.py modernapp -r home,about -D User --tailwind cdn")
    print(f"     {c('CYAN', '→ Design responsivo com Tailwind CSS via CDN')}")
    print()
    print(f"  {GEAR} {c('YELLOW', 'API REST:')}")
    print( "     python startproject.py myapi -r api,users -D User,Post --api")
    print(f"     {c('CYAN', '→ Endpoints JSON para consumo de API')}")
    print()
    print(f"  {ROCKET} {c('YELLOW', 'Projeto completo (produção):')}")
    print( "     python startproject.py fullapp -r home,dashboard,profile -D User,Post --login login --tailwind build")
    print(f"     {c('CYAN', '→ App completo com auth, DB e Tailwind otimizado')}")
    print()
    print(f"{bold(c('CYAN', 'ESTRUTURA DO PROJETO GERADO:'))}")
    print(f"  projeto/")
    print(f"  ├── main.py              {c('CYAN', '# Aplicação Flask principal')}")
    print(f"  ├── routes/              {c('CYAN', '# Módulos de rotas (blueprints)')}")
    print(f"  │   ├── home/            {c('CYAN', '# Exemplo de rota')}")
    print(f"  │   │   ├── templates/   {c('CYAN', '# Templates HTML da rota')}")
    print(f"  │   │   └── home.py      {c('CYAN', '# Blueprint da rota')}")
    print(f"  ├── models.py            {c('CYAN', '# Models do banco (se -D)')}")
    print(f"  └── extensions.py        {c('CYAN', '# Extensões Flask (se -D)')}")
    print()
    print(f"{bold(c('CYAN', 'APÓS GERAR O PROJETO:'))}")
    print(f"  {c('YELLOW', '1.')} cd seu_projeto")
    print(f"  {c('YELLOW', '2.')} pip install -r requirements.txt")
    print(f"  {c('YELLOW', '3.')} python main.py")
    print(f"  {c('YELLOW', '4.')} Acesse: {c('GREEN', 'http://localhost:5000')}")
    print()
    sys.exit(0)

# ─── Escrita de arquivos ─────────────────────────────────────────
def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def append(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(content)

# ─── Geração de conteúdo ────────────────────────────────────────
def models_import(models):
    return ", ".join(models)

def gen_main_py(db, login, login_name, models):
    lines = ["from flask import Flask", "from routes import blueprints"]
    if db and login:
        lines.append("from extensions import db, login_manager")
    elif db:
        lines.append("from extensions import db")
    lines.append("")
    lines.append("app = Flask(__name__)")
    lines.append("")
    if db:
        lines.append('app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"')
        lines.append('app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False')
    lines.append('app.secret_key = "altere-sua-secret-key-aqui"')
    lines.append("")
    if db:
        lines.append("db.init_app(app)")
    if db and login:
        lines.append("login_manager.init_app(app)")
        lines.append(f'login_manager.login_view = "{login_name}.{login_name}"')
    lines.append("")
    lines.append("for bp in blueprints:")
    lines.append("    app.register_blueprint(bp)")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    if db:
        lines.append("    with app.app_context():")
        lines.append("        db.create_all()")
    lines.append('    app.run(host="0.0.0.0", port=5000, debug=True)')
    return "\n".join(lines) + "\n"

def gen_routes_init(rotas, login, login_name):
    lines = []
    for r in rotas:
        lines.append(f"from .{r}.{r} import {r}_bp")
    if login:
        lines.append(f"from .{login_name}.{login_name} import {login_name}_bp")
    lines.append("")
    lines.append("blueprints = [")
    for r in rotas:
        lines.append(f"    {r}_bp,")
    if login:
        lines.append(f"    {login_name}_bp,")
    lines.append("]")
    return "\n".join(lines) + "\n"

def gen_route_py_api(rota, db, models):
    lines = ["from flask import Blueprint, jsonify"]
    if db:
        lines.append("from extensions import db")
        lines.append(f"from models import {models_import(models)}")
    lines.append("")
    lines.append(f'{rota}_bp = Blueprint("{rota}", __name__)')
    lines.append("")
    lines.append(f'@{rota}_bp.route("/{rota}")')
    lines.append(f"def {rota}():")
    lines.append(f'    return jsonify({{"message": "API da rota {rota} funcionando!"}})')
    return "\n".join(lines) + "\n"

def gen_route_py_html(rota, db, models, tailwind):
    lines = ["from flask import Blueprint, render_template"]
    if db:
        lines.append("from extensions import db")
        lines.append(f"from models import {models_import(models)}")
    lines.append("")
    is_home = rota == "home"
    if tailwind:
        if is_home:
            lines.append(f'{rota}_bp = Blueprint("{rota}", __name__, template_folder="templates")')
        else:
            lines.append(f'{rota}_bp = Blueprint("{rota}", __name__, template_folder="templates", url_prefix="/{rota}")')
    else:
        if is_home:
            lines.append(f'{rota}_bp = Blueprint("{rota}", __name__, template_folder="templates", static_folder="static", static_url_path="/{rota}/static")')
        else:
            lines.append(f'{rota}_bp = Blueprint("{rota}", __name__, template_folder="templates", static_folder="static", static_url_path="/{rota}/static", url_prefix="/{rota}")')
    lines.append("")
    lines.append(f'@{rota}_bp.route("/")')
    lines.append(f"def {rota}():")
    lines.append(f'    return render_template("{rota}.html")')
    return "\n".join(lines) + "\n"

def gen_template_tailwind_cdn(rota):
    return f"""\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Página {rota}</title>
</head>

<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="text-center">
        <h1 class="text-4xl font-bold text-green-400 mb-4">
            ✨ Rota {rota} criada com sucesso!
        </h1>
        <p class="text-gray-300">
            Powered by Flask + Tailwind CSS
        </p>
    </div>

    <script src="https://cdn.tailwindcss.com" defer></script>
</body>
</html>
"""

def gen_template_tailwind_build(rota):
    return f"""\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Página {rota}</title>

    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/output.css') }}}}">
</head>

<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="text-center">
        <h1 class="text-4xl font-bold text-green-400 mb-4">
            ✨ Rota {rota} criada com sucesso!
        </h1>
        <p class="text-gray-300">
            Powered by Flask + Tailwind CSS (Build)
        </p>
    </div>
</body>
</html>
"""

def gen_template_plain(rota):
    return f"""\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Página {rota}</title>

    <link rel="stylesheet" href="{{{{ url_for('{rota}.static', filename='css/style.css') }}}}">
</head>

<body>
    <div class="container">
        <h1>Olá, rota {rota} criada com sucesso!</h1>
    </div>
</body>
</html>
"""

def gen_style_css():
    return """\
* {
    margin: 0;
    padding: 0;
}

body {
  font-family: Arial, sans-serif;
  color: #ddd;
  background-color: #121212;
}

h1 {
  color: #4CAF50;
}
"""

# ─── Login blueprints ────────────────────────────────────────────
def gen_login_py_api(login_name, models):
    first_model = models[0]
    return f"""\
from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required
from models import {models_import(models)}
from extensions import login_manager

{login_name}_bp = Blueprint("{login_name}", __name__)

@login_manager.user_loader
def load_user(user_id):
    return {first_model}.query.get(int(user_id))

@{login_name}_bp.route("/{login_name}", methods=["POST"])
def {login_name}():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = {first_model}.query.filter_by(username=username).first()
        if user:
            login_user(user)
            return jsonify({{"success": True, "message": "Login realizado com sucesso", "user": {{"id": user.id, "username": user.username}}}})

    return jsonify({{"success": False, "message": "Credenciais inválidas"}}), 401

@{login_name}_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({{"success": True, "message": "Logout realizado com sucesso"}})
"""

def gen_login_py_tailwind(login_name, models):
    first_model = models[0]
    return f"""\
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import {models_import(models)}
from extensions import login_manager

{login_name}_bp = Blueprint("{login_name}", __name__, template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return {first_model}.query.get(int(user_id))

@{login_name}_bp.route("/{login_name}", methods=["GET", "POST"])
def {login_name}():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            user = {first_model}.query.filter_by(username=username).first()
            if user:
                login_user(user)
                return redirect(url_for("home.home"))

        flash("Credenciais inválidas")

    return render_template("{login_name}.html")

@{login_name}_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("{login_name}.{login_name}"))
"""

def gen_login_py_plain(login_name, models):
    first_model = models[0]
    return f"""\
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import {models_import(models)}
from extensions import login_manager

{login_name}_bp = Blueprint("{login_name}", __name__, template_folder="templates", static_folder="static", static_url_path="/{login_name}/static")

@login_manager.user_loader
def load_user(user_id):
    return {first_model}.query.get(int(user_id))

@{login_name}_bp.route("/{login_name}", methods=["GET", "POST"])
def {login_name}():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            user = {first_model}.query.filter_by(username=username).first()
            if user:
                login_user(user)
                return redirect(url_for("home.home"))

        flash("Credenciais inválidas")

    return render_template("{login_name}.html")

@{login_name}_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("{login_name}.{login_name}"))
"""

def gen_login_template_cdn(login_name):
    return f"""\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Login</title>
</head>

<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 class="text-3xl font-bold text-green-400 mb-6 text-center">
            🔐 Login
        </h1>

        {{% with messages = get_flashed_messages() %}}
            {{% if messages %}}
                <div class="bg-red-600 text-white p-3 rounded mb-4">
                    {{{{ messages[0] }}}}
                </div>
            {{% endif %}}
        {{% endwith %}}

        <form method="POST" class="space-y-4">
            <input type="text" name="username" placeholder="Usuário" required
                   class="w-full p-3 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-green-400 focus:outline-none">

            <input type="password" name="password" placeholder="Senha" required
                   class="w-full p-3 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-green-400 focus:outline-none">

            <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded transition duration-200">
                Entrar
            </button>
        </form>
    </div>
    <script src="https://cdn.tailwindcss.com" defer></script>
</body>
</html>
"""

def gen_login_template_build(login_name):
    return f"""\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Login</title>

    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/output.css') }}}}">
</head>

<body class="bg-gray-900 text-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 class="text-3xl font-bold text-green-400 mb-6 text-center">
            🔐 Login
        </h1>

        {{% with messages = get_flashed_messages() %}}
            {{% if messages %}}
                <div class="bg-red-600 text-white p-3 rounded mb-4">
                    {{{{ messages[0] }}}}
                </div>
            {{% endif %}}
        {{% endwith %}}

        <form method="POST" class="space-y-4">
            <input type="text" name="username" placeholder="Usuário" required
                   class="w-full p-3 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-green-400 focus:outline-none">

            <input type="password" name="password" placeholder="Senha" required
                   class="w-full p-3 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-green-400 focus:outline-none">

            <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded transition duration-200">
                Entrar
            </button>
        </form>
    </div>
</body>
</html>
"""

def gen_login_template_plain(login_name):
    return f"""\
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Login</title>

    <link rel="stylesheet" href="{{{{ url_for('{login_name}.static', filename='css/style.css') }}}}">
</head>

<body>
    <div class="container">
        <h1>Página de Login</h1>

        {{% with messages = get_flashed_messages() %}}
            {{% if messages %}}
                <div class="error">{{{{ messages[0] }}}}</div>
            {{% endif %}}
        {{% endwith %}}

        <form method="POST">
            <input type="text" name="username" placeholder="Usuário" required>
            <input type="password" name="password" placeholder="Senha" required>
            <button type="submit">Entrar</button>
        </form>
    </div>
</body>
</html>
"""

def gen_extensions_py(login):
    lines = ["from flask_sqlalchemy import SQLAlchemy"]
    if login:
        lines.append("from flask_login import LoginManager")
    lines.append("")
    lines.append("db = SQLAlchemy()")
    if login:
        lines.append("login_manager = LoginManager()")
    return "\n".join(lines) + "\n"

def gen_models_py(models, login):
    lines = ["from extensions import db"]
    if login:
        lines.append("from flask_login import UserMixin")
    lines.append("")

    for i, model in enumerate(models):
        if login and i == 0:
            lines += [
                f"class {model}(db.Model, UserMixin):",
                "    id = db.Column(db.Integer, primary_key=True)",
                "    username = db.Column(db.String(80), unique=True, nullable=False)",
                "    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())",
                "",
                "    def __repr__(self):",
                f"        return f'<{model} {{self.username}}>'",
                "",
            ]
        else:
            lines += [
                f"class {model}(db.Model):",
                "    id = db.Column(db.Integer, primary_key=True)",
                "    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())",
                "",
                "    def __repr__(self):",
                f"        return f'<{model} {{self.id}}>'",
                "",
            ]
    return "\n".join(lines)

def gen_package_json(project_name):
    return f"""\
{{
  "name": "{project_name}",
  "version": "1.0.0",
  "description": "Flask app with Tailwind CSS",
  "scripts": {{
    "dev": "npx tailwindcss -i ./src/input.css -o ./static/css/output.css --watch",
    "build": "npx tailwindcss -i ./src/input.css -o ./static/css/output.css --minify"
  }},
  "devDependencies": {{
    "tailwindcss": "^3.4.0"
  }}
}}
"""

def gen_tailwind_config():
    return """\
module.exports = {
  content: ["./routes/**/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

def gen_gitignore(tailwind_build):
    lines = ["__pycache__/", "*.pyc", "*.db"]
    if tailwind_build:
        lines += ["node_modules/", "src/", "tailwind.config.js", "package.json", "package-lock.json"]
    return "\n".join(lines) + "\n"

def gen_requirements(db, login):
    lines = ["Flask==2.3.3"]
    if db:
        lines.append("Flask-SQLAlchemy==3.0.5")
    if login:
        lines.append("Flask-Login==0.6.3")
    return "\n".join(lines) + "\n"

# ─── Argparse customizado (para -r e -D sem --) ──────────────────
class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\n{ERROR_SYM} {c('RED', message)}")
        print(c('YELLOW', "Use -h ou --help para ver os comandos disponíveis"))
        sys.exit(1)

def parse_args():
    # Pré-processamento manual para suportar -D e --api sem argparse completo
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        show_help()

    project_name = args[0]
    rest = args[1:]

    rotas = ["home"]
    models = []
    db = False
    api = False
    login = False
    login_name = ""
    tailwind = False
    tailwind_type = ""

    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg in ("-h", "--help"):
            show_help()
        elif arg == "-r":
            if i + 1 < len(rest):
                rotas = [r.strip() for r in rest[i + 1].split(",") if r.strip()]
                i += 2
            else:
                print(f"\n{ERROR_SYM} {c('RED', 'Erro: use -r seguido dos nomes das rotas (ex: -r home,login)')}")
                sys.exit(1)
        elif arg == "-D":
            if i + 1 < len(rest):
                db = True
                models = [m.strip() for m in rest[i + 1].split(",") if m.strip()]
                i += 2
            else:
                print(f"\n{ERROR_SYM} {c('RED', 'Erro: use -D seguido do(s) nome(s) das Models (ex: -D Usuario,Post)')}")
                sys.exit(1)
        elif arg == "--api":
            api = True
            i += 1
        elif arg in ("-l", "--login"):
            if i + 1 < len(rest):
                login = True
                login_name = rest[i + 1]
                i += 2
            else:
                print(f"\n{ERROR_SYM} {c('RED', 'Erro: use -l ou --login seguido do nome da rota (ex: -l login)')}")
                sys.exit(1)
        elif arg == "--tailwind":
            if i + 1 < len(rest) and rest[i + 1] in ("cdn", "build"):
                tailwind = True
                tailwind_type = rest[i + 1]
                i += 2
            else:
                print(f"\n{ERROR_SYM} {c('RED', 'Erro: use --tailwind cdn ou --tailwind build')}")
                sys.exit(1)
        else:
            print(f"\n{ERROR_SYM} {c('RED', f'Parâmetro desconhecido: {arg}')}")
            print(c('YELLOW', "Use -h ou --help para ver os comandos disponíveis"))
            sys.exit(1)

    # Validação: --login exige -D com pelo menos um model
    if login and (not db or not models):
        print(f"\n{ERROR_SYM} {c('RED', 'Erro: --login requer -D com pelo menos um model (ex: -D User --login login)')}")
        sys.exit(1)

    return project_name, rotas, models, db, api, login, login_name, tailwind, tailwind_type

# ─── Main ────────────────────────────────────────────────────────
def main():
    project_name, rotas, models, db, api, login, login_name, tailwind, tailwind_type = parse_args()

    # Resolve caminho absoluto (igual ao realpath do bash)
    projeto = Path(project_name).resolve()

    # ── Banner ──
    print()
    print(f"{bold(c('MAGENTA', '╔════════════════════════════════════════════════════════════════╗'))}")
    print(f"{bold(c('MAGENTA', '║'))}  {ROCKET} {bold(c('CYAN', 'CRIANDO PROJETO FLASK MODULAR'))}                       {bold(c('MAGENTA', '║'))}")
    print(f"{bold(c('MAGENTA', '║'))}     {STAR} {c('YELLOW', 'By Allan José (Al4xs) - code.allan')}                 {bold(c('MAGENTA', '║'))}")
    print(f"{bold(c('MAGENTA', '╚════════════════════════════════════════════════════════════════╝'))}")
    print()
    print(f"{GEAR} {bold(c('CYAN', 'Projeto:'))} {c('GREEN', projeto.name)}")
    print(f"{GEAR} {bold(c('CYAN', 'Rotas:'))} {c('GREEN', ' '.join(rotas))}")
    if db:
        print(f"{DATABASE} {c('CYAN', 'Banco de dados:')} {c('GREEN', 'Habilitado')} - Models: {c('GREEN', ' '.join(models))}")
    if api:
        print(f"{GEAR} {c('CYAN', 'Modo API:')} {c('GREEN', 'Habilitado')}")
    if login:
        print(f"{LOCK} {c('CYAN', 'Sistema de Login:')} {c('GREEN', 'Habilitado')} - Rota: {c('GREEN', login_name)}")
    if tailwind:
        print(f"{PAINT} {c('CYAN', 'Tailwind CSS:')} {c('GREEN', f'Habilitado ({tailwind_type})')}")
    print()

    # ── Estrutura base ──
    (projeto / "routes").mkdir(parents=True, exist_ok=True)

    # ── main.py ──
    write(projeto / "main.py", gen_main_py(db, login, login_name, models))

    # ── routes/__init__.py ──
    write(projeto / "routes" / "__init__.py", gen_routes_init(rotas, login, login_name))

    # ── Criar rotas normais ──
    for rota in rotas:
        rota_dir = projeto / "routes" / rota
        if tailwind:
            (rota_dir / "templates").mkdir(parents=True, exist_ok=True)
        else:
            (rota_dir / "templates").mkdir(parents=True, exist_ok=True)
            (rota_dir / "static" / "css").mkdir(parents=True, exist_ok=True)

        if api:
            write(rota_dir / f"{rota}.py", gen_route_py_api(rota, db, models))
        else:
            write(rota_dir / f"{rota}.py", gen_route_py_html(rota, db, models, tailwind))

            if tailwind and tailwind_type == "cdn":
                write(rota_dir / "templates" / f"{rota}.html", gen_template_tailwind_cdn(rota))
            elif tailwind and tailwind_type == "build":
                write(rota_dir / "templates" / f"{rota}.html", gen_template_tailwind_build(rota))
            else:
                write(rota_dir / "templates" / f"{rota}.html", gen_template_plain(rota))
                write(rota_dir / "static" / "css" / "style.css", gen_style_css())

    # ── Criar rota de login (-l) ──
    if login:
        login_dir = projeto / "routes" / login_name

        if api:
            login_dir.mkdir(parents=True, exist_ok=True)
            write(login_dir / f"{login_name}.py", gen_login_py_api(login_name, models))
        elif tailwind:
            (login_dir / "templates").mkdir(parents=True, exist_ok=True)
            write(login_dir / f"{login_name}.py", gen_login_py_tailwind(login_name, models))
        else:
            (login_dir / "templates").mkdir(parents=True, exist_ok=True)
            (login_dir / "static" / "css").mkdir(parents=True, exist_ok=True)
            write(login_dir / f"{login_name}.py", gen_login_py_plain(login_name, models))

        if not api:
            if tailwind and tailwind_type == "cdn":
                write(login_dir / "templates" / f"{login_name}.html", gen_login_template_cdn(login_name))
            elif tailwind and tailwind_type == "build":
                write(login_dir / "templates" / f"{login_name}.html", gen_login_template_build(login_name))
            else:
                write(login_dir / "templates" / f"{login_name}.html", gen_login_template_plain(login_name))

    # ── Banco de dados ──
    if db:
        write(projeto / "extensions.py", gen_extensions_py(login))
        write(projeto / "models.py", gen_models_py(models, login))

    # ── Tailwind build ──
    if tailwind and tailwind_type == "build":
        (projeto / "static" / "css").mkdir(parents=True, exist_ok=True)
        write(projeto / "package.json", gen_package_json(projeto.name))
        write(projeto / "tailwind.config.js", gen_tailwind_config())
        (projeto / "src").mkdir(parents=True, exist_ok=True)
        write(projeto / "src" / "input.css",
              "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
        write(projeto / "static" / "css" / "output.css",
              "/* Tailwind CSS será gerado aqui com: npm run build */\n")

    # ── requirements.txt ──
    write(projeto / "requirements.txt", gen_requirements(db, login))

    # ── .gitignore ──
    write(projeto / ".gitignore", gen_gitignore(tailwind and tailwind_type == "build"))

    # ── Resumo final ──
    print()
    print(f"{bold(c('GREEN', '╔════════════════════════════════════════════════════════════════╗'))}")
    print(f"{bold(c('GREEN', '║'))}  {CHECKMARK} {bold(c('GREEN', 'PROJETO CRIADO COM SUCESSO!'))}                         {bold(c('GREEN', '║'))}")
    print(f"{bold(c('GREEN', '╚════════════════════════════════════════════════════════════════╝'))}")
    print()
    print(f"{ROCKET} {bold(c('CYAN', 'Para rodar o projeto:'))}")
    print(f"   {c('YELLOW', f'cd {projeto.name}')}")
    if tailwind and tailwind_type == "build":
        print(f"   {c('YELLOW', 'npm install')}")
        print(f"   {c('YELLOW', 'npm run build')} {c('CYAN', '(ou npm run dev para watch)')}")
    print(f"   {c('YELLOW', 'pip install -r requirements.txt')}")
    print(f"   {c('YELLOW', 'python main.py')}")
    print()
    print(f"{STAR} {bold(c('CYAN', 'Recursos criados:'))}")
    rotas_str = " ".join(rotas)
    print(f"   {CHECKMARK} {c('GREEN', f'{len(rotas)} rota(s): {rotas_str}')}")
    if db:
        models_str = " ".join(models)
        print(f"   {DATABASE} {c('GREEN', f'{len(models)} model(s): {models_str}')}")
    if login:
        print(f"   {LOCK} {c('GREEN', 'Sistema de autenticação')}")
    if api:
        print(f"   {GEAR} {c('GREEN', 'Endpoints API')}")
    if tailwind:
        print(f"   {PAINT} {c('GREEN', f'Tailwind CSS ({tailwind_type})')}")
    print()
    print(f"{bold(c('MAGENTA', '╔════════════════════════════════════════════════════════════════╗'))}")
    print(f"{bold(c('MAGENTA', '║'))}  {CODE} {c('YELLOW', 'Criado por: Allan José (Al4xs) - code.allan')}         {bold(c('MAGENTA', '║'))}")
    print(f"{bold(c('MAGENTA', '║'))}     {STAR} {c('CYAN', 'Bom desenvolvimento! 🎉')}                               {bold(c('MAGENTA', '║'))}")
    print(f"{bold(c('MAGENTA', '╚════════════════════════════════════════════════════════════════╝'))}")
    print()

if __name__ == "__main__":
    main()
