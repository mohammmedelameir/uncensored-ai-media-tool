import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import UncensoredMediaGenerator

class TestUncensoredMediaGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.generator = UncensoredMediaGenerator()
        
    def test_generate_image_returns_pil(self):
        img = self.generator.generate_image("test prompt", steps=1)
        from PIL import Image
        self.assertIsInstance(img, Image.Image)
        
    def test_generate_image_dimensions(self):
        img = self.generator.generate_image("test", steps=1)
        self.assertEqual(img.size, (512, 512))
        
    def test_generate_batch_count(self):
        prompts = ["a", "b", "c"]
        images = self.generator.generate_batch(prompts, steps=1)
        self.assertEqual(len(images), 3)
        
    def test_generate_batch_all_images(self):
        prompts = ["x", "y"]
        images = self.generator.generate_batch(prompts, steps=1)
        for img in images:
            self.assertIsNotNone(img)

if __name__ == "__main__":
    unittest.main()