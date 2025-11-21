from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import subprocess  # Untuk speedtest kalau perlu
# Paste SEMUA kode Python asli kamu di sini (dari import sampai main_menu)
# Hapus welcome_screen() dan main_menu(), karena di-wrap di API

app = Flask(__name__)
CORS(app)  # Izinkan frontend akses API

@app.route('/api/waster', methods=['POST'])
async def api_waster():
    data = request.json
    num_workers = int(data.get('num_workers', 30))
    target_bytes = data.get('target_bytes', float('inf'))
    mode_name = {10: 'Slow', 30: 'Stabil', 60: 'Cepat', 100: 'Agresif'}.get(num_workers, 'Stabil')
    
    logs = []  # Kumpul log untuk return
    # Jalankan fungsi asli kamu
    try:
        await run_waster_async(num_workers, mode_name, target_bytes)
        logs.append({'msg': '✅ Selesai!', 'type': 'success'})  # Contoh, tambah real log capture
    except Exception as e:
        return jsonify({'error': str(e)})
    return jsonify({'logs': logs})

@app.route('/api/stresser', methods=['POST'])
async def api_stresser():
    data = request.json
    num_workers = int(data.get('num_workers', 150))
    url = data.get('url')
    total_requests = data.get('total_requests', float('inf'))
    mode_name = {50: 'Ringan', 150: 'Sedang', 300: 'Kuat', 500: 'Ekstrem'}.get(num_workers, 'Sedang')
    
    logs = []
    try:
        await run_stresser_async(num_workers, mode_name, url, total_requests)
        logs.append({'msg': '✅ Selesai!', 'type': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})
    return jsonify({'logs': logs})

@app.route('/api/speedtest', methods=['POST'])
def api_speedtest():
    try:
        # Jalankan speedtest asli kamu (asumsi modul speedtest installed)
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        return jsonify({'download': f'{download:.2f}', 'upload': f'{upload:.2f}', 'ping': f'{ping:.2f}'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return open('index.html').read()  # Serve frontend HTML

if __name__ == '__main__':
    app.run(debug=True)
