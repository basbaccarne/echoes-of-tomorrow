**Logical path Pi side**

```mermaid
graph TD;
    IDLE-->|horn button release| PLAY_WELCOME;
    PLAY_WELCOME-->|end of audiofile|RECORDING;
    RECORDING-->|hashtag button press|SENDING;
    SENDING-->|send complete|RESPONDING;
    RESPONDING-->|end of audiofile|IDLE;
```

**Installation instructions and build**   

*Raspi - wiring*
* Connect horn button to ``GPIO4`` and ``GROUND``
* Cònnect hashtag button to ``GPIO3`` and ``GROUND``
* Connect USB telephone to USB
* Attach power
* Configure SD card

*Raspi - code*
* Update & upgrade
* Git clone
* Dependencies:
* Switch to offline network comon
* Set ID
* Set service
