from PIL import Image, ImageDraw
import math

# 创建画布
width, height = 1080, 1440
img = Image.new('RGB', (width, height), '#e8f5e9')
draw = ImageDraw.Draw(img)

# 创建渐变背景
for y in range(height):
    ratio = y / height
    r = int(232 - ratio * 45)
    g = int(245 - ratio * 65)
    b = int(233 - ratio * 62)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

center_x, center_y = 540, 750

# 耳朵
draw.ellipse([center_x - 180, center_y - 240, center_x - 60, center_y - 120], fill='#1a1a1a')
draw.ellipse([center_x + 60, center_y - 240, center_x + 180, center_y - 120], fill='#1a1a1a')

# 身体
draw.ellipse([center_x - 180, center_y + 50, center_x + 180, center_y + 450], fill='#ffffff')

# 头
draw.ellipse([center_x - 160, center_y - 230, center_x + 160, center_y + 90], fill='#ffffff')

# 黑眼圈
draw.ellipse([center_x - 110, center_y - 110, center_x - 10, center_y - 10], fill='#1a1a1a')
draw.ellipse([center_x + 10, center_y - 110, center_x + 110, center_y - 10], fill='#1a1a1a')

# 眼睛（白色）
draw.ellipse([center_x - 90, center_y - 90, center_x - 50, center_y - 50], fill='#ffffff')
draw.ellipse([center_x + 50, center_y - 90, center_x + 90, center_y - 50], fill='#ffffff')

# 眼珠
draw.ellipse([center_x - 82, center_y - 82, center_x - 58, center_y - 58], fill='#1a1a1a')
draw.ellipse([center_x + 58, center_y - 82, center_x + 82, center_y - 58], fill='#1a1a1a')

# 眼睛高光
draw.ellipse([center_x - 75, center_y - 88, center_x - 65, center_y - 78], fill='#ffffff')
draw.ellipse([center_x + 65, center_y - 88, center_x + 75, center_y - 78], fill='#ffffff')

# 鼻子
draw.ellipse([center_x - 30, center_y + 10, center_x + 30, center_y + 50], fill='#1a1a1a')

# 腮红
draw.ellipse([center_x - 170, center_y - 20, center_x - 90, center_y + 40], fill=(255, 182, 193))
draw.ellipse([center_x + 90, center_y - 20, center_x + 170, center_y + 40], fill=(255, 182, 193))

# 四肢
draw.ellipse([center_x - 250, center_y + 150, center_x - 150, center_y + 350], fill='#1a1a1a')
draw.ellipse([center_x + 150, center_y + 150, center_x + 250, center_y + 350], fill='#1a1a1a')
draw.ellipse([center_x - 140, center_y + 400, center_x - 20, center_y + 480], fill='#1a1a1a')
draw.ellipse([center_x + 20, center_y + 400, center_x + 140, center_y + 480], fill='#1a1a1a')

# 竹子装饰
def draw_bamboo(x, y, size=1.0):
    # 竹竿
    draw.rectangle([x, y, x + 15*size, y + 80*size], fill='#8d6e63')
    # 竹叶
    draw.polygon([(x - 5*size, y), (x + 7*size, y - 30*size), (x + 20*size, y)], fill='#66bb6a')
    draw.polygon([(x + 10*size, y - 5*size), (x + 30*size, y - 25*size), (x + 20*size, y + 5*size)], fill='#4caf50')

for i in range(6):
    draw_bamboo(80 + i * 180, 1250, 1.2)

# 保存图片
output_path = r'C:\Users\Administrator\.openclaw\workspace\panda_post.png'
img.save(output_path, 'PNG')
print(f'Image saved to: {output_path}')
