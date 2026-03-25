#!/usr/bin/env python3
# test_hardware.py — tests LED ring, I2S amp, and USB audio

import time
import subprocess
import board
import neopixel

# ── Config ────────────────────────────────────────────────────────────────────
LED_COUNT   = 16          # adjust to your ring size
LED_PIN     = board.D10  # SPI mode for NeoPixel (avoids I2S conflict)
BRIGHTNESS  = 0.3

AUDIO_RING  = "i2s_amp"   # MAX98357A via dmix
AUDIO_USB   = "default"   # USB card

RING_WAV    = "/home/pi/echoes-of-tomorrow/audio_files/ring.wav"
USB_WAV     = "/home/pi/echoes-of-tomorrow/audio_files/pick-up_phone.wav"


# ── Helpers ───────────────────────────────────────────────────────────────────

def play(path, card):
    print(f"   ▶  aplay -D {card} {path}")
    proc = subprocess.Popen(
        ["aplay", "-D", card, path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    proc.wait()
    if proc.returncode != 0:
        print(f"   ⚠️  aplay exited with code {proc.returncode}")
    else:
        print("   ✅  Done")


# ── Test 1: LED swirl ─────────────────────────────────────────────────────────

def test_leds():
    print("\n🌈  [1/3] Testing LED ring — swirl...")
    pixels = neopixel.NeoPixel(
        LED_PIN, LED_COUNT,
        brightness=BRIGHTNESS,
        auto_write=False,
        pixel_order=neopixel.GRB,
    )

    colors = [
        (255,   0,   0),   # red
        (255, 128,   0),   # orange
        (255, 255,   0),   # yellow
        (0,   255,   0),   # green
        (0,     0, 255),   # blue
        (128,   0, 255),   # purple
    ]

    # Two full swirl cycles
    for _ in range(2):
        for color in colors:
            for i in range(LED_COUNT):
                pixels[i] = color
                pixels.show()
                time.sleep(0.03)

    pixels.fill((0, 0, 0))
    pixels.show()
    print("   ✅  Done")


# ── Test 2: I2S amp (ring) ────────────────────────────────────────────────────

def test_i2s():
    print("\n🔔  [2/3] Testing I2S amp (MAX98357A)...")
    play(RING_WAV, AUDIO_RING)


# ── Test 3: USB audio ─────────────────────────────────────────────────────────

def test_usb():
    print("\n🔊  [3/3] Testing USB audio...")
    play(USB_WAV, AUDIO_USB)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 40)
    print("  Hardware test — LED / I2S / USB")
    print("=" * 40)

    test_leds()
    time.sleep(0.5)

    test_i2s()
    time.sleep(0.5)

    test_usb()

    print("\n✅  All tests complete.")