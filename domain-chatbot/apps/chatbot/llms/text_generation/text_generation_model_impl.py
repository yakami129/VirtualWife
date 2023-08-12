import json
from langchain.llms.base import LLM
from typing import Dict, List, Any, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
import requests
import os


class TextGenerationModel(LLM):
    max_new_tokens: int = 2048
    temperature: float = 0.5
    top_p: float = 0.9

    # .env add text_generation_api_url=xxx
    text_generation_api_url: str = os.getenv("TEXT_GENERATION_API_URL")
    chat_api_url: str = text_generation_api_url + '/api/v1/generate'

    def __init__(self):
        super().__init__()
        print("########################### init TextGeneration ###########################")
        print('text_generation_api_url:', self.text_generation_api_url)
        print('chat_api_url:', self.chat_api_url)
        print("######################################################################")

    @property
    def _llm_type(self) -> str:
        return "text_generation"

    def _call(self, prompt: str,
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              ) -> str:

        print("stop:", stop)

        body = {
            'prompt': prompt,
            'max_new_tokens': self.max_new_tokens,
            'preset': 'None',
            'do_sample': True,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'typical_p': 1,
            'epsilon_cutoff': 0,
            'eta_cutoff': 0,
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.1,
            'repetition_penalty_range': 2048,
            'top_k': 0,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,
            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': ['alan:', '<|endoftext|>', '\\end']
        }

        response = requests.post(self.chat_api_url, json=body)
        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            return result
