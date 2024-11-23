from .webpage_screenshot_node import WebpageScreenshotNode
from .camera_watermark_node import CameraWatermarkNode

NODE_CLASS_MAPPINGS = {
    "WebpageScreenshot": WebpageScreenshotNode,
    "CameraWatermark": CameraWatermarkNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebpageScreenshot": "Webpage Screenshot",
    "CameraWatermark": "Camera Watermark"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 