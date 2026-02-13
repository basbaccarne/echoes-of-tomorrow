from huggingface_hub import hf_hub_download

print("Downloading smaller ChocoLlama...")
hf_hub_download(
    repo_id="mradermacher/ChocoLlama-2-7B-instruct-GGUF",
    filename="ChocoLlama-2-7B-instruct.Q2_K.gguf",  # Vsmall model
    local_dir="./chocollama-small"
)
print("✓ Download complete!")