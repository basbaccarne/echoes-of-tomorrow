from hume import HumeVoiceClient
from hume.models.config import LanguageConfig
import asyncio

# Je hebt een Hume API key nodig van: https://platform.hume.ai

async def test_hume_evi():
    """Test Hume's Empathic Voice Interface"""
    
    client = HumeVoiceClient(api_key="jouw-hume-api-key")
    
    # Configure Dutch voice
    config = LanguageConfig(
        language="nl",  # Nederlands
    )
    
    # Start een voice sessie
    async with client.connect(config=config) as socket:
        print("🎤 Connected to Hume EVI")
        
        # Send audio of text
        await socket.send_text_input(
            "Vertel me over groene mobiliteit in België"
        )
        
        # Receive response
        async for message in socket:
            if message.type == "audio_output":
                # Save audio
                with open("hume_response.wav", "wb") as f:
                    f.write(message.data)
                print("✓ Got audio response")
                break

# Run
asyncio.run(test_hume_evi())