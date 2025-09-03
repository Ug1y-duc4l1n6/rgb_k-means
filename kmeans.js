// Simple k-means implementation for RGB pixels
function kmeans(pixels, k, maxIter=10) {
  // pixels: array of [r,g,b]
  // k: number of clusters
  // Returns: {labels, centroids}
  // Randomly initialize centroids
  let centroids = [];
  for (let i = 0; i < k; i++) {
    centroids.push(pixels[Math.floor(Math.random() * pixels.length)].slice());
  }
  let labels = new Array(pixels.length).fill(0);
  for (let iter = 0; iter < maxIter; iter++) {
    // Assign labels
    for (let i = 0; i < pixels.length; i++) {
      let minDist = Infinity, minIdx = 0;
      for (let j = 0; j < k; j++) {
        let d = dist3(pixels[i], centroids[j]);
        if (d < minDist) { minDist = d; minIdx = j; }
      }
      labels[i] = minIdx;
    }
    // Update centroids
    let sums = Array.from({length: k}, () => [0,0,0]);
    let counts = new Array(k).fill(0);
    for (let i = 0; i < pixels.length; i++) {
      let l = labels[i];
      sums[l][0] += pixels[i][0];
      sums[l][1] += pixels[i][1];
      sums[l][2] += pixels[i][2];
      counts[l]++;
    }
    for (let j = 0; j < k; j++) {
      if (counts[j] > 0) {
        centroids[j][0] = sums[j][0]/counts[j];
        centroids[j][1] = sums[j][1]/counts[j];
        centroids[j][2] = sums[j][2]/counts[j];
      }
    }
  }
  return {labels, centroids};
}
function dist3(a, b) {
  return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2;
}
