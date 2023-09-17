# llama2

## models

```sh
python3 convert.py models/llama-2-7b-chat
./quantize ./models/llama-2-7b-chat/ggml-model-f16.gguf ./models/llama-2-7b-chat/ggml-model-q4_0.gguf q4_0
./main -m ./models/llama-2-7b-chat/ggml-model-q4_0.gguf -n 128
```