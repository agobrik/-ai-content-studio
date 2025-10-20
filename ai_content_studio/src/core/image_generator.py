"""
Image Generator - High-Quality Stable Diffusion implementation with SDXL support
"""

import sys
import os
import warnings

# Suppress ALL warnings about ONNX
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

# Block ONNX pipeline imports (we don't need them)
class _FakeOnnxRuntimeModel:
    """Fake class to satisfy issubclass() checks"""
    pass

class _FakeOnnxModule:
    """Fake module that returns a fake class for OnnxRuntimeModel"""
    def __getattr__(self, name):
        if name == 'OnnxRuntimeModel':
            return _FakeOnnxRuntimeModel
        return None

sys.modules['diffusers.pipelines.onnx_utils'] = _FakeOnnxModule()

import torch
from diffusers import (
    StableDiffusionXLPipeline,
    StableDiffusionPipeline,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler
)
from pathlib import Path
import datetime
from PIL import Image


class ImageGenerator:
    """Generate high-quality images using Stable Diffusion XL"""

    def __init__(self, model_name: str = "stabilityai/stable-diffusion-xl-base-1.0",
                 cache_dir: Path = None, use_refiner: bool = False):
        """
        Initialize the image generator

        Args:
            model_name: HuggingFace model identifier
            cache_dir: Directory to cache models
            use_refiner: Whether to use SDXL refiner for enhanced quality
        """
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.use_refiner = use_refiner
        self.pipe = None
        self.refiner = None
        self.device = self._get_device()
        self.is_sdxl = "xl" in model_name.lower()

    def _get_device(self):
        """Get the appropriate device (CUDA/CPU)"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def load_model(self):
        """Load the Stable Diffusion model (SDXL or SD 1.5)"""
        if self.pipe is not None:
            return

        print(f"Loading model: {self.model_name}")
        print(f"Using device: {self.device}")

        # Determine which pipeline to use
        if self.is_sdxl:
            # Load SDXL pipeline for high quality
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                cache_dir=self.cache_dir,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None,
            )

            # Use Euler Ancestral scheduler for better quality with SDXL
            self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
                self.pipe.scheduler.config
            )

            # Load refiner if requested
            if self.use_refiner:
                print("Loading SDXL refiner for enhanced quality...")
                try:
                    from diffusers import StableDiffusionXLImg2ImgPipeline
                    self.refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                        "stabilityai/stable-diffusion-xl-refiner-1.0",
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                        cache_dir=self.cache_dir,
                        use_safetensors=True,
                        variant="fp16" if self.device == "cuda" else None,
                    )
                    self.refiner = self.refiner.to(self.device)
                    print("Refiner loaded successfully")
                except Exception as e:
                    print(f"Could not load refiner: {e}")
                    self.refiner = None
        else:
            # Load standard SD 1.5 pipeline
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                cache_dir=self.cache_dir,
                safety_checker=None,
            )

            # Use DPM-Solver++ scheduler for faster inference
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )

        # Move to device
        self.pipe = self.pipe.to(self.device)

        # Enable memory optimizations
        if self.device == "cuda":
            self.pipe.enable_attention_slicing()
            # Try to enable xformers if available
            try:
                self.pipe.enable_xformers_memory_efficient_attention()
            except Exception:
                pass

            # Enable VAE slicing for SDXL to reduce memory usage
            if self.is_sdxl:
                try:
                    self.pipe.enable_vae_slicing()
                    self.pipe.enable_vae_tiling()
                except Exception:
                    pass

        print("Model loaded successfully")

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        width: int = 1024,
        height: int = 1024,
        seed: int = None,
        output_dir: Path = None,
        transparent_background: bool = False
    ) -> Path:
        """
        Generate a high-quality image from a text prompt

        Args:
            prompt: Text description of the desired image
            negative_prompt: Things to avoid in the image
            num_inference_steps: Number of denoising steps (recommended: 30-50)
            guidance_scale: Guidance scale for generation (recommended: 7.0-9.0 for SDXL)
            width: Image width (SDXL optimal: 1024, must be multiple of 8)
            height: Image height (SDXL optimal: 1024, must be multiple of 8)
            seed: Random seed for reproducibility
            output_dir: Directory to save the generated image
            transparent_background: Whether to remove background and make transparent

        Returns:
            Path to the generated image
        """
        # Load model if not already loaded
        self.load_model()

        # Enhance prompt for quality
        enhanced_prompt = self._enhance_prompt(prompt, transparent_background)

        # Enhance negative prompt for quality
        enhanced_negative = self._enhance_negative_prompt(negative_prompt)

        # Set seed for reproducibility
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)

        # Generate image
        print(f"Generating high-quality image with prompt: {prompt}")
        print(f"Enhanced prompt: {enhanced_prompt}")

        with torch.inference_mode():
            if self.is_sdxl:
                # SDXL generation
                result = self.pipe(
                    prompt=enhanced_prompt,
                    negative_prompt=enhanced_negative,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                    generator=generator,
                    output_type="pil" if not self.use_refiner else "latent",
                )

                # Apply refiner if available
                if self.refiner is not None:
                    print("Applying refiner for enhanced quality...")
                    result = self.refiner(
                        prompt=enhanced_prompt,
                        negative_prompt=enhanced_negative,
                        image=result.images,
                        num_inference_steps=20,
                        strength=0.3,
                        generator=generator,
                    )

                image = result.images[0]
            else:
                # Standard SD 1.5 generation
                result = self.pipe(
                    prompt=enhanced_prompt,
                    negative_prompt=enhanced_negative,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    width=width,
                    height=height,
                    generator=generator,
                )
                image = result.images[0]

        # Remove background if requested
        if transparent_background:
            print("Removing background for transparency...")
            image = self._remove_background(image)

        # Save image
        if output_dir is None:
            output_dir = Path("./output/images")

        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sdxl_image_{timestamp}.png" if self.is_sdxl else f"sd_image_{timestamp}.png"
        output_path = output_dir / filename

        image.save(output_path)
        print(f"High-quality image saved to: {output_path}")

        return output_path

    def _enhance_prompt(self, prompt: str, transparent_bg: bool = False) -> str:
        """Enhance prompt for better quality"""
        # Quality enhancers
        quality_terms = "masterpiece, best quality, highly detailed, professional, sharp focus, 8k uhd"

        # Background handling
        if transparent_bg:
            bg_terms = "clean white background, studio lighting, isolated object, product shot"
        else:
            bg_terms = "beautiful composition, professional lighting"

        # Combine
        enhanced = f"{prompt}, {quality_terms}, {bg_terms}"
        return enhanced

    def _enhance_negative_prompt(self, negative_prompt: str) -> str:
        """Enhance negative prompt to avoid quality issues"""
        # Common quality issues to avoid
        quality_issues = (
            "low quality, worst quality, low res, blurry, jpeg artifacts, "
            "ugly, distorted, deformed, disfigured, poorly drawn, "
            "bad anatomy, wrong anatomy, extra limbs, missing limbs, "
            "text, watermark, signature, username, "
            "cropped, out of frame, draft, unfinished"
        )

        if negative_prompt:
            return f"{negative_prompt}, {quality_issues}"
        return quality_issues

    def _remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background from image for transparency"""
        try:
            from rembg import remove
            print("Removing background using rembg...")
            output = remove(image)
            print("Background removed successfully")
            return output
        except ImportError:
            print("Warning: rembg not installed. Install with: pip install rembg")
            print("Returning original image without background removal")
            return image
        except Exception as e:
            print(f"Error removing background: {e}")
            return image

    def generate_batch(
        self,
        prompts: list,
        negative_prompt: str = "",
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512,
        output_dir: Path = None
    ) -> list:
        """
        Generate multiple images from a list of prompts

        Args:
            prompts: List of text descriptions
            negative_prompt: Things to avoid in all images
            num_inference_steps: Number of denoising steps
            guidance_scale: Guidance scale for generation
            width: Image width
            height: Image height
            output_dir: Directory to save generated images

        Returns:
            List of paths to generated images
        """
        image_paths = []

        for prompt in prompts:
            image_path = self.generate(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                output_dir=output_dir
            )
            image_paths.append(image_path)

        return image_paths

    def unload_model(self):
        """Unload model from memory"""
        if self.pipe is not None:
            del self.pipe
            self.pipe = None

        if self.refiner is not None:
            del self.refiner
            self.refiner = None

        # Clear CUDA cache if using GPU
        if self.device == "cuda":
            torch.cuda.empty_cache()

        print("Model unloaded from memory")
