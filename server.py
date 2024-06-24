from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Uložiště pro data a PINy
scans = {}

# Funkce pro získání dat ze SGRM Brokeru
def get_sgrm_data():
    # Příklad získání dat ze SGRM Brokeru, upravte podle potřeby
    sgrm_data = {
        "example_key_1": "example_value_1",
        "example_key_2": "example_value_2",
        # přidejte další data dle potřeby
    }
    return sgrm_data

# HTML šablona pro zobrazení dat
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Scan Data</title>
</head>
<body>
    <h1>Scan Data</h1>
    {% if pin %}
        <h2>Data for PIN: {{ pin }}</h2>
        <p><strong>Public IP:</strong> {{ data.public_ip }}</p>
        <p><strong>OS Version:</strong> {{ data.os_version }}</p>
        <p><strong>Recent Apps:</strong> {{ data.recent_apps }}</p>
        <p><strong>Strange Named Apps:</strong></p>
        <ul>
            {% for app in data.strange_named_apps %}
                <li>{{ app }}</li>
            {% endfor %}
        </ul>
        <p><strong>SGRM Broker Data:</strong></p>
        <ul>
            {% for key, value in data.sgrm_data.items() %}
                <li>{{ key }}: {{ value }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <h2>No data found for this PIN</h2>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    pin = request.args.get('pin')
    data = scans.get(pin)
    return render_template_string(html_template, pin=pin, data=data)

@app.route('/scan/<pin>', methods=['POST'])
def scan(pin):
    data = request.json
    data['sgrm_data'] = get_sgrm_data()
    scans[pin] = data
    return jsonify({'status': 'success'})

@app.route('/scan/<pin>', methods=['GET'])
def get_scan(pin):
    data = scans.get(pin)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'No data found for this PIN'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30031)
