import numpy as np


class KMeans:
    def __init__(self, n_clusters, max_iters=100, random_state=None):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.random_state = random_state
        np.random.seed(random_state)

    def fit(self, similarity_scores):
        # Inicializar los centroides aleatoriamente
        self.centroids = similarity_scores[np.random.choice(similarity_scores.shape[0], self.n_clusters, replace=False)]

        for _ in range(self.max_iters):
            # Calcular las distancias entre los puntos y los centroides
            distances = np.linalg.norm(similarity_scores[:, np.newaxis] - self.centroids, axis=2)

            # Asignar puntos al cluster más cercano
            labels = np.argmin(distances, axis=1)

            # Actualizar los centroides como el promedio de los puntos en cada cluster
            new_centroids = np.array([similarity_scores[labels == i].mean(axis=0) for i in range(self.n_clusters)])

            # Verificar si los centroides convergieron
            if np.all(self.centroids == new_centroids):
                break

            self.centroids = new_centroids

        self.labels = labels
        return self
