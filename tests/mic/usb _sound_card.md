# Capture audio using a 3.5mm jack mic and USB sound adapter

* Using a microphone with a 3.5mm jack (e.g. [the Beringer BC LAB](https://www.behringer.com/product.html?modelCode=0505-AAE)). Make sure it is TTRS (3 black rings) or, on some cards, TRS (2 rings).
* And a USB sound card like [this one](https://www.bol.com/be/nl/p/externe-geluidskaart-muziekadapter-usb-3-5-mm-mini-jack-kabel-15-cm-zwart/9300000188829315)

**check sound cards & test**
To get the ID of the sound card use
```console
arecord -l
```
*e.g card 2 || device 0*

Test (make sure you have an active playback device): 
*Record and play a 5 second snippet*
```console
arecord -D plughw:2,0 -f cd -d 5 test.wav
aplay test.wav
```

**volume settings**
```console
alsamixer 
```
* use F6 to slect you sound card
* use F4 to select capture
* This does not show live line levels, but whether capture is enabled, gain level & whether it’s muted