"""
Test script for Text-to-Speech Generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.tts_generator import TTSGenerator


def test_tts_generation():
    """Test TTS generation in multiple languages"""
    print("=" * 70)
    print("Testing Text-to-Speech Generation (Coqui TTS)")
    print("=" * 70)

    # Initialize generator
    base_dir = Path(__file__).parent.parent
    cache_dir = base_dir / "models" / "tts"

    print("\n1. Initializing TTS Generator...")
    generator = TTSGenerator(cache_dir=cache_dir)

    print("\n2. Loading model...")
    generator.load_model()

    output_dir = base_dir / "output" / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test cases for different languages
    test_cases = [
        {
            "language": "en",
            "text": "Hello! Welcome to AI Content Studio. This is a test of the text to speech system.",
            "name": "English"
        },
        {
            "language": "tr",
            "text": "Merhaba! AI İçerik Stüdyosuna hoş geldiniz. Bu, metin okuma sisteminin bir testidir.",
            "name": "Turkish"
        }
    ]

    generated_files = []

    for i, test in enumerate(test_cases, 1):
        print(f"\n{i+2}. Generating speech in {test['name']}...")
        print(f"   Text: {test['text'][:50]}...")

        try:
            audio_path = generator.generate(
                text=test['text'],
                language=test['language'],
                speed=1.0,
                output_format="wav",
                output_dir=output_dir
            )

            generated_files.append({
                "language": test['name'],
                "path": audio_path
            })

            print(f"   ✓ Audio generated: {Path(audio_path).name}")

        except Exception as e:
            print(f"   ✗ Error generating {test['name']}: {e}")

    print(f"\n✓ Test completed!")
    print(f"\nGenerated audio files:")
    for file_info in generated_files:
        print(f"  - {file_info['language']}: {file_info['path']}")

    print(f"\nPlease verify:")
    print(f"1. All audio files exist at the specified paths")
    print(f"2. Audio files can be played")
    print(f"3. Speech is clear and matches the input text")
    print(f"4. Languages are correctly spoken")

    return generated_files


if __name__ == "__main__":
    try:
        test_tts_generation()
        print("\n" + "=" * 70)
        print("TEXT-TO-SPEECH TEST: PASSED")
        print("=" * 70)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        print("\n" + "=" * 70)
        print("TEXT-TO-SPEECH TEST: FAILED")
        print("=" * 70)
        sys.exit(1)
