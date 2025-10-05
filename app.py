from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'txt', 'csv'}

if not os.path.exists('uploads'):
    os.makedirs('uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_ecg_file(filepath):
    df = pd.read_csv(filepath)
    return df

def create_plots(df, view_mode='separate', sampling_rate=500):
    leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c',
              '#e67e22', '#34495e', '#16a085', '#c0392b', '#2980b9', '#27ae60']
    
    time = [i / sampling_rate for i in range(len(df))]
    
    if view_mode == 'overlay':
        fig = go.Figure()
        for lead, color in zip(leads, colors):
            if lead in df.columns:
                fig.add_trace(go.Scatter(
                    x=time, y=df[lead],
                    mode='lines',
                    name=lead,
                    line=dict(color=color, width=1.5)
                ))
        
        fig.update_layout(
            title='12-Lead ECG (Overlay)',
            xaxis_title='Time (seconds)',
            yaxis_title='Amplitude (mV)',
            height=600,
            hovermode='x unified',
            template='plotly_white'
        )
        return [fig]
    
    else:  # separate
        figs = []
        for lead, color in zip(leads, colors):
            if lead in df.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=time, y=df[lead],
                    mode='lines',
                    name=lead,
                    line=dict(color=color, width=1.5)
                ))
                fig.update_layout(
                    title=f'Lead {lead}',
                    xaxis_title='Time (s)',
                    yaxis_title='Amplitude (mV)',
                    height=200,
                    margin=dict(l=50, r=20, t=40, b=30),
                    template='plotly_white'
                )
                figs.append(fig)
        return figs

def calculate_statistics(df):
    leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    stats = {}
    for lead in leads:
        if lead in df.columns:
            stats[lead] = {
                'min': float(df[lead].min()),
                'max': float(df[lead].max()),
                'mean': float(df[lead].mean()),
                'std': float(df[lead].std())
            }
    return stats

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            df = parse_ecg_file(filepath)
            view_mode = request.form.get('view_mode', 'separate')
            
            figs = create_plots(df, view_mode)
            stats = calculate_statistics(df)
            
            plots_json = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) for fig in figs]
            
            os.remove(filepath)  # Clean up
            
            return jsonify({
                'plots': plots_json,
                'stats': stats,
                'duration': len(df) / 500,
                'samples': len(df)
            })
        
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
