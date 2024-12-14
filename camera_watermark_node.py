import os
import base64
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from .base_node import BaseNode

class CameraWatermarkNode(BaseNode):
    @classmethod
    def read_brand_files(cls):
        brand_data_uris = {}
        brand_options = []
        brand_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "brand")
        
        if os.path.exists(brand_dir):
            for file in os.listdir(brand_dir):
                if file.endswith(('.svg', '.png', '.jpg', '.jpeg')):
                    brand_name = os.path.splitext(file)[0]
                    brand_options.append(brand_name)
                    brand_file_path = os.path.join(brand_dir, file)
                    with open(brand_file_path, 'rb') as f:
                        brand_file_content = f.read()
                        brand_file_base64 = base64.b64encode(brand_file_content).decode('utf-8')
                        if file.endswith('.svg'):
                            brand_data_uris[brand_name] = f"data:image/svg+xml;base64,{brand_file_base64}"
                        elif file.endswith('.png'):
                            brand_data_uris[brand_name] = f"data:image/png;base64,{brand_file_base64}"
                        elif file.endswith(('.jpg', '.jpeg')):
                            brand_data_uris[brand_name] = f"data:image/jpeg;base64,{brand_file_base64}"
        
        if not brand_options:
            brand_options = ["liuqianhong"]
            
        return brand_options, brand_data_uris

    def __init__(self):
        super().__init__()
        template_dir = os.path.dirname(os.path.realpath(__file__))
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        _, self.brand_data_uris = self.read_brand_files()

    @classmethod
    def INPUT_TYPES(cls):
        current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        brand_options, _ = cls.read_brand_files()

        return {
            "required": {
                "model": ("STRING", {"default": "COMFYUI ULTRA"}),
                "date": ("STRING", {"default": current_time}),
                "brand": (brand_options, {"default": "liuqianhong"}),
                "device": ("STRING", {"default": "23mm f/1.0 1/320 ISO1495"}),
                "gps": ("STRING", {"default": "51°30'00\"N 0°10'00\"E"}),
                "width": ("INT", {"default": 1280, "min": 64, "max": 2048}),
            }
        }

    def to_image(self, model="COMFYUI ULTRA", date=None, brand="liuqianhong",
                device="23mm f/1.0 1/320 ISO1495", gps="51°30'00\"N 0°10'00\"E",
                width=1280):
        if date is None:
            date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            
        template_data = {
            'model': model,
            'model_arr': model.split(" ", 1),
            'date': date,
            'brand': brand,
            'device': device,
            'gps': gps,
            'width': width,
            'height': 1024,
            'brand_uri': self.brand_data_uris.get(brand, '')
        }
        
        template = self.jinja_env.get_template('templates/camera_watermark/template.html')
        rendered_html = template.render(**template_data)
        
        html_base64 = base64.b64encode(rendered_html.encode('utf-8')).decode('utf-8')
        data_url = f"data:text/html;base64,{html_base64}"
        
        tensor = self._capture_screenshot(data_url, width, 512, element_id="preview-info")
        return (tensor,)