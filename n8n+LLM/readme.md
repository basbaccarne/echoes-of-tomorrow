# Building the agent in n8n (for Windows)

## Installing n8n

n8n is a visual agent builder we need to bring all pieces of the puzzle together.

---

### 🛠 Requirements

Before installing, ensure your environment meets the following criteria:

* **Node.js:** Version `20.x` or higher. (Confirmed compatible with **Raspberry Pi 5**).
* **npm:** Installed and updated.

| Check Version | Command |
| :--- | :--- |
| **Node.js** | `node --version` |
| **npm** | `npm --version` |

---

### 🚀 Installation & Setup

Run `npm install -g n8n` in your terminal.

Run `n8n start` to start

Type `http://localhost:5678` in your browser to open the visual n8n editor

You will need to create an account in n8n

full details: https://docs.n8n.io/hosting/installation/npm/

## Installing Ollama (The LLM brain)
Download & Install: Go to https://ollama.com/download/windows and install the Windows version.

Pull the Model: Open a new PowerShell window and type `ollama run llama3.2` (This downloads a very capable, lightweight model that supports Dutch. Once it's done downloading, you can close the window.)

For the reading documents in the RAG we will pull a second model better suited for this task, run `ollama pull nomic-embed-text` (also works for Dutch documents)

## Building the agent
Type `http://localhost:5678` in your browser to open the visual n8n editor

### Creating the RAG -> to be completed
create file path: "C:\Users\XXX\.n8n-files\knowledge_base_echoes-of-tomorrow.txt". It is very important the folder is named exactly **.n8n-files** as n8n can only enter this folder. In this folder, save the knowledge base file (txt)

