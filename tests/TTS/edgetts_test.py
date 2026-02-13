import asyncio
import edge_tts

async def speak(text, 
                voice="nl-BE-ArnaudNeural",
                rate="+0%",      # Snelheid: -50% tot +100%
                pitch="+0Hz",    # Toonhoogte: -50Hz tot +50Hz
                volume="+0%"):   # Volume: -50% tot +50%
    
    print(f"🔊 Settings: rate={rate}, pitch={pitch}, volume={volume}")
    
    communicate = edge_tts.Communicate(
        text, 
        voice,
        rate=rate,
        pitch=pitch,
        volume=volume
    )
    
    await communicate.save("tts_output.mp3")

# Test verschillende settings
text = "Welkom bij de bibliotheek. Ik kan je helpen met informatie over toekomstbeelden van België."


asyncio.run(speak(text, rate="-10%", pitch="-5Hz"))