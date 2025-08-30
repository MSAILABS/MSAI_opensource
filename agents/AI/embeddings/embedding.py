import torch, os

from transformers import AutoModel, AutoTokenizer

from AI.agents.utilities import resolve_device
    

from typing import Any, List

from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.embeddings import BaseEmbedding


class CustomEmbeddings(BaseEmbedding):
    _model: Any = PrivateAttr()
    _instruction: str = PrivateAttr()
    _tokenizer: Any = PrivateAttr()
    _device: Any = PrivateAttr()

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        instruction: str = "Represent a document for semantic search:",
        device_id: str = 'cpu',
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        # Convert all characters except alphabet and number to "_"
        model_name_dir = ''.join([c if c.isalnum() else '_' for c in model_name])
        # if first character is number added A in front, so that dir name should not give eeror
        if model_name_dir and model_name_dir[0].isdigit():
            model_name_dir = 'A' + model_name_dir

        token_dir = f"./model_data/{model_name_dir}_token"
        model_dir = f"./model_data/{model_name_dir}_model"

        if os.path.isdir(token_dir) and os.path.isdir(model_dir):
            print('LOADING BAI')
            self._tokenizer = AutoTokenizer.from_pretrained(f"./model_data/{model_name_dir}_token")
            self._model = AutoModel.from_pretrained(f"./model_data/{model_name_dir}_model")
            self._device = resolve_device(device_id)
            print(f'device {device_id}')
            self._model.to(self._device)
        else:
            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
            self._model = AutoModel.from_pretrained(model_name)
            self._tokenizer.save_pretrained(f"./model_data/{model_name_dir}_token")
            self._model.save_pretrained(f"./model_data/{model_name_dir}_model")

        self._instruction = instruction

    def get_embedding(self, text, cpu=True):
        """
        Returns a [CLS] vector for the given text, with automatic
        device alignment between model, inputs, and outputs.
 
        Parameters
        ----------
        text : str or list[str]
            The input text(s) to embed.
        cpu : bool
            If True, output will be moved to CPU NumPy array.
            If False, output stays as a tensor on the model's device.
        """
        # Detect model device dynamically
        device = next(self._model.parameters()).device
 
        # Ensure model is on the detected device
        self._model.to(device)
 
        # Tokenize & move inputs to same device
        inputs = self._tokenizer(
            [text],
            padding=True,
            truncation=True,
            return_tensors='pt'
        ).to(device)
 
        with torch.no_grad():
            embeddings = self._model(**inputs).last_hidden_state
 
        cls_vec = embeddings
 
        if cpu:
            return cls_vec.cpu().detach().numpy()
        else:
            return cls_vec.detach()
        
    def get_embedding_torch(self, text):
        inputs = self._tokenizer(text, return_tensors='pt')
        outputs = self._model(**inputs)
        embeddings = outputs.last_hidden_state
        embeddings = torch.mean(embeddings, dim=1)
        return embeddings.detach().cpu().numpy()

    @classmethod
    def class_name(cls) -> str:
        return "instructor"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        embeddings = self.get_embedding(text=query)
        # embeddings = self._model.encode([[self._instruction, query]])
        return embeddings[0][0]

    def _get_text_embedding(self, text: str) -> List[float]:
        embeddings = self.get_embedding(text=text)
        # embeddings = self._model.encode([[self._instruction, text]])
        return embeddings[0][0]

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        text = ""

        for t in texts:
            text += t

        embeddings = self.get_embedding(text=text)
        return embeddings[0]