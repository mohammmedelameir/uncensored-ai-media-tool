import argparse
from src import UncensoredMediaGenerator, VideoPipeline

def main():
    parser = argparse.ArgumentParser(description="Uncensored AI Media Tool")
    parser.add_argument("--mode", choices=["image", "video"], required=True,
                        help="Generation mode")
    parser.add_argument("--prompt", type=str, help="Single prompt for image mode")
    parser.add_argument("--prompts", nargs="+", help="List of prompts for video mode")
    parser.add_argument("--output", type=str, default="output.png",
                        help="Output file path")
    parser.add_argument("--steps", type=int, default=30, help="Inference steps")
    
    args = parser.parse_args()
    gen = UncensoredMediaGenerator()
    
    if args.mode == "image":
        if not args.prompt:
            raise ValueError("--prompt required for image mode")
        img = gen.generate_image(args.prompt, steps=args.steps)
        img.save(args.output)
        print(f"Image saved to {args.output}")
    
    elif args.mode == "video":
        if not args.prompts or len(args.prompts) < 2:
            raise ValueError("--prompts requires at least 2 prompts for video mode")
        pipeline = VideoPipeline(gen)
        pipeline.generate_frames(args.prompts, steps=args.steps)
        pipeline.save_video(args.output)

if __name__ == "__main__":
    main()