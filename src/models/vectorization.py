import numpy as np
import requests
import faiss
import json
import re

from tqdm.auto import tqdm


class SemanticVectorizer:
    def __init__(self, api_key, models_config):
        self.api_key = api_key
        self.models_config = models_config
        self.model = None
        self.usage_price_per_token = 0
        self.texts = []
        self.embeddings = []
        self.faiss_index = None

    def set_model(self, model_name):
        found = False
        for group in self.models_config["models"]:
            for variant in group["variants"]:
                if variant["model"] == model_name:
                    self.model = model_name
                    self.usage_price_per_token = variant.get("usage_price_per_token", 0)
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f"Model {model_name} not found in configuration.")

    def preprocess_text(self, text):
        """
        Preprocesses the text before embedding.
        """
        text = text.lower()
        return text.replace("\n", " ").strip()

    def read_and_process_markdown(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        sections = re.split(r"\n(#{1,3} .*)\n", text)
        self.texts = [self.preprocess_text(sections[0])] + [
            self.preprocess_text(f"{sections[i]}\n{sections[i + 1]}")
            for i in range(1, len(sections), 2)
        ]
        return self.texts

    def query_openai_embedding(self, text):
        preprocessed_text = self.preprocess_text(text)
        url = "https://api.openai.com/v1/embeddings"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "input": preprocessed_text,
            "model": self.model,
        }
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            embedding = np.array(data["data"][0]["embedding"], dtype="float32")
            return embedding, data.get("usage", {})
        else:
            print(
                f"Failed to generate embedding: Status code {response.status_code}, Response: {response.text}"
            )
            return None, None

    def generate_embeddings(self, save_index=False, index_path=None, texts_path=None):
        total_cost = 0
        for text in tqdm(self.texts):
            embedding, usage = self.query_openai_embedding(text)
            if embedding is not None:
                self.embeddings.append(embedding)
                total_cost += self.calculate_cost(usage)
        self.embeddings = np.array(self.embeddings)
        self.create_faiss_index()

        if save_index and index_path:
            self.save_faiss_index(index_path)
            if texts_path:  # Save texts at specified path
                with open(texts_path, "w", encoding="utf-8") as f:
                    json.dump(self.texts, f)

        return total_cost

    def load_texts(self, texts_path):
        """Loads texts from a specified path."""
        try:
            with open(texts_path, "r", encoding="utf-8") as f:
                self.texts = json.load(f)
        except Exception as e:
            print(f"Error loading texts: {e}")

    def create_faiss_index(self):
        if self.embeddings.size > 0:
            dimension = self.embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatL2(dimension)
            self.faiss_index.add(self.embeddings)
        else:
            print("No embeddings to add to FAISS index.")

    def search_similar_sections(self, query_text, num_results):
        query_embedding, _ = self.query_openai_embedding(query_text)
        if self.faiss_index is None:
            raise ValueError(
                "FAISS index is not initialized. Please create the index before searching."
            )
        if query_embedding is None:
            return []
        distances, indices = self.faiss_index.search(
            np.array([query_embedding], dtype="float32"), num_results
        )
        return [self.texts[idx] for idx in indices[0] if idx < len(self.texts)]

    def save_faiss_index(self, index_path, texts_path):
        # Save the FAISS index
        if self.faiss_index:
            faiss.write_index(self.faiss_index, index_path)
            print(f"FAISS index saved successfully to {index_path}.")

        # Save the texts
        with open(texts_path, "w", encoding="utf-8") as f:
            json.dump(self.texts, f)
        print(f"Texts saved successfully to {texts_path}.")

    def load_faiss_index(self, index_path):
        self.faiss_index = faiss.read_index(index_path)

    def calculate_cost(self, usage):
        total_tokens = usage.get("total_tokens", 0)
        total_price = total_tokens * self.usage_price_per_token
        return total_price
