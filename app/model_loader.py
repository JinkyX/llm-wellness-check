# Load GGUF model with llama-cpp
from llama_cpp import Llama

_model = None

def load_model(model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"):
    global _model
    if _model is None:
        _model = Llama(model_path=model_path, n_ctx=2048)
    return _model