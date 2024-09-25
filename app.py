from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import datetime
import re
import time

app = Flask(__name__)

# Função para realizar o ping e armazenar resultados de pacotes
def ping(destino, lock, estatisticas):
    comando = ['ping', destino]

    if subprocess.os.name == 'nt':
        comando.append('-t')

    processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Inicializa contadores de pacotes
    total_pacotes = 0
    pacotes_perdidos = 0

    try:
        while True:
            linha = processo.stdout.readline()
            if not linha:
                break

            total_pacotes += 1  # Incrementa o total de pacotes enviados

            if "Esgotado o tempo limite do pedido" in linha or "Request timed out" in linha:
                pacotes_perdidos += 1
            else:
                match = re.search(r'tempo[=<]\d+ms', linha)
                if not match:
                    pacotes_perdidos += 1

            time.sleep(1)  # Intervalo de 1 segundo entre os pings

            # Calcula a taxa de perda de pacotes e registra
            taxa_perda = (pacotes_perdidos / total_pacotes) * 100 if total_pacotes > 0 else 0
            with lock:
                estatisticas[destino] = {
                    "total": total_pacotes,
                    "perdidos": pacotes_perdidos,
                    "taxa_perda": taxa_perda
                }

    except KeyboardInterrupt:
        print(f"Ping para {destino} interrompido.")

# Variáveis globais para estatísticas
estatisticas = {}
lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_ping', methods=['POST'])
def start_ping():
    ip1 = request.form.get('ip1')
    ip2 = request.form.get('ip2')

    estatisticas[ip1] = {"total": 0, "perdidos": 0, "taxa_perda": 0.0}
    estatisticas[ip2] = {"total": 0, "perdidos": 0, "taxa_perda": 0.0}

    threading.Thread(target=ping, args=(ip1, lock, estatisticas), daemon=True).start()
    threading.Thread(target=ping, args=(ip2, lock, estatisticas), daemon=True).start()

    return jsonify({"status": "Pinging started", "ip1": ip1, "ip2": ip2})

@app.route('/get_stats', methods=['GET'])
def get_stats():
    with lock:
        return jsonify(estatisticas)

if __name__ == '__main__':
    app.run(debug=True)
