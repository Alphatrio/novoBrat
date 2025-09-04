from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# In-memory storage for demo purposes
_documents = {}
_annotations = {}

@app.route('/documents', methods=['GET'])
def list_documents():
    """Return all documents."""
    return jsonify(list(_documents.values()))

@app.route('/documents', methods=['POST'])
def create_document():
    """Create a new document."""
    data = request.get_json() or {}
    doc_id = str(len(_documents) + 1)
    doc = {'id': doc_id, **data}
    _documents[doc_id] = doc
    return jsonify(doc), 201

@app.route('/documents/<doc_id>', methods=['GET'])
def get_document(doc_id):
    """Retrieve a specific document by ID."""
    doc = _documents.get(doc_id)
    if not doc:
        return jsonify({'error': 'Document not found'}), 404
    return jsonify(doc)

@app.route('/annotations', methods=['GET'])
def list_annotations():
    """Return all annotations."""
    return jsonify(list(_annotations.values()))

@app.route('/annotations', methods=['POST'])
def create_annotation():
    """Create a new annotation."""
    data = request.get_json() or {}
    ann_id = str(len(_annotations) + 1)
    ann = {'id': ann_id, **data}
    _annotations[ann_id] = ann
    return jsonify(ann), 201

@app.route('/annotations/<ann_id>', methods=['GET'])
def get_annotation(ann_id):
    """Retrieve a specific annotation by ID."""
    ann = _annotations.get(ann_id)
    if not ann:
        return jsonify({'error': 'Annotation not found'}), 404
    return jsonify(ann)

@app.errorhandler(Exception)
def handle_exception(err):
    app.logger.exception('Unhandled exception: %s', err)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
