#importing all libraries and functions
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
import os
import subprocess
from  eventvstimegraph import generate_eventvtime_graph
from levelgraph import generate_level_graph
from eventcode import generate_eventcode_graph
import numpy as np


#Initializing flask
app = Flask(__name__)
app.secret_key='blaziken'
result_folder = 'results'
os.makedirs(result_folder, exist_ok=True)   


#Main page
@app.route('/', methods=['GET', 'POST'])
def upload_log():
    if request.method == 'POST':
        file = request.files['logFile']
        if not file or not file.filename.endswith('.log'):
            return "Only .log files are allowed.", 400

        filename = file.filename.replace(" ", "_")
        log_path = os.path.join(result_folder, filename)
        csv_filename = filename.replace('.log', '.csv')
        csv_path = os.path.join(result_folder, csv_filename)
        file.save(log_path)

        #Running the bash script for parsing
        result = subprocess.run(
            ['./apacheconverter.sh', log_path, csv_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"Parsing failed!\n{result.stderr}", 400

        return render_template('success.html',filename=csv_filename)

    return render_template('logupload.html')


#View logs page
@app.route('/logs/<filename>')
def view_logs(filename):
    filepath = os.path.join(result_folder, filename)
    with open(filepath, 'r') as f:
        lines = f.readlines()
    rows = [line.strip().split(',') for line in lines]
    headers = rows[0]
    data = rows[1:]

    return render_template('logdisplay.html', headers=headers, rows=data)


#Event logged with Time page
@app.route('/eventvtimegraph/<filename>', methods=['GET', 'POST'])
def eventvtime_page(filename):
    plot_url = None
    csv_path = os.path.join(result_folder, filename)

    if request.method == 'POST':
        selected_events = request.form.getlist('events')
        if not selected_events:
            return "Please select at least one event.", 400
        
        mintime = np.datetime64(request.form['mintime']) if 'mintime' in request.form else None
        maxtime = np.datetime64(request.form['maxtime']) if 'maxtime' in request.form else None
        out_png = os.path.join('static', 'eventvtime_plot.png')
        generate_eventvtime_graph(csv_path, selected_events, out_png, mintime, maxtime)
        plot_url = url_for('static', filename='eventvtime_plot.png')

    return render_template('eventvstimegraphs.html', plot_url=plot_url)


#Level state distribution page
@app.route('/levelgraph/<filename>', methods=['GET', 'POST'])
def level_page(filename):
    plot_url = None
    csv_path = os.path.join(result_folder, filename)

    if request.method == 'POST':
        mintime = np.datetime64(request.form['mintime']) if 'mintime' in request.form else None
        maxtime = np.datetime64(request.form['maxtime']) if 'maxtime' in request.form else None
        out_png = os.path.join('static', 'level_plot.png')
        generate_level_graph(csv_path, out_png, mintime, maxtime)
        plot_url = url_for('static', filename='level_plot.png')

    return render_template('levelgraphs.html', plot_url=plot_url)


#Event code distribution page
@app.route('/eventcodegraph/<filename>', methods=['GET', 'POST'])
def eventcode_page(filename):
    plot_url = None
    csv_path = os.path.join(result_folder, filename)

    if request.method == 'POST':
        mintime = np.datetime64(request.form['mintime']) if 'mintime' in request.form else None
        maxtime = np.datetime64(request.form['maxtime']) if 'maxtime' in request.form else None
        out_png = os.path.join('static', 'eventcode_plot.png')
        generate_eventcode_graph(csv_path, out_png, mintime, maxtime)
        plot_url = url_for('static', filename='eventcode_plot.png')
    

    return render_template('eventcodegraphs.html', plot_url=plot_url)


#Self plotting page
@app.route('/selfplot/<filename>', methods=['GET', 'POST'])
def selfplot_page(filename):
    plot_url = None
    code_path = 'selfplot.py'
    csv_path = os.path.join(result_folder, filename)
    output_path = os.path.join('static', 'selfplot_output.png')

    if request.method == 'POST':
        mintime = np.datetime64(request.form['mintime']) if 'mintime' in request.form else None
        maxtime = np.datetime64(request.form['maxtime']) if 'maxtime' in request.form else None

        code = request.form['code']
        with open(code_path, 'w') as f:
            f.write(code)

        local_vars = {}
        try:
            exec(code, local_vars)
            local_vars['generate_self_plot'](csv_path, output_path, mintime, maxtime)
            plot_url = url_for('static', filename='selfplot_output.png')
        except Exception as e:
            return f"Error during execution: {e}", 500

    with open(code_path, 'r') as f:
        code = f.read()

    return render_template('selfplot.html', code=code, plot_url=plot_url)


#Reset option for self plotting page to return original template
@app.route('/selfplot/reset', methods=['POST'])
def reset_selfplot():
    filename=request.form.get('filename')
    with open('selfplot_template.py', 'r') as template_file:
        template_code = template_file.read()
    with open('selfplot.py', 'w') as selfplot_file:
        selfplot_file.write(template_code)
    return redirect(url_for('selfplot_page',filename=filename))


#Starting flask
if __name__ == '__main__':
    app.run(debug=True)
