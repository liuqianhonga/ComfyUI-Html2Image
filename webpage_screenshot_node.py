from .base_node import BaseNode

class WebpageScreenshotNode(BaseNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "https://example.com"}),
                "width": ("INT", {"default": 1280, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 720, "min": 64, "max": 4096}),
                "wait_time_seconds": ("FLOAT", {"default": 0.5, "min": 0.1}),
                "full_page": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "css_selector": ("STRING", {"default": ""}),
            }
        }

    def to_image(self, url, width=1280, height=720, wait_time_seconds=0.5, full_page=False, css_selector=None):
        capture_height = None if full_page else height
        element_selector = css_selector if css_selector and css_selector.strip() else None
        
        tensor = self._capture_screenshot(
            url, 
            width, 
            capture_height, 
            wait_time_seconds=wait_time_seconds,
            element_selector=element_selector,
            full_page=full_page
        )
        return (tensor,)