import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Liste globale pour stocker les points ajoutés
points = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_point', methods=['POST'])
def add_point():
    data = request.get_json()
    lat = data['lat']
    lon = data['lon']
    points.append({'lat': lat, 'lon': lon})
    return jsonify({'status': 'Point ajouté avec succès'})

@app.route('/cluster', methods=['POST'])
def cluster():
    data = request.get_json()
    input_points = data['points']
    n_clusters = data.get('n_clusters', 3)

    if len(input_points) < 2:
        return jsonify({'error': 'Il faut au moins 2 points pour effectuer un clustering.'}), 400
    
    if not isinstance(n_clusters, int) or n_clusters < 1 or n_clusters > 10:
        return jsonify({'error': 'Le nombre de groupes doit être un entier entre 1 et 10.'}), 400
    
    if n_clusters > len(input_points):
        return jsonify({'error': 'Le nombre de groupes ne peut pas dépasser le nombre de points.'}), 400

    coords = np.array([[point['lat'], point['lon']] for point in input_points])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(coords)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    
    colors = [
        '#FF5733', '#33FF57', '#3357FF', '#FF33F6', '#FFC107',
        '#8E44AD', '#00BCD4', '#4CAF50', '#F44336', '#E91E63'
    ]
    colored_points = [
        {'lat': float(coords[i][0]), 'lon': float(coords[i][1]), 'color': colors[labels[i]]}
        for i in range(len(coords))
    ]
    
    response = {
        'points': colored_points,
        'centroids': centroids.tolist()
    }
    return jsonify(response)

@app.route('/reset', methods=['POST'])
def reset():
    global points
    points = []
    return jsonify({'status': 'Carte réinitialisée avec succès'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)