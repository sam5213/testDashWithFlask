import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Flask
from flask_socketio import SocketIO, send, emit

app = dash.Dash(__name__)
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


if __name__ == '__main__':
    socketio.run(server, debug=True)