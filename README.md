# ComfyUI Html2Image Nodes

提供网页截图、相机水印、自由模板转图片功能。

![Workflow示例](workflow/workflow.png)

## 功能

### 1. 网页截图 (Webpage Screenshot)
可以对任意网页进行截图，支持以下功能：
- 自定义截图尺寸
- 等待时间控制
- 完整页面截图
- CSS 选择器指定区域截图

参数说明：
- `url`: 要截图的网页地址，默认为 "https://example.com"
- `width`: 截图宽度，默认 1280，范围 64-4096
- `height`: 截图高度，默认 720，范围 64-4096
- `wait_time_seconds`: 等待页面加载的时间（秒），默认 0.5，最小 0.1
- `full_page`: 是否截取完整页面，默认 `false`。选中时会忽略 `height` 参数
- `css_selector`: CSS 选择器（可选），用于截取特定元素。例如：".content" 或 "#header"

### 2. 相机水印 (Camera Watermark)
生成类似手机相机的信息水印，支持以下功能：
- 自定义相机型号
- 自动生成时间戳
- 多品牌 Logo 支持
- 自定义拍摄参数
- 自定义 GPS 信息
- 可调整宽度

> 如需更改模板可更改根目录下的 `template/camera_watermark/template.html` 文件

参数说明：
- `model`: 相机型号，默认为 "COMFYUI X1 ULTRA"
- `date`: 拍摄日期时间，默认为当前时间，格式：YYYY.MM.DD HH:MM:SS
- `brand`: 品牌选择，基于 brand 目录下的 SVG 文件自动生成选项
- `device`: 拍摄参数，默认为 "23mm f/1.0 1/320 ISO1495"
- `gps`: GPS 信息，默认为 "51°30'00\"N 0°10'00\"E"
- `width`: 水印宽度，默认 1280，范围 64-2048

### 3. 自由网页模板转图片 (Template To Image)

此节点支持将HTML模板转换为图片，可用于生成各类图片内容。目前支持以下模板：

#### 3.1 节气图片模板 (jieqi)

一个优雅的节气展示模板，支持自定义文本和图片。

![节气 Workflow 示例](workflow/jieqi_workflow.png)

**功能特点**：
- 支持自定义背景图片
- 支持自定义主标题和副标题
- 内置优雅的排版和字体
- 自适应不同尺寸

**参数说明**：
- `image1`: 背景图片（可选，默认使用内置背景图）
- `text1`: 节气名称（默认值："冬至"）
- `text2`: 日期文本（默认值："12月21日"）
- `text3`: 祝福语（默认值："天时人事日相催，冬至阳生春又来。祝您冬至快乐。"）
- `text4`: 遮罩层透明度（默认值："0.3"）

#### 3.2 新年贺卡模板 (happy_new_year)

一个响应式的2025新年贺卡模板，支持动态背景和文本叠加效果。

![新年贺卡 Workflow 示例](workflow/happy_new_year_workflow.png)

**功能特点**：
- 支持自定义背景图片
- 支持二维码嵌入
- 中英双语支持
- 响应式设计，自动缩放
- 无背景图时显示装饰元素（建筑、云朵）
- 半透明文本遮罩层

**参数说明**：
- `image1`: 背景图片（可选）
- `image2`: 二维码图片（可选）
- `text1`: Logo文本（默认值："YOUR LOGO"）
- `text2`: 域名文本（默认值："plus.palxp.cn"）
- `text3`: 主问候语（默认值："Hello 2025"）
- `text4`: 中文问候语（默认值："你好，2025"）
- `text5`: 第一行底部文本（默认值："勇敢出发"）
- `text6`: 第二行底部文本（默认值："遇见更好的自己"）
- `text7`: 底部问候语（默认值："HAPPY NEW YEAR"）
- `text8`: 遮罩层透明度（默认值："0.3"，0无遮罩）

**通用参数**：
- `template_file`: 模板文件，可选值：["template/jieqi/template.html", "template/happy_new_year/template.html"]
- `width`: 输出图片宽度（默认：640，范围：64-2048）
- `height`: 输出图片高度（默认：1024，范围：64-2048）

## 安装

1. 将本项目克隆到 ComfyUI 的 `custom_nodes` 目录：
```bash
cd custom_nodes
git clone https://github.com/liuqianhonga/ComfyUI-Html2Image.git
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 重启 ComfyUI

## 使用示例

### 网页截图节点
1. 普通网页截图：
   - 设置 url 和所需的宽高
   - 调整 wait_time_seconds 确保页面加载完成

2. 完整页面截图：
   - 启用 full_page 选项
   - 设置所需的宽度（height 将被忽略）

3. 特定元素截图：
   - 在 css_selector 中输入目标元素的选择器
   - 例如：".article-content" 或 "#main-header"

### 相机水印节点
1. 基本使用：
   - 设置所需的宽度
   - 其他参数保持默认值

2. 自定义水印：
   - 修改 model 为所需的相机型号
   - 设置自定义的拍摄参数和 GPS 信息
   - 选择不同的品牌 Logo


## 常见问题

### 网页截图相关
1. 截图显示不完整
   - 增加 wait_time_seconds 的值
   - 检查网页是否需要登录或有其他加载条件
   - 确认网页是否有动态加载内容

2. CSS 选择器无法找到元素
   - 确认选择器语法正确
   - 检查元素是否是动态加载的
   - 可能需要增加等待时间

3. 完整页面截图出现问题
   - 检查页面是否有固定定位元素
   - 确认页面高度是否正确计算

### 相机水印相关
1. 品牌 Logo 不显示
   - 检查 brand 目录中是否有对应的 SVG 文件
   - 确保 SVG 文件格式正确
   - 检查文件权限

2. 时间戳格式问题
   - 可以自定义时间格式
   - 支持手动输入时间

3. 水印尺寸问题
   - 宽度会自动计算对应的高度
   - 保持了品牌 Logo 的原始比例
