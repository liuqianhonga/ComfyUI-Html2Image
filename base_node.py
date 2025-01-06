import os
import base64
from PIL import Image
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import numpy as np
import torch

class BaseNode:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "to_image"
    CATEGORY = "image"
    
    # Class level service to avoid repeated driver checks
    _service = None

    def __init__(self):
        if BaseNode._service is None:
            BaseNode._service = Service(ChromeDriverManager().install())
            
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

    def _capture_screenshot(self, url, width, height, wait_time_seconds=0.5, element_id=None, element_selector=None, full_page=False):
        driver = webdriver.Chrome(service=self._service, options=self.chrome_options)
        try:
            # 设置初始窗口大小
            driver.set_window_size(width, height or 1024)
            driver.get(url)
            
            # 等待页面加载完成
            WebDriverWait(driver, wait_time_seconds + 5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # 等待所有图片加载完成
            WebDriverWait(driver, wait_time_seconds + 5).until(
                lambda d: d.execute_script("""
                    return Array.from(document.images).every(img => img.complete);
                """)
            )

            # 额外等待时间
            time.sleep(wait_time_seconds)
            
            if full_page:
                # 获取页面完整高度
                total_height = driver.execute_script("return document.documentElement.scrollHeight")
                driver.set_window_size(width, total_height)
                time.sleep(1)  # 调整大小后额外等待
            
            if element_id:
                # 通过ID查找元素，并等待元素可见
                element = WebDriverWait(driver, wait_time_seconds + 5).until(
                    EC.visibility_of_element_located((By.ID, element_id))
                )
                screenshot = element.screenshot_as_png
            elif element_selector:
                # 通过CSS选择器查找元素，并等待元素可见
                try:
                    element = WebDriverWait(driver, wait_time_seconds + 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, element_selector))
                    )
                    screenshot = element.screenshot_as_png
                except:
                    raise ValueError(f"Element with selector '{element_selector}' not found")
            else:
                # 截取整个页面
                screenshot = driver.get_screenshot_as_png()
            
            image = Image.open(io.BytesIO(screenshot))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            image_array = np.array(image)
            image_array = image_array.astype(np.float32) / 255.0
            if len(image_array.shape) == 2:
                image_array = np.stack([image_array] * 3, axis=-1)
            
            tensor = torch.from_numpy(image_array)
            tensor = tensor.unsqueeze(0)
            
            return tensor
        
        finally:
            driver.quit()