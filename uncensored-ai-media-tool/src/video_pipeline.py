import cv2
import numpy as np
from PIL import Image
from .generator import UncensoredMediaGenerator

class VideoPipeline:
    """Generate video frames from prompts and assemble into video."""
    
    def __init__(self, generator: UncensoredMediaGenerator, fps: int = 4):
        self.generator = generator
        self.fps = fps
        self.frames = []
        
    def generate_frames(self, prompts: list[str], interpolation_steps: int = 2, **kwargs):
        """Generate frames for each prompt with interpolation between them."""
        base_images = self.generator.generate_batch(prompts, **kwargs)
        
        self.frames = []
        for i in range(len(base_images) - 1):
            img_a = np.array(base_images[i])
            img_b = np.array(base_images[i + 1])
            self.frames.append(img_a)
            
            for step in range(1, interpolation_steps):
                alpha = step / interpolation_steps
                blended = cv2.addWeighted(img_a, 1 - alpha, img_b, alpha, 0)
                self.frames.append(blended)
        
        if base_images:
            self.frames.append(np.array(base_images[-1]))
    
    def save_video(self, output_path: str, codec: str = "mp4v"):
        """Save generated frames as a video file."""
        if not self.frames:
            raise ValueError("No frames to save. Run generate_frames first.")
        
        height, width = self.frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (width, height))
        
        for frame in self.frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        
        out.release()
        print(f"Video saved to {output_path} ({len(self.frames)} frames)")