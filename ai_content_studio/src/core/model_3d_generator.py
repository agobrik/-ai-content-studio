"""
3D Model Generator - Advanced Text-to-3D and Image-to-3D with TripoSR
Supports multiple methods:
1. TripoSR (Best quality - real 3D reconstruction)
2. MiDaS Depth Estimation (Good quality - depth-based)
3. Simple Extrusion (Fallback - basic relief)
"""

import torch
import numpy as np
from PIL import Image
from pathlib import Path
import datetime
import trimesh
from typing import Optional, Union, Literal
import warnings


class Model3DGenerator:
    """Generate 3D models from text or images using multiple methods"""

    def __init__(self, cache_dir: Path = None):
        """
        Initialize the 3D model generator

        Args:
            cache_dir: Directory to cache models
        """
        self.cache_dir = cache_dir
        self.device = self._get_device()
        self.image_generator = None
        self.triposr_model = None
        self.midas_model = None
        self.midas_transform = None

        # Try to determine available methods
        self.available_methods = self._detect_available_methods()

        print(f"3D Generator initialized on device: {self.device}")
        print(f"Available methods: {', '.join(self.available_methods)}")

    def _get_device(self):
        """Get the appropriate device (CUDA/CPU)"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def _detect_available_methods(self) -> list:
        """Detect which 3D generation methods are available"""
        methods = ["extrusion"]  # Always available

        # Check for MiDaS (timm is required)
        try:
            import timm
            methods.insert(0, "midas")
        except ImportError:
            pass

        # TripoSR is complex to setup, will be loaded on-demand
        # It's listed as available but will fallback if loading fails
        if "midas" in methods:
            methods.insert(0, "triposr")

        return methods

    def _get_image_generator(self):
        """Lazy load image generator for text-to-3D"""
        if self.image_generator is None:
            from .image_generator import ImageGenerator
            self.image_generator = ImageGenerator(
                cache_dir=self.cache_dir
            )
        return self.image_generator

    def load_model(self, method: str = "auto"):
        """
        Load the 3D generation model

        Args:
            method: Which method to use (auto/triposr/midas/extrusion)
        """
        if method == "auto":
            method = self.available_methods[0]

        print(f"Loading 3D model with method: {method}")

        if method == "triposr":
            self._load_triposr()
        elif method == "midas":
            self._load_midas()
        elif method == "extrusion":
            print("Using simple extrusion method (no model loading required)")
        else:
            raise ValueError(f"Unknown method: {method}")

    def _load_triposr(self):
        """Load TripoSR model for high-quality 3D reconstruction"""
        if self.triposr_model is not None:
            return

        try:
            print("Loading TripoSR model from HuggingFace...")
            print("Note: TripoSR requires significant download (~1GB)")
            print("First time setup may take several minutes...")

            # Try to import TripoSR directly
            try:
                from tsr.system import TSR
                from tsr.utils import remove_background, resize_foreground

                print("Loading TripoSR with official implementation...")

                # Load model
                self.triposr_model = TSR.from_pretrained(
                    "stabilityai/TripoSR",
                    config_name="config.yaml",
                    weight_name="model.ckpt",
                )

                # Move to device
                self.triposr_model.renderer.set_chunk_size(8192)
                self.triposr_model.to(self.device)

                print("SUCCESS: TripoSR model loaded successfully (official implementation)")

            except ImportError:
                # Fallback: Try alternative import
                print("Official TripoSR not found, trying alternative method...")
                import torch.hub

                # Load via torch hub or direct HuggingFace
                self.triposr_model = torch.hub.load(
                    "stabilityai/TripoSR",
                    "TripoSR",
                    trust_repo=True,
                    verbose=True
                )

                if self.triposr_model is not None:
                    self.triposr_model.to(self.device)
                    print("SUCCESS: TripoSR loaded via torch.hub")
                else:
                    raise RuntimeError("Failed to load TripoSR")

        except Exception as e:
            print(f"ERROR: Failed to load TripoSR: {e}")
            print("=" * 60)
            print("TripoSR INSTALLATION INSTRUCTIONS:")
            print("1. Install TripoSR:")
            print("   pip install git+https://github.com/VAST-AI-Research/TripoSR.git")
            print("2. Or install dependencies:")
            print("   pip install trimesh rembg pillow torch torchvision")
            print("=" * 60)
            print("Falling back to MiDaS (depth-based 3D) instead...")
            self.triposr_model = None
            # Remove triposr from available methods
            if "triposr" in self.available_methods:
                self.available_methods.remove("triposr")

    def _load_midas(self):
        """Load MiDaS model for depth-based 3D generation"""
        if self.midas_model is not None:
            return

        try:
            print("Loading MiDaS depth estimation model...")
            print("This will download ~400MB on first use...")

            # Load MiDaS from torch hub
            self.midas_model = torch.hub.load(
                "intel-isl/MiDaS",
                "DPT_Large",
                trust_repo=True,
                verbose=True
            )
            self.midas_model.to(self.device)
            self.midas_model.eval()

            # Load transforms
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
            self.midas_transform = midas_transforms.dpt_transform

            print("SUCCESS: MiDaS model loaded successfully")

        except Exception as e:
            print(f"ERROR: Failed to load MiDaS: {e}")
            import traceback
            traceback.print_exc()
            print("Falling back to simple extrusion")
            self.midas_model = None
            if "midas" in self.available_methods:
                self.available_methods.remove("midas")

    def generate_from_text(
        self,
        prompt: str,
        negative_prompt: str = "blurry, low quality, distorted",
        output_format: str = "glb",
        output_dir: Path = None,
        method: str = "auto",
        extrusion_depth: float = 0.5,
        progress_callback=None
    ) -> Path:
        """
        Generate a 3D model directly from text prompt

        This is a two-step process:
        1. Generate 2D image from text (using Stable Diffusion)
        2. Convert to 3D using selected method

        Args:
            prompt: Text description of the 3D model
            negative_prompt: What to avoid in the image
            output_format: Output format (glb, obj, stl, ply)
            output_dir: Directory to save the generated model
            method: Which 3D method to use (auto/triposr/midas/extrusion)
            extrusion_depth: Depth for extrusion-based methods (0.1 to 2.0)
            progress_callback: Optional callback for progress updates

        Returns:
            Path to the generated 3D model
        """
        if progress_callback:
            progress_callback(0, "Generating 2D image from text...")

        # Step 1: Generate 2D image
        print(f"Step 1/2: Generating 2D image from prompt: {prompt}")
        image_gen = self._get_image_generator()
        image_gen.load_model()

        # Generate image optimized for 3D conversion
        temp_output_dir = Path("./output/temp_3d")
        temp_output_dir.mkdir(parents=True, exist_ok=True)

        # Optimize prompt for 3D conversion - very specific for single object
        optimized_prompt = (
            f"{prompt}, single object, centered on white background, "
            f"product photography, studio lighting, professional photo, "
            f"isometric view, clear subject, clean composition, "
            f"masterpiece, best quality, highly detailed, 8k uhd"
        )

        image_path = image_gen.generate(
            prompt=optimized_prompt,
            negative_prompt=(
                f"{negative_prompt}, multiple objects, cluttered background, "
                f"blurry, low quality, distorted, text, watermark, "
                f"people, hands, faces, complex scene, partial object, "
                f"cropped, cut off, incomplete"
            ),
            num_inference_steps=40,  # Optimal for SDXL
            guidance_scale=7.5,  # Optimal for SDXL
            width=1024,  # SDXL optimal resolution
            height=1024,  # SDXL optimal resolution
            output_dir=temp_output_dir,
            transparent_background=True  # Always remove background for 3D
        )

        if progress_callback:
            progress_callback(50, "Converting 2D image to 3D model...")

        # Step 2: Convert to 3D
        print(f"Step 2/2: Converting image to 3D model...")
        result = self.generate_from_image(
            image_path=image_path,
            output_format=output_format,
            output_dir=output_dir,
            method=method,
            extrusion_depth=extrusion_depth,
            remove_background=True  # Always remove background for text-to-3D
        )

        if progress_callback:
            progress_callback(100, "3D model generated!")

        return result

    def generate_from_image(
        self,
        image_path: Union[str, Path],
        output_format: str = "glb",
        output_dir: Path = None,
        method: str = "auto",
        extrusion_depth: float = 0.5,
        remove_background: bool = False
    ) -> Path:
        """
        Generate a 3D model from a 2D image

        Args:
            image_path: Path to input image
            output_format: Output format (glb, obj, stl, ply)
            output_dir: Directory to save the generated model
            method: Which 3D method to use (auto/triposr/midas/extrusion)
            extrusion_depth: Depth for extrusion-based methods (0.1 to 2.0)
            remove_background: Whether to remove background before conversion

        Returns:
            Path to the generated 3D model
        """
        print(f"Generating 3D model from image: {image_path}")

        # Load image
        image = Image.open(image_path).convert("RGB")

        # Optional: Remove background for better 3D conversion
        if remove_background:
            image = self._remove_background(image)

        # Determine method
        if method == "auto":
            method = self.available_methods[0]

        print(f"Using method: {method}")

        # Generate 3D mesh based on method
        if method == "triposr":
            if self.triposr_model is None:
                self._load_triposr()
            if self.triposr_model is not None:
                mesh = self._generate_with_triposr(image)
            else:
                print("TripoSR not available, falling back to MiDaS")
                method = "midas"

        if method == "midas":
            if self.midas_model is None:
                self._load_midas()
            if self.midas_model is not None:
                mesh = self._generate_with_midas(image, extrusion_depth)
            else:
                print("MiDaS not available, falling back to simple extrusion")
                method = "extrusion"

        if method == "extrusion" or 'mesh' not in locals():
            # Fallback to simple extrusion
            print("Using simple extrusion method")
            image_rgba = image.convert("RGBA")
            mesh = self._create_mesh_from_image_simple(image_rgba, extrusion_depth)

        # Setup output path
        if output_dir is None:
            output_dir = Path("./output/models_3d")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"model_3d_{timestamp}.{output_format}"
        output_path = output_dir / filename

        # Export mesh
        self._export_mesh(mesh, output_path, output_format)

        print(f"SUCCESS: 3D model saved to: {output_path}")
        return output_path

    def _remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background from image"""
        try:
            from rembg import remove
            print("Removing background...")
            image_rgba = remove(image)
            print("SUCCESS: Background removed")
            return image_rgba
        except Exception as e:
            print(f"Could not remove background: {e}")
            return image

    def _generate_with_triposr(self, image: Image.Image) -> trimesh.Trimesh:
        """
        Generate 3D mesh using TripoSR (best quality - proper volumetric 3D)

        TripoSR is a state-of-the-art image-to-3D model that generates
        full 3D geometry, not flat extrusion. This produces REAL 3D models.
        """
        print("Generating PROPER 3D mesh with TripoSR (not flat extrusion)...")

        if self.triposr_model is None:
            self._load_triposr()

        if self.triposr_model is None:
            raise RuntimeError("TripoSR model not available")

        # Prepare image - TripoSR works best with clean backgrounds
        if image.mode != "RGBA":
            # Convert to RGBA
            rgba = Image.new("RGBA", image.size, (255, 255, 255, 255))
            rgba.paste(image, (0, 0))
            image = rgba

        # Resize to 512x512 (TripoSR optimal size)
        image = image.resize((512, 512), Image.Resampling.LANCZOS)

        try:
            # Try official TripoSR API
            from tsr.utils import remove_background, resize_foreground

            # Preprocess image
            image = remove_background(image, rembg_session=None)
            image = resize_foreground(image, 0.85)

            # Run TripoSR
            with torch.no_grad():
                scene_codes = self.triposr_model([image], device=self.device)

            # Extract mesh with marching cubes
            mesh_out = self.triposr_model.extract_mesh(scene_codes, resolution=256)[0]

            # mesh_out is a dict with 'vertices' and 'faces'
            vertices = mesh_out['vertices'].cpu().numpy()
            faces = mesh_out['faces'].cpu().numpy()

            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

            print(f"SUCCESS: TripoSR generated REAL 3D model: {len(vertices)} vertices, {len(faces)} faces")
            print("This is a proper volumetric 3D model, not a flat extrusion!")

        except Exception as e:
            print(f"Official TripoSR API failed: {e}")
            print("Trying alternative method...")

            # Fallback: Direct tensor processing
            image_array = np.array(image)
            if image_array.shape[2] == 4:
                image_array = image_array[:, :, :3]  # Remove alpha

            # Convert to tensor
            image_tensor = torch.from_numpy(image_array).permute(2, 0, 1).float() / 255.0
            image_tensor = image_tensor.unsqueeze(0).to(self.device)

            # Generate with model
            with torch.no_grad():
                # Call model directly
                outputs = self.triposr_model(image_tensor)

                # Extract geometry
                if hasattr(outputs, 'vertices') and hasattr(outputs, 'faces'):
                    vertices = outputs.vertices[0].cpu().numpy()
                    faces = outputs.faces[0].cpu().numpy()
                else:
                    raise RuntimeError("Could not extract mesh from TripoSR output")

            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

            print(f"SUCCESS: TripoSR generated mesh: {len(vertices)} vertices, {len(faces)} faces")

        # Post-process mesh
        mesh.vertices -= mesh.vertices.mean(axis=0)  # Center
        scale = 1.0 / (np.max(np.abs(mesh.vertices)) + 1e-8)
        mesh.vertices *= scale * 0.5  # Scale and normalize

        # Clean up
        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        mesh.fix_normals()

        return mesh

    def _generate_with_midas(self, image: Image.Image, extrusion_depth: float = 0.5) -> trimesh.Trimesh:
        """
        Generate 3D mesh using MiDaS depth estimation (good quality)

        MiDaS estimates depth from the image and creates a depth-based mesh
        """
        print("Generating 3D mesh with MiDaS depth estimation...")

        if self.midas_model is None:
            self._load_midas()

        if self.midas_model is None:
            raise RuntimeError("MiDaS model not available")

        # Prepare image
        img_array = np.array(image)

        # Apply transform
        input_batch = self.midas_transform(img_array).to(self.device)

        # Predict depth
        with torch.no_grad():
            prediction = self.midas_model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img_array.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = prediction.cpu().numpy()

        # Normalize depth map
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
        depth_map = depth_map * extrusion_depth

        # Create mesh from depth map
        mesh = self._create_mesh_from_depth(img_array, depth_map)

        print(f"SUCCESS: MiDaS mesh generated: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")

        return mesh

    def _create_mesh_from_depth(
        self,
        image_array: np.ndarray,
        depth_map: np.ndarray
    ) -> trimesh.Trimesh:
        """
        Create a high-quality 3D mesh from image and depth map

        Creates a SOLID 3D object with:
        - Front face with depth
        - Back face (flat)
        - Side walls connecting them
        """
        height, width = depth_map.shape

        # Higher resolution for better quality
        max_size = 512
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            new_height = int(height * scale)
            new_width = int(width * scale)

            depth_map = np.array(Image.fromarray(depth_map).resize((new_width, new_height), Image.Resampling.LANCZOS))
            image_array = np.array(Image.fromarray(image_array).resize((new_width, new_height), Image.Resampling.LANCZOS))
            height, width = new_height, new_width

        # Apply Gaussian smoothing
        from scipy.ndimage import gaussian_filter
        depth_map = gaussian_filter(depth_map, sigma=1.5)

        # Amplify depth for better 3D effect
        depth_map = depth_map * 2.0

        all_vertices = []
        all_faces = []
        all_colors = []

        # FRONT SURFACE (with depth)
        front_vertex_offset = len(all_vertices)
        for y in range(height):
            for x in range(width):
                nx = (x / (width - 1)) * 2 - 1
                ny = -((y / (height - 1)) * 2 - 1)
                nz = depth_map[y, x]
                all_vertices.append([nx, ny, nz])
                all_colors.append(image_array[y, x][:3])

        # Front faces
        for y in range(height - 1):
            for x in range(width - 1):
                v1 = front_vertex_offset + y * width + x
                v2 = front_vertex_offset + y * width + (x + 1)
                v3 = front_vertex_offset + (y + 1) * width + (x + 1)
                v4 = front_vertex_offset + (y + 1) * width + x
                all_faces.append([v1, v2, v3])
                all_faces.append([v1, v3, v4])

        # BACK SURFACE (flat, at z=0)
        back_vertex_offset = len(all_vertices)
        for y in range(height):
            for x in range(width):
                nx = (x / (width - 1)) * 2 - 1
                ny = -((y / (height - 1)) * 2 - 1)
                nz = 0.0  # Flat back
                all_vertices.append([nx, ny, nz])
                all_colors.append(image_array[y, x][:3] * 0.6)  # Darker

        # Back faces (reversed winding)
        for y in range(height - 1):
            for x in range(width - 1):
                v1 = back_vertex_offset + y * width + x
                v2 = back_vertex_offset + y * width + (x + 1)
                v3 = back_vertex_offset + (y + 1) * width + (x + 1)
                v4 = back_vertex_offset + (y + 1) * width + x
                all_faces.append([v1, v3, v2])  # Reversed
                all_faces.append([v1, v4, v3])  # Reversed

        # SIDE WALLS (connecting front and back)
        # Left edge
        for y in range(height - 1):
            x = 0
            vf1 = front_vertex_offset + y * width + x
            vf2 = front_vertex_offset + (y + 1) * width + x
            vb1 = back_vertex_offset + y * width + x
            vb2 = back_vertex_offset + (y + 1) * width + x
            all_faces.append([vf1, vb1, vb2])
            all_faces.append([vf1, vb2, vf2])

        # Right edge
        for y in range(height - 1):
            x = width - 1
            vf1 = front_vertex_offset + y * width + x
            vf2 = front_vertex_offset + (y + 1) * width + x
            vb1 = back_vertex_offset + y * width + x
            vb2 = back_vertex_offset + (y + 1) * width + x
            all_faces.append([vf1, vf2, vb2])
            all_faces.append([vf1, vb2, vb1])

        # Top edge
        for x in range(width - 1):
            y = 0
            vf1 = front_vertex_offset + y * width + x
            vf2 = front_vertex_offset + y * width + (x + 1)
            vb1 = back_vertex_offset + y * width + x
            vb2 = back_vertex_offset + y * width + (x + 1)
            all_faces.append([vf1, vf2, vb2])
            all_faces.append([vf1, vb2, vb1])

        # Bottom edge
        for x in range(width - 1):
            y = height - 1
            vf1 = front_vertex_offset + y * width + x
            vf2 = front_vertex_offset + y * width + (x + 1)
            vb1 = back_vertex_offset + y * width + x
            vb2 = back_vertex_offset + y * width + (x + 1)
            all_faces.append([vf1, vb2, vf2])
            all_faces.append([vf1, vb1, vb2])

        vertices = np.array(all_vertices, dtype=np.float32)
        faces = np.array(all_faces, dtype=np.int32)
        colors = np.array(all_colors, dtype=np.uint8)

        # Create trimesh
        mesh = trimesh.Trimesh(
            vertices=vertices,
            faces=faces,
            vertex_colors=colors
        )

        # Clean up
        mesh.remove_degenerate_faces()
        mesh.remove_duplicate_faces()
        mesh.remove_infinite_values()
        mesh.fix_normals()

        print(f"Created SOLID 3D mesh: {len(vertices)} vertices, {len(faces)} faces")
        print(f"  Front surface: {height}x{width} grid")
        print(f"  Back surface: {height}x{width} grid")
        print(f"  Side walls: 4 edges closed")

        return mesh

    def _create_mesh_from_image_simple(
        self,
        image: Image.Image,
        extrusion_depth: float = 0.5
    ) -> trimesh.Trimesh:
        """
        Create a 3D mesh from an image using simple luminosity-based extrusion

        This is the fallback method when advanced models are not available.
        Creates a relief/embossed 3D model.
        """
        print("Creating 3D mesh using simple extrusion...")

        # Resize for manageable vertex count
        max_size = 256
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        width, height = image.size

        # Convert to numpy arrays
        img_array = np.array(image)

        # Extract RGB and alpha channels
        if img_array.shape[2] == 4:
            rgb = img_array[:, :, :3]
            alpha = img_array[:, :, 3] / 255.0
        else:
            rgb = img_array
            alpha = np.ones((height, width))

        # Calculate depth map from luminosity
        luminosity = np.mean(rgb, axis=2) / 255.0
        depth_map = luminosity * alpha * extrusion_depth

        # Create vertices
        vertices = []
        faces = []
        colors = []
        vertex_map = {}

        # Create front face vertices (with depth)
        for y in range(height):
            for x in range(width):
                if alpha[y, x] > 0.1:  # Only create vertices for visible pixels
                    # Normalize coordinates to -1 to 1
                    nx = (x / width) * 2 - 1
                    ny = (y / height) * 2 - 1
                    nz = depth_map[y, x]

                    vertex_idx = len(vertices)
                    vertices.append([nx, -ny, nz])  # Flip Y for correct orientation
                    colors.append(rgb[y, x])
                    vertex_map[(x, y, 'front')] = vertex_idx

        # Create back face vertices (flat)
        for y in range(height):
            for x in range(width):
                if alpha[y, x] > 0.1:
                    nx = (x / width) * 2 - 1
                    ny = (y / height) * 2 - 1

                    vertex_idx = len(vertices)
                    vertices.append([nx, -ny, 0])  # Back at z=0
                    colors.append(rgb[y, x] * 0.7)  # Slightly darker back
                    vertex_map[(x, y, 'back')] = vertex_idx

        # Create faces for front surface
        for y in range(height - 1):
            for x in range(width - 1):
                corners = [
                    (x, y, 'front'), (x+1, y, 'front'),
                    (x+1, y+1, 'front'), (x, y+1, 'front')
                ]

                if all(c in vertex_map for c in corners):
                    v1, v2, v3, v4 = [vertex_map[c] for c in corners]
                    faces.append([v1, v2, v3])
                    faces.append([v1, v3, v4])

        # Create faces for back surface (reversed winding)
        for y in range(height - 1):
            for x in range(width - 1):
                corners = [
                    (x, y, 'back'), (x+1, y, 'back'),
                    (x+1, y+1, 'back'), (x, y+1, 'back')
                ]

                if all(c in vertex_map for c in corners):
                    v1, v2, v3, v4 = [vertex_map[c] for c in corners]
                    faces.append([v1, v3, v2])
                    faces.append([v1, v4, v3])

        # Create side faces
        self._create_side_faces(vertex_map, faces, width, height)

        # Convert to numpy arrays
        vertices = np.array(vertices, dtype=np.float32)
        faces = np.array(faces, dtype=np.int32)
        colors = np.array(colors, dtype=np.uint8)

        print(f"Created mesh with {len(vertices)} vertices and {len(faces)} faces")

        # Create trimesh object
        mesh = trimesh.Trimesh(
            vertices=vertices,
            faces=faces,
            vertex_colors=colors
        )

        # Clean up mesh
        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        mesh.remove_infinite_values()
        mesh.fix_normals()

        return mesh

    def _create_side_faces(self, vertex_map, faces, width, height):
        """Create side faces connecting front and back"""
        # Left edge
        for y in range(height - 1):
            x = 0
            if (x, y, 'front') in vertex_map and (x, y+1, 'front') in vertex_map:
                vf1 = vertex_map[(x, y, 'front')]
                vf2 = vertex_map[(x, y+1, 'front')]
                vb1 = vertex_map[(x, y, 'back')]
                vb2 = vertex_map[(x, y+1, 'back')]
                faces.append([vf1, vb1, vb2])
                faces.append([vf1, vb2, vf2])

        # Right edge
        for y in range(height - 1):
            x = width - 1
            if (x, y, 'front') in vertex_map and (x, y+1, 'front') in vertex_map:
                vf1 = vertex_map[(x, y, 'front')]
                vf2 = vertex_map[(x, y+1, 'front')]
                vb1 = vertex_map[(x, y, 'back')]
                vb2 = vertex_map[(x, y+1, 'back')]
                faces.append([vf1, vf2, vb2])
                faces.append([vf1, vb2, vb1])

        # Top edge
        for x in range(width - 1):
            y = 0
            if (x, y, 'front') in vertex_map and (x+1, y, 'front') in vertex_map:
                vf1 = vertex_map[(x, y, 'front')]
                vf2 = vertex_map[(x+1, y, 'front')]
                vb1 = vertex_map[(x, y, 'back')]
                vb2 = vertex_map[(x+1, y, 'back')]
                faces.append([vf1, vf2, vb2])
                faces.append([vf1, vb2, vb1])

        # Bottom edge
        for x in range(width - 1):
            y = height - 1
            if (x, y, 'front') in vertex_map and (x+1, y, 'front') in vertex_map:
                vf1 = vertex_map[(x, y, 'front')]
                vf2 = vertex_map[(x+1, y, 'front')]
                vb1 = vertex_map[(x, y, 'back')]
                vb2 = vertex_map[(x+1, y, 'back')]
                faces.append([vf1, vb2, vf2])
                faces.append([vf1, vb1, vb2])

    def _export_mesh(
        self,
        mesh: trimesh.Trimesh,
        output_path: Path,
        format: str
    ):
        """Export mesh to file with proper validation"""
        format = format.lower()

        export_formats = {
            "glb": "glb",
            "obj": "obj",
            "stl": "stl",
            "ply": "ply"
        }

        if format not in export_formats:
            raise ValueError(f"Unsupported format: {format}. Supported: {list(export_formats.keys())}")

        # Validate and fix mesh before export
        try:
            mesh.fill_holes()
            mesh.fix_normals()
        except Exception as e:
            print(f"Warning: Could not fix mesh issues: {e}")

        # Export
        mesh.export(str(output_path), file_type=export_formats[format])

        # Report statistics
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        print(f"Exported {format.upper()}: {output_path.name}")
        print(f"  Vertices: {len(mesh.vertices)}")
        print(f"  Faces: {len(mesh.faces)}")
        print(f"  File size: {file_size:.2f} MB")
        print(f"  Is watertight: {mesh.is_watertight}")

    def unload_model(self):
        """Unload models from memory"""
        if self.image_generator is not None:
            self.image_generator.unload_model()
            self.image_generator = None

        if self.triposr_model is not None:
            del self.triposr_model
            self.triposr_model = None

        if self.midas_model is not None:
            del self.midas_model
            self.midas_model = None
            self.midas_transform = None

        # Clear CUDA cache if using GPU
        if self.device == "cuda":
            torch.cuda.empty_cache()

        print("3D generator models unloaded from memory")
