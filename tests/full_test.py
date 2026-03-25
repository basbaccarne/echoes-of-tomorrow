#!/usr/bin/env python3
# tests/full_test.py — tests LED ring, I2S amp, and USB audio then shuts down

import time
import subprocess
import logging
import board
import neopixel

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_PATH = "/home/pi/echoes-of-tomorrow/tests/full_test.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger().addHandler(logging.StreamHandler())

# ── Config ────────────────────────────────────────────────────────────────────
LED_COUNT  = 24
LED_PIN    = board.MOSI
BRIGHTNESS = 0.3

AUDIO_RING = "i2s_amp"
AUDIO_USB  = "default"

RING_WAV   = "/home/pi/echoes-of-tomorrow/audio_files/ring.wav"
USB_WAV    = "/home/pi/echoes-of-tomorrow/audio_files/pick-up_phone.wav"


# ── Helpers ───────────────────────────────────────────────────────────────────

def play(path, card):
    logging.info(f"   ▶  aplay -D {card} {path}")
    proc = subprocess.Popen(
        ["aplay", "-D", card, path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    proc.wait()
    if proc.returncode != 0:
        logging.warning(f"   ⚠️  aplay exited with code {proc.returncode}")
    else:
        logging.info("   ✅  Done")


# ── Test 1: LED swirl ─────────────────────────────────────────────────────────

def test_leds():
    logging.info("[1/3] Testing LED ring — swirl...")
    pixels = neopixel.NeoPixel(
        LED_PIN, LED_COUNT,
        brightness=BRIGHTNESS,
        auto_write=False,
        pixel_order=neopixel.GRB,
    )

    colors = [
        (255,   0,   0),
        (255, 128,   0),
        (255, 255,   0),
        (0,   255,   0),
        (0,     0, 255),
        (128,   0, 255),
    ]

    for _ in range(2):
        for color in colors:
            for i in range(LED_COUNT):
                pixels[i] = color
                pixels.show()
                time.sleep(0.03)

    pixels.fill((0, 0, 0))
    pixels.show()
    logging.info("   ✅  Done")


# ── Test 2: I2S amp ───────────────────────────────────────────────────────────

def test_i2s():
    logging.info("[2/3] Testing I2S amp (MAX98357A)...")
    play(RING_WAV, AUDIO_RING)


# ── Test 3: USB audio ─────────────────────────────────────────────────────────

def test_usb():
    logging.info("[3/3] Testing USB audio...")
    play(USB_WAV, AUDIO_USB)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.info("=" * 40)
    logging.info("  Hardware test — LED / I2S / USB")
    logging.info("=" * 40)

    try:
        test_leds()
        time.sleep(0.5)

        test_i2s()
        time.sleep(0.5)

        test_usb()

        logging.info("✅  All tests complete.")

    except Exception as e:
        logging.error(f"❌  Test failed: {e}")

    finally:
        logging.info("🔌  Shutting down...")
        subprocess.run(["sudo", "shutdown", "-h", "now"])