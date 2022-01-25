from flask import Flask,request,render_template,jsonify,abort,make_response
import numpy as np

app = Flask(__name__)
app.secret_key = "pass"

class DataStore():
    n = 0
    X = None
    X_inv = None
    invertableMatrix = True

data = DataStore()

@app.route('/')
def main():
    return(render_template("main.html",title="Main page",color="primary"))

@app.route('/inverse',methods=["GET","POST"])
def inverseMatrix():
    if request.form.get("dimension"):
        data.n = int(request.form.get("dimension"))
    if request.form.get(f"x{1}{1}"):
        data.X = np.zeros((data.n,data.n))
        for i in range(data.n):
            for j in range(data.n):
                data.X[i,j] = float(request.form.get(f"x{i}{j}"))
        if np.linalg.det(data.X)<1e-16:
            data.invertableMatrix = False
        else:
            data.invertableMatrix = True
            data.X_inv = np.linalg.inv(data.X)
    if request.form.get("clear"):
        data.n = 0
        data.X = None
        data.X_inv = None
        data.invertableMatrix = True
    if request.form.get("select"):
        data.X = None
        data.X_inv = None
        data.invertableMatrix = True

    return(render_template("inverse.html",title="Inverse Matrix",color="success",data=data))


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)