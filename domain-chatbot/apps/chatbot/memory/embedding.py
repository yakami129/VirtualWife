import torch
from transformers import AutoTokenizer, AutoModel

class Embedding:

    def __init__(self):
        # 初始化向量化模型
        self.model_name = 'hfl/chinese-roberta-wwm-ext'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def get_embedding_from_language_model(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt",
                                padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        return embedding
