# Integration using n8n
Requirements (nodejs > v20 -> check with ```node --version```)
```bash
sudo apt install nodejs npm
```

Snelle testen
```bash
npx n8n
```
Permenent install
```bash
sudo npm install -g n8n
sudo n8n start
```
Test set-up
* Set-up an environment that starts with a webhook
* Configure the webhook as POST + change the path to `audio-transcription`
* Execute this [test code](/tests/integration/send_to_n8n.py)