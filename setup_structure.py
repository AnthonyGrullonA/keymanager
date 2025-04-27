import os

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Carpeta creada: {path}")
    else:
        print(f"ℹ️ Carpeta ya existe: {path}")

def create_file(path, content=""):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Archivo creado: {path}")
    else:
        print(f"ℹ️ Archivo ya existe: {path}")

def main():
    # Base path
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Estructura de carpetas
    folders = [
        os.path.join(base_dir, "templates"),
        os.path.join(base_dir, "templates", "vault"),
        os.path.join(base_dir, "templates", "vault", "base"),  # Subcarpeta para fragmentos
        os.path.join(base_dir, "templates", "registration"),
        os.path.join(base_dir, "static"),
        os.path.join(base_dir, "static", "vault"),
        os.path.join(base_dir, "static", "vault", "css"),
        os.path.join(base_dir, "static", "vault", "js"),
        os.path.join(base_dir, "media"),
    ]

    for folder in folders:
        create_dir(folder)

    # Archivos base en vault app
    vault_app_dir = os.path.join(base_dir, "vault")
    files = {
        os.path.join(vault_app_dir, "forms.py"): "# forms.py - Vault Forms\n",
        os.path.join(vault_app_dir, "urls.py"): "# urls.py - Vault URLs\n",
    }

    for file_path, content in files.items():
        create_file(file_path, content)

    # Templates principales
    templates = {
        os.path.join(base_dir, "templates", "vault", "base.html"): (
            "<!-- base.html -->\n"
            "<!DOCTYPE html>\n<html lang='es'>\n<head>\n"
            "    {% include 'vault/base/header.html' %}\n"
            "</head>\n<body>\n"
            "    {% include 'vault/base/navbar.html' %}\n"
            "    <main class='container mt-5'>\n"
            "        {% block content %}{% endblock %}\n"
            "    </main>\n"
            "    {% include 'vault/base/footer.html' %}\n"
            "</body>\n</html>"
        ),
        os.path.join(base_dir, "templates", "vault", "dashboard.html"): "<!-- dashboard.html -->\n{% extends 'vault/base.html' %}\n{% block content %}<h1>Dashboard</h1>{% endblock %}",
        os.path.join(base_dir, "templates", "vault", "team_list.html"): "<!-- team_list.html -->\n{% extends 'vault/base.html' %}\n{% block content %}<h2>Teams</h2>{% endblock %}",
        os.path.join(base_dir, "templates", "vault", "team_create.html"): "<!-- team_create.html -->\n{% extends 'vault/base.html' %}\n{% block content %}<h2>Create Team</h2>{% endblock %}",
        os.path.join(base_dir, "templates", "vault", "password_list.html"): "<!-- password_list.html -->\n{% extends 'vault/base.html' %}\n{% block content %}<h2>Passwords</h2>{% endblock %}",
        os.path.join(base_dir, "templates", "vault", "password_create.html"): "<!-- password_create.html -->\n{% extends 'vault/base.html' %}\n{% block content %}<h2>Create Password</h2>{% endblock %}",
        os.path.join(base_dir, "templates", "registration", "login.html"): "<!-- login.html -->\n{% extends 'vault/base.html' %}\n{% block content %}<h2>Login</h2>{% endblock %}",
    }

    # Templates de fragmentos reutilizables (header, navbar, footer)
    fragments = {
        os.path.join(base_dir, "templates", "vault", "base", "header.html"): (
            "<!-- header.html -->\n"
            "<meta charset='UTF-8'>\n"
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
            "<title>Key Manager</title>\n"
            "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css' rel='stylesheet'>\n"
            "<link rel='stylesheet' href='{% static \"vault/css/style.css\" %}'>"
        ),
        os.path.join(base_dir, "templates", "vault", "base", "navbar.html"): (
            "<!-- navbar.html -->\n"
            "<nav class='navbar navbar-expand-lg navbar-dark bg-dark'>\n"
            "  <div class='container'>\n"
            "    <a class='navbar-brand' href='{% url \"vault:dashboard\" %}'>Key Manager</a>\n"
            "    <div class='collapse navbar-collapse'>\n"
            "      <ul class='navbar-nav ms-auto'>\n"
            "        {% if user.is_authenticated %}\n"
            "          <li class='nav-item'><a class='nav-link' href='{% url \"vault:team_list\" %}'>Equipos</a></li>\n"
            "          <li class='nav-item'><a class='nav-link' href='{% url \"vault:password_list\" %}'>Contraseñas</a></li>\n"
            "          <li class='nav-item'><a class='nav-link' href='{% url \"logout\" %}'>Salir</a></li>\n"
            "        {% else %}\n"
            "          <li class='nav-item'><a class='nav-link' href='{% url \"login\" %}'>Entrar</a></li>\n"
            "        {% endif %}\n"
            "      </ul>\n"
            "    </div>\n"
            "  </div>\n"
            "</nav>"
        ),
        os.path.join(base_dir, "templates", "vault", "base", "footer.html"): (
            "<!-- footer.html -->\n"
            "<footer class='text-center mt-5 mb-3'>\n"
            "  <small>&copy; 2024 - Key Manager System</small>\n"
            "</footer>\n"
            "<script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js'></script>\n"
            "<script src='{% static \"vault/js/app.js\" %}'></script>"
        ),
    }

    for template_path, content in {**templates, **fragments}.items():
        create_file(template_path, content)

    print("\n🚀 Estructura básica completa creada correctamente.")

if __name__ == "__main__":
    main()
