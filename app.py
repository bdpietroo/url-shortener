from flask import Flask, render_template, request, redirect, url_for
import string
import random

app = Flask(__name__)

url_mapping = {}

def gerar_codigo_curto(tamanho=6):
    """
    Gera um código curto aleatório para a URL.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        original_url = request.form.get('url')
        if original_url:
            # Adiciona o esquema HTTP se estiver faltando
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'http://' + original_url

            # Gera código curto único
            code = gerar_codigo_curto()
            while code in url_mapping:
                code = gerar_codigo_curto()

            # Armazena o mapeamento
            url_mapping[code] = original_url

            # Monta a URL curta completa
            short_url = request.host_url + code

    return render_template('index.html', short_url=short_url)

@app.route('/<code>')
def redirecionar(code):
    """
    Redireciona para a URL original com base no código curto.
    """
    original_url = url_mapping.get(code)
    if original_url:
        return redirect(original_url)
    else: 
        return render_template('index.html', error="Link inválido ou expirado."), 404
    
if __name__ == '__main__':
    app.run(debug=True)