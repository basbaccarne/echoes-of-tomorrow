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

## Building the agent
Type `http://localhost:5678` in your browser to open the visual n8n editor

