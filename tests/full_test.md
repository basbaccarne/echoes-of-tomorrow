allow shutdown
```bash
sudo visudo
```

add at the botom
``ìni
pi ALL=(ALL) NOPASSWD: /usr/sbin/shutdown
`` 

Create service
```bash
sudo nano /etc/systemd/system/hardware-test.service
```
```ini
[Unit]
Description=Hardware test — LED / I2S / USB
After=sound.target

[Service]
Type=oneshot
User=pi
WorkingDirectory=/home/pi/echoes-of-tomorrow/tests
ExecStart=/usr/bin/python3 /home/pi/echoes-of-tomorrow/tests/full_test.py
RemainAfterExit=no
StandardOutput=append:/home/pi/full_test.log
StandardError=append:/home/pi/full_test.log

[Install]
WantedBy=multi-user.target
```
actiavate service
```bash
sudo systemctl daemon-reload
sudo systemctl enable hardware-test.service
sudo systemctl start hardware-test.service
```

