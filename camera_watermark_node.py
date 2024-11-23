import os
import base64
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from .base_node import BaseNode

class CameraWatermarkNode(BaseNode):
    @classmethod
    def read_svg_files(cls):
        svg_data_uris = {}
        brand_options = []
        brand_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "brand")
        
        if os.path.exists(brand_dir):
            for file in os.listdir(brand_dir):
                if file.endswith('.svg'):
                    brand_name = os.path.splitext(file)[0]
                    brand_options.append(brand_name)
                    svg_path = os.path.join(brand_dir, file)
                    with open(svg_path, 'rb') as f:
                        svg_content = f.read()
                        svg_base64 = base64.b64encode(svg_content).decode('utf-8')
                        svg_data_uris[brand_name] = f"data:image/svg+xml;base64,{svg_base64}"
        
        if not brand_options:
            brand_options = ["leica"]
            
        return brand_options, svg_data_uris

    def __init__(self):
        super().__init__()
        template_dir = os.path.dirname(os.path.realpath(__file__))
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        _, self.svg_data_uris = self.read_svg_files()

    @classmethod
    def INPUT_TYPES(cls):
        brand_options, _ = cls.read_svg_files()
        current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        return {
            "required": {
                "model": ("STRING", {"default": "COMFYUI X1 ULTRA"}),
                "date": ("STRING", {"default": current_time}),
                "brand": (brand_options, {"default": brand_options[0]}),
                "device": ("STRING", {"default": "23mm f/1.0 1/320 ISO1495"}),
                "gps": ("STRING", {"default": "51°30'00\"N 0°10'00\"E"}),
                "width": ("INT", {"default": 1280, "min": 64, "max": 2048}),
            }
        }

    def to_image(self, model="COMFYUI X1 ULTRA", date=None, brand="leica",
                device="23mm f/1.0 1/320 ISO1495", gps="51°30'00\"N 0°10'00\"E",
                width=1280):
        if date is None:
            date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            
        template_data = {
            'model': model,
            'date': date,
            'brand': brand,
            'device': device,
            'gps': gps,
            'width': width,
            'height': 512,
            'svg_uri': self.svg_data_uris.get(brand, '')
        }
        
        template = self.jinja_env.get_template('camera_watermark_template.html')
        rendered_html = template.render(**template_data)
        
        html_base64 = base64.b64encode(rendered_html.encode('utf-8')).decode('utf-8')
        data_url = f"data:text/html;base64,{html_base64}"
        
        tensor = self._capture_screenshot(data_url, width, 512, element_id="preview-info")
        return (tensor,)