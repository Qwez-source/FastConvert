import click
import os
from PIL import Image
import cv2
import numpy as np

class Converter:
    @staticmethod
    def convert_image(input_path, output_path):
        """Convert image files between different formats"""
        try:
            with Image.open(input_path) as img:
                if output_path.lower().endswith(('.jpg', '.jpeg')) and img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(output_path)
            return True
        except Exception as e:
            print(f"Error converting image: {e}")
            return False

    @staticmethod
    def convert_video(input_path, output_path):
        """Convert video files between different formats or extract frame"""
        try:
            print(f"Opening video file: {input_path}")
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                raise Exception("Could not open video file")

            # If output is an image format, extract frame
            if os.path.splitext(output_path)[1].lower() in image_formats:
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Could not read frame from video")
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Save as image using PIL
                img = Image.fromarray(frame_rgb)
                if output_path.lower().endswith(('.jpg', '.jpeg')):
                    img = img.convert('RGB')
                img.save(output_path)
            else:
                # Normal video conversion
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # Create VideoWriter with appropriate codec
                ext = os.path.splitext(output_path)[1].lower()
                if ext == '.mp4':
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                elif ext == '.avi':
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                elif ext == '.amv':
                    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                    fps = 25.0 if fps == 0 else fps
                    width = 160 if width == 0 else width
                    height = 120 if height == 0 else height
                else:
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    if ext == '.amv' and (frame.shape[1] != width or frame.shape[0] != height):
                        frame = cv2.resize(frame, (width, height))
                    out.write(frame)
                
                out.release()
            
            cap.release()
            return True
            
        except Exception as e:
            print(f"Error converting video: {e}")
            return False

# Supported formats
image_formats = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff', '.tif', 
                '.ico', '.ppm', '.pgm', '.pbm', '.jp2', '.eps']
video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv', '.mpeg', 
                '.mpg', '.3gp', '.m4v', '.amv']

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def convert(input_path, output_path):
    """
    Convert files between different formats.
    See FORMATS.md for complete list of supported formats and conversions.
    """
    input_ext = os.path.splitext(input_path)[1].lower()
    output_ext = os.path.splitext(output_path)[1].lower()
    
    try:
        # Handle regular conversions
        if input_ext in image_formats and output_ext in image_formats:
            success = Converter.convert_image(input_path, output_path)
        elif input_ext in video_formats and (output_ext in video_formats or output_ext in image_formats):
            success = Converter.convert_video(input_path, output_path)
        else:
            click.echo(f"Unsupported conversion: {input_ext} to {output_ext}")
            return
        
        if success:
            click.echo(f"Successfully converted {input_path} to {output_path}")
        else:
            click.echo("Conversion failed")
            
    except Exception as e:
        click.echo(f"Error during conversion: {e}")

if __name__ == '__main__':
    convert()
