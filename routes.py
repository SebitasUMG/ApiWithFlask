import os

from flask import Flask, jsonify, request
from api.avl_tree import AVLTree
import pandas as pd

app = Flask(__name__)
avl_tree = AVLTree()

@app.router('/')
def index():
    return "Api usando Flask."


@app.route('/api/batch-data', methods=['POST'])
def batch_data():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file.save(os.path.join('data', file.filename))
        data = pd.read_csv(os.path.join('data', file.filename))
        for index, row in data.iterrows():
            avl_tree.insert(row['id'], row)
        return jsonify({'message': 'Data loaded successfully'}), 201


@app.route('/api/print_tree', methods=['GET'])
def print_tree():
    tree_structure = avl_tree.print_tree()
    return jsonify(tree_structure), 200


@app.route('/api/insert-record', methods=['POST'])
def insert_record():
    data = request.get_json()
    record_id = data.get('key')
    record_info = data.get('value')
    avl_tree.insert(record_id, record_info)
    return jsonify({'message': 'Record inserted successfully'})


@app.route('/api/search-record/<int:record_id>', methods=['GET'])
def search_record(record_id):
    print(record_id)
    record = avl_tree.search(record_id)
    if record is not None:
        return jsonify(record), 200
    else:
        return jsonify({'message': 'Record not found'}), 404


@app.route('/api/group-info', methods=['GET'])
def group_info():
    group_info = {
        'members': [
            {'name': 'Josue Sebastian Mancilla', 'id': '9490-22-1157',
             'contribution': 'Creacion de endpoint carga de registros, e insercion de datos en el archivo, contribucion en el arbol avl'},
            {'name': 'Willy Estuardo Culajay Asturias', 'id': '9490-22-3432',
             'contribution': 'Creacion de enpoint de busqueda y muestra de informacion de integrantes, contribucion en el arbol avl'},
        ]
    }
    return jsonify(group_info)


if __name__ == '__main__':
    app.run()
