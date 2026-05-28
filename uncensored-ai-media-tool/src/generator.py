import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import numpy as np

class UncensoredMediaGenerator:
    """Uncensored image generator using stable diffusion with safety checker disabled."""
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        self.pipe.to(self.device)
        self.pipe.enable_attention_slicing()
        
    def generate_image(self, prompt: str, negative_prompt: str = "", 
                       steps: int = 30, guidance_scale: float = 7.5) -> Image.Image:
        """Generate an uncensored image from text prompt."""
        with torch.no_grad():
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=guidance_scale
            )
        return result.images[0]
    
    def generate_batch(self, prompts: list[str], **kwargs) -> list[Image.Image]:
        """Generate multiple images from a list of prompts."""
        return [self.generate_image(p, **kwargs) for p in prompts]