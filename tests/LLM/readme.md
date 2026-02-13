# Processing the data
A question is asked to a person from the future. An LLM trained on futures research data replies.

## The models
### 1. Ollama 
* Local
* Free
* Privacy friendly

Download the general model
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Dutch options
```bash
ollama pull llama3.2:3b  # small, quick on pi
# or
ollama pull gemma2:2b  # even smaller
```
* [testcode](/tests/LLM/ollama.py)

### 2. ChocoLlama
Dutch version of Ollama (the model might be a bit big for our raspi setup)
* [Github repo](https://github.com/ChocoLlamaModel/ChocoLlama)
* [Hugging Face](https://huggingface.co/ChocoLlama)

1. Download
[download chocollama using this python code](/tests/LLM/chocollama_download.py)   

2. Make Modelfile
    ```bash
    cat > Modelfile-small << 'EOF'
    FROM ./chocollama-small/ChocoLlama-2-7B-instruct.Q2_K.gguf
    SYSTEM Je bent een jonge ouder die in de toekomst leeft. In het jaar 2050.
    EOF
    ```

3. Import in Ollama
    ```bash
    ollama create chocollama-small -f Modelfile-small
    ```

4. Test direct
    ```bash
    ollama run chocollama "Hoe worden kinderen opgevoed in jouw tijd?"
    ```

5. Run test code
    [testcode](/tests/LLM/chocolama.py)

### 3. Open AI
```bash
pip install openai
```

* [testcode](/tests/LLM/openai.py)