import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Flask, render_template, request, abort
from flask_socketio import SocketIO, send, emit

app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
server = Flask(__name__)
socketio = SocketIO(server)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # в миллисекундах
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_figure(n):
    # Сгенерируйте случайные данные для графика
    data = [go.Bar(x=['A', 'B', 'C'], y=[random.randint(0, 10) for _ in range(3)])]
    return {'data': data, 'layout': go.Layout(title='Live Update Graph')}

@socketio.on('connect')
def connect():
    print('Client connected')
    emit('response', 'Connected!')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@app.route('/', methods=['GET', 'POST'])
def webhook(path):
    if request.method == 'POST':
        data = request.get_json()
        if data and 'ref' in data and data['ref'] == 'webhook':
            return render_template(path or 'index.html', base_url=base_url)
        else:
            abort(400)
    else:
        abort(405)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template(path or 'index.html', base_url=base_url)


if __name__ == '__main__':
    base_url = request.host_url
    port = int(os.environ.get('PORT', 5000))
    socketio.run(server, port=port, debug=True)
