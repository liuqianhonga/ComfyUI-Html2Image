from .webpage_screenshot_node import WebpageScreenshotNode
from .camera_watermark_node import CameraWatermarkNode
from .template_to_image_node import TemplateToImageNode

NODE_CLASS_MAPPINGS = {
    "WebpageScreenshot": WebpageScreenshotNode,
    "CameraWatermark": CameraWatermarkNode,
    "TemplateToImage": TemplateToImageNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebpageScreenshot": "Webpage Screenshot",
    "CameraWatermark": "Camera Watermark",
    "TemplateToImage": "Template To Image"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 