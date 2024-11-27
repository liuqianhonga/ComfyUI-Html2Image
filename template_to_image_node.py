from .base_node import BaseNode
import os
import tempfile
from PIL import Image
import numpy as np
from jinja2 import Environment, FileSystemLoader

class TemplateToImageNode(BaseNode):
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "to_image"
    CATEGORY = "image"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template_file": ("STRING", {"default": "templates/jieqi/template.html"}),
                "width": ("INT", {"default": 1242, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 2208, "min": 64, "max": 4096}),
                "wait_time_seconds": ("FLOAT", {"default": 0.5, "min": 0.1}),
            },
            "optional": {
                "text1": ("STRING", {"default": ""}),
                "text2": ("STRING", {"default": ""}),
                "text3": ("STRING", {"default": ""}),
                "text4": ("STRING", {"default": ""}),
                "text5": ("STRING", {"default": ""}),
                "text6": ("STRING", {"default": ""}),
                "text7": ("STRING", {"default": ""}),
                "image1": ("IMAGE", {"default": None}),
                "image2": ("IMAGE", {"default": None}),
                "image3": ("IMAGE", {"default": None}),
            }
        }

    def __init__(self):
        super().__init__()
        # 设置Jinja2环境
        template_dir = os.path.dirname(os.path.realpath(__file__))
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def to_image(self, template_file, width=1280, height=720, wait_time_seconds=0.5,
                 text1="", text2="", text3="", text4="", text5="",
                 text6="", text7="", image1=None, image2=None, image3=None):
    
        template_data = {}
        # 只添加非空的参数
        for i, text in enumerate([text1, text2, text3, text4, text5, text6, text7], 1):
            if text.strip():
                template_data[f'text{i}'] = text

        # 获取模板文件的绝对路径
        if not os.path.isabs(template_file):
            template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), template_file)

        # 获取模板文件所在的目录
        template_dir = os.path.dirname(template_file)

        # 处理图片参数
        image_files = []
        for i, image in enumerate([image1, image2, image3], 1):
            if image is not None:
                # 保存图片到临时文件
                image_filename = f"image{i}.png"
                image_path = os.path.join(template_dir, image_filename)
                
                input_image = image.cpu().numpy()
                
                if len(input_image.shape) == 4:
                    input_image = input_image[0]
                
                if input_image.shape[-1] != 3:
                    input_image = np.transpose(input_image, (1, 2, 0))
                
                img = Image.fromarray((input_image * 255).astype('uint8')).convert('RGB')                
                img.save(image_path)

                template_data[f'image{i}'] = f"./{image_filename}"
                image_files.append(image_path)

        # 读取模板文件内容
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 创建临时模板
        template = self.jinja_env.from_string(template_content)
        
        # 渲染模板
        rendered_html = template.render(**template_data)
        
        # 在模板文件所在的目录中创建临时文件
        with tempfile.NamedTemporaryFile(dir=template_dir, delete=False, suffix='.html', mode='w', encoding='utf-8') as temp_file:
            temp_file.write(rendered_html)
            temp_file_path = temp_file.name

        # 截图
        tensor = self._capture_screenshot(
            temp_file_path, 
            width, 
            height, 
            wait_time_seconds
        )
        
        # 删除临时文件
        os.remove(temp_file_path)
        for image_path in image_files:
            os.remove(image_path)
        
        return (tensor, width, height)