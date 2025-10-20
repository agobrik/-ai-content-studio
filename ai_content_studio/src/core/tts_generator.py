"""
Text-to-Speech Generator - Multi-engine high-quality TTS
Supports multiple TTS engines:
1. Edge-TTS (Microsoft Edge, high quality, free, online)
2. gTTS (Google TTS, simple, free, online)
3. pyttsx3 (Offline, system voices)
"""

from gtts import gTTS
from pathlib import Path
import datetime
from typing import Optional, Literal


class TTSGenerator:
    """Generate speech from text using multiple high-quality TTS engines"""

    def __init__(self, cache_dir: Path = None, engine: str = "edge"):
        """
        Initialize the TTS generator

        Args:
            cache_dir: Directory to cache models
            engine: TTS engine to use ('edge', 'gtts', 'pyttsx3')
        """
        self.cache_dir = cache_dir
        self.engine = engine
        self.pyttsx3_engine = None
        self.available_voices = []

        print(f"TTS Generator initialized with engine: {engine}")

        # Initialize selected engine
        if engine == "pyttsx3":
            self._init_pyttsx3()
        elif engine == "edge":
            print("Edge-TTS will be initialized on-demand")
        else:  # gtts
            print("gTTS will be used (simple, online)")

    def _init_pyttsx3(self):
        """Initialize pyttsx3 offline engine"""
        try:
            import pyttsx3
            self.pyttsx3_engine = pyttsx3.init()

            # Get available voices
            voices = self.pyttsx3_engine.getProperty('voices')
            self.available_voices = [(v.id, v.name, v.languages) for v in voices]

            print(f"pyttsx3 initialized with {len(self.available_voices)} voices")
            for i, (vid, vname, vlangs) in enumerate(self.available_voices[:5]):
                print(f"  {i+1}. {vname} ({vlangs})")

        except Exception as e:
            print(f"Failed to initialize pyttsx3: {e}")
            print("Install with: pip install pyttsx3")
            self.pyttsx3_engine = None

    def load_model(self):
        """Load the TTS model"""
        if self.engine == "pyttsx3" and self.pyttsx3_engine is None:
            self._init_pyttsx3()
        print(f"{self.engine.upper()} TTS ready to use")

    def generate(
        self,
        text: str,
        language: str = "en",
        speed: float = 1.0,
        output_format: str = "wav",
        output_dir: Path = None,
        reference_audio: str = None,
        voice: str = None
    ) -> Path:
        """
        Generate high-quality speech from text

        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'es', 'tr')
            speed: Speech speed multiplier
            output_format: Output format (wav, mp3)
            output_dir: Directory to save the generated audio
            reference_audio: Not supported yet
            voice: Specific voice to use (engine-dependent)

        Returns:
            Path to the generated audio file
        """
        print(f"Generating speech using {self.engine.upper()}...")
        print(f"Text: {text[:80]}...")
        print(f"Language: {language}, Voice: {voice or 'default'}")

        # Create output directory
        if output_dir is None:
            output_dir = Path("./output/audio")

        output_dir.mkdir(parents=True, exist_ok=True)

        # Route to appropriate engine
        if self.engine == "edge":
            return self._generate_edge_tts(text, language, speed, output_format, output_dir, voice)
        elif self.engine == "pyttsx3":
            return self._generate_pyttsx3(text, speed, output_format, output_dir, voice)
        else:  # gtts
            return self._generate_gtts(text, language, speed, output_format, output_dir)

    def _generate_edge_tts(
        self, text: str, language: str, speed: float,
        output_format: str, output_dir: Path, voice: Optional[str]
    ) -> Path:
        """Generate speech using Microsoft Edge TTS (high quality)"""
        try:
            import edge_tts
            import asyncio

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_edge_{timestamp}.mp3"
            output_path = output_dir / filename

            # Voice mapping for Edge TTS
            voice_map = {
                "en": voice or "en-US-AriaNeural",  # Female
                "en-male": "en-US-GuyNeural",
                "en-female": "en-US-AriaNeural",
                "es": voice or "es-ES-ElviraNeural",
                "fr": voice or "fr-FR-DeniseNeural",
                "de": voice or "de-DE-KatjaNeural",
                "it": voice or "it-IT-ElsaNeural",
                "pt": voice or "pt-BR-FranciscaNeural",
                "tr": voice or "tr-TR-EmelNeural",
                "ru": voice or "ru-RU-SvetlanaNeural",
                "ja": voice or "ja-JP-NanamiNeural",
                "ko": voice or "ko-KR-SunHiNeural",
                "zh-cn": voice or "zh-CN-XiaoxiaoNeural",
            }

            selected_voice = voice_map.get(language, "en-US-AriaNeural")

            # Speed formatting for Edge TTS (-50% to +100%)
            rate = f"+{int((speed - 1.0) * 100)}%" if speed > 1.0 else f"{int((speed - 1.0) * 100)}%"

            print(f"Using Edge TTS voice: {selected_voice} at rate: {rate}")

            # Generate with Edge TTS
            async def generate():
                communicate = edge_tts.Communicate(text, selected_voice, rate=rate)
                await communicate.save(str(output_path))

            # Run async function
            asyncio.run(generate())

            # Convert to WAV if requested
            if output_format == "wav":
                output_path = self._convert_mp3_to_wav(output_path)

            print(f"High-quality audio saved to: {output_path}")
            return output_path

        except ImportError:
            print("Edge-TTS not installed. Install with: pip install edge-tts")
            print("Falling back to gTTS...")
            return self._generate_gtts(text, language, speed, output_format, output_dir)
        except Exception as e:
            print(f"Error with Edge-TTS: {e}")
            print("Falling back to gTTS...")
            return self._generate_gtts(text, language, speed, output_format, output_dir)

    def _generate_pyttsx3(
        self, text: str, speed: float, output_format: str,
        output_dir: Path, voice: Optional[str]
    ) -> Path:
        """Generate speech using pyttsx3 (offline)"""
        if self.pyttsx3_engine is None:
            raise RuntimeError("pyttsx3 engine not available")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_pyttsx3_{timestamp}.{output_format}"
        output_path = output_dir / filename

        # Set voice if specified
        if voice and self.available_voices:
            for vid, vname, _ in self.available_voices:
                if voice.lower() in vname.lower() or voice == vid:
                    self.pyttsx3_engine.setProperty('voice', vid)
                    print(f"Using voice: {vname}")
                    break

        # Set speech rate
        rate = self.pyttsx3_engine.getProperty('rate')
        self.pyttsx3_engine.setProperty('rate', int(rate * speed))

        # Generate
        self.pyttsx3_engine.save_to_file(text, str(output_path))
        self.pyttsx3_engine.runAndWait()

        print(f"Offline audio saved to: {output_path}")
        return output_path

    def _generate_gtts(
        self, text: str, language: str, speed: float,
        output_format: str, output_dir: Path
    ) -> Path:
        """Generate speech using Google TTS (simple, online)"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_gtts_{timestamp}.mp3"
        output_path = output_dir / filename

        # Map language codes
        lang_map = {
            "zh-cn": "zh-CN",
            "zh": "zh-CN"
        }
        gtts_lang = lang_map.get(language, language)

        # Generate speech with gTTS
        tts = gTTS(text=text, lang=gtts_lang, slow=(speed < 0.8))
        tts.save(str(output_path))

        # Convert to WAV if requested
        if output_format == "wav":
            output_path = self._convert_mp3_to_wav(output_path)

        print(f"Audio saved to: {output_path}")
        return output_path

    def _convert_mp3_to_wav(self, mp3_path: Path) -> Path:
        """Convert MP3 to WAV using ffmpeg directly"""
        wav_path = mp3_path.with_suffix('.wav')

        try:
            import subprocess

            print(f"Converting {mp3_path.name} to WAV using ffmpeg...")

            # Use ffmpeg directly (faster and more reliable)
            result = subprocess.run(
                ['ffmpeg', '-i', str(mp3_path), '-acodec', 'pcm_s16le', '-ar', '44100', str(wav_path), '-y'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Remove MP3 file
                mp3_path.unlink()
                print(f"Converted to WAV: {wav_path.name}")
                return wav_path
            else:
                print(f"ffmpeg error: {result.stderr}")
                print("Keeping MP3 format")
                return mp3_path

        except FileNotFoundError:
            print("ffmpeg not found. MP3 to WAV conversion requires ffmpeg.")
            print("Install ffmpeg: winget install Gyan.FFmpeg")
            print("Keeping MP3 format")
            return mp3_path
        except Exception as e:
            print(f"Error converting to WAV: {e}")
            print("Keeping MP3 format")
            return mp3_path

    def get_available_voices(self, language: str = "en") -> list:
        """Get list of available voices for the current engine"""
        if self.engine == "edge":
            # Edge TTS voices
            edge_voices = {
                "en": ["en-US-AriaNeural (Female)", "en-US-GuyNeural (Male)", "en-GB-SoniaNeural (Female)", "en-AU-NatashaNeural (Female)"],
                "es": ["es-ES-ElviraNeural (Female)", "es-ES-AlvaroNeural (Male)", "es-MX-DaliaNeural (Female)"],
                "fr": ["fr-FR-DeniseNeural (Female)", "fr-FR-HenriNeural (Male)", "fr-CA-SylvieNeural (Female)"],
                "de": ["de-DE-KatjaNeural (Female)", "de-DE-ConradNeural (Male)", "de-AT-IngridNeural (Female)"],
                "it": ["it-IT-ElsaNeural (Female)", "it-IT-DiegoNeural (Male)"],
                "pt": ["pt-BR-FranciscaNeural (Female)", "pt-BR-AntonioNeural (Male)", "pt-PT-RaquelNeural (Female)"],
                "tr": ["tr-TR-EmelNeural (Female)", "tr-TR-AhmetNeural (Male)"],
                "ru": ["ru-RU-SvetlanaNeural (Female)", "ru-RU-DmitryNeural (Male)"],
                "ja": ["ja-JP-NanamiNeural (Female)", "ja-JP-KeitaNeural (Male)"],
                "ko": ["ko-KR-SunHiNeural (Female)", "ko-KR-InJoonNeural (Male)"],
                "zh-cn": ["zh-CN-XiaoxiaoNeural (Female)", "zh-CN-YunxiNeural (Male)", "zh-CN-XiaoyiNeural (Female)"],
            }
            return edge_voices.get(language, edge_voices["en"])

        elif self.engine == "pyttsx3":
            return [f"{vname}" for vid, vname, vlangs in self.available_voices]

        else:  # gtts
            return ["Default Voice (gTTS)"]

    def generate_batch(
        self,
        texts: list,
        language: str = "en",
        speed: float = 1.0,
        output_format: str = "wav",
        output_dir: Path = None
    ) -> list:
        """
        Generate speech for multiple texts

        Args:
            texts: List of texts to convert
            language: Language code
            speed: Speech speed multiplier
            output_format: Output format (wav, mp3)
            output_dir: Directory to save generated audio files

        Returns:
            List of paths to generated audio files
        """
        audio_paths = []

        for text in texts:
            audio_path = self.generate(
                text=text,
                language=language,
                speed=speed,
                output_format=output_format,
                output_dir=output_dir
            )
            audio_paths.append(audio_path)

        return audio_paths

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        # gTTS supports many languages
        return ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'ja', 'ko', 'hu', 'hi']

    def unload_model(self):
        """Unload model from memory (not needed for gTTS)"""
        print("gTTS does not require unloading")
