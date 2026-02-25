# What does rpiaudio code do?

It is meant to be ran on a raspberry pi.

It repeatedly looks for files in the recordings folder and play folder.

If it finds a file in the recordings folder, it transfers this file to the server with the LLM setup, sending it to the ~/receive folder

If it finds a file in the play folder, it plays this file using the aplay command (available on raspberry pi)

__Important Assumptions:__
- it is connected to the same network as the LLM server
- you know the access credentials and IP of the LLM server
- the logic to run the recording making is running separately in another script
- the (finished) recordings will end up in the recordings folder
- a audio speaker is connected to the raspberry pi

# Where do I find all these folders (and other settings)?

In the config.toml file (in the parent directory), of course!

# Setup
1. use raspberry pi imager to write image to RPI10 with headless setup
    - hostname: rpiaudio01
    - enable ssh connect
    - enable ssh
    - enable wifi (own hotspot)
2. provide raspberry connect credentials and connect using remote screen or ssh
3. create 3 folders in the /home/pi folder: recordings, processed, play
   * recordings: created from users talking to the phone, send to LLM server ASAP, then move to processed
   * processed: recordings that have been processed
   * play: responses received from the LLM server, to be played ASAP, and then moved to processed
4. if you don’t have a ssh key yet (typically not the case):
    - generate one using ```ssh-keygen``` command (all on default is ok)
    - send the key to the receiving using ```ssh-copy-id pi@<RECEIVER_IP>```
    - When asked, provide the super secret password for the server user, and from now on you shouldn’t have to provide the password anymore
5. run script from github repo echoes-of-tomorrow within folder tests/rpiaudio
    - installation: you only need to run this command: ```pip install toml```
    - python run.py
