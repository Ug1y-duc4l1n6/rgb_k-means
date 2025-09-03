from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    k = int(request.form['k'])
    img = Image.open(file).convert('RGB')
    arr = np.array(img)
    h, w, c = arr.shape
    pixels = arr.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(pixels)
    centroids = kmeans.cluster_centers_.astype(int)
    # Recolor image
    recolored = centroids[labels].reshape(h, w, 3).astype(np.uint8)
    recolored_img = Image.fromarray(recolored)
    # Encode recolored image
    buf = BytesIO()
    recolored_img.save(buf, format='PNG')
    buf.seek(0)
    recolored_b64 = base64.b64encode(buf.read()).decode('utf-8')
    # Prepare RGB scatter plot
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pixels[:,0], pixels[:,1], pixels[:,2], c=pixels/255, s=1, alpha=0.1)
    ax.scatter(centroids[:,0], centroids[:,1], centroids[:,2], c=centroids/255, s=100, marker='X', edgecolor='k')
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')
    plt.tight_layout()
    buf2 = BytesIO()
    plt.savefig(buf2, format='PNG')
    plt.close(fig)
    buf2.seek(0)
    rgb_b64 = base64.b64encode(buf2.read()).decode('utf-8')
    return jsonify({
        'recolored': recolored_b64,
        'rgb_plot': rgb_b64,
        'centroids': centroids.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
