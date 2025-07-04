import faiss
import numpy as np
import pickle
import os

class FaissStore:
    def __init__(self, dim=384, index_path='faiss.index', metadata_path='meta.pkl'):
        self.dim = dim
        self.index_path = index_path
        self.metadata_path = metadata_path

        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.load()

    def add(self, embeddings, metadatas):
        embeddings = np.array(embeddings).astype('float32')
        self.index.add(embeddings)
        self.metadata.extend(metadatas)
        self.save()

    def search(self, query_embedding, top_k=5):
        query_embedding = np.array([query_embedding]).astype('float32')
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for i, score in zip(I[0], D[0]):
            if i < len(self.metadata):
                results.append((self.metadata[i], score))
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)

    def remove_by_pdf(self, pdf_name):
        new_meta = []
        new_embeds = []

        for i, meta in enumerate(self.metadata):
            if meta['pdf'] != pdf_name:
                new_meta.append(meta)
                emb = self.index.reconstruct(i)
                new_embeds.append(emb)

        self.index.reset()
        if new_embeds:
            self.index.add(np.array(new_embeds).astype('float32'))
        self.metadata = new_meta
        self.save()
