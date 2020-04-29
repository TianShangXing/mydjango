# # 图像处理
import cv2

# # 读图
# img = cv2.imread('./code.png', cv2.IMREAD_GRAYSCALE)

# # 写图
# cv2.imwrite('./code1.png', img)

# 图片水印
# from PIL import Image, ImageDraw, ImageFont

# # 读图
# im = Image.open("./static/upload/人物男头01.jpg")

# print(im.format, im.size, im.mode)

# # 生成画笔
# draw = ImageDraw.Draw(im)

# # 绘制
# draw.text((0, 0), 'xing', fill=(76, 234, 124, 180))

# im.show()

# 图像压缩
# 读图
img = cv2.imread('./static/upload/人物男头01.jpg')

# 压缩png
# cv2.imwrite('./static/upload/人物男头02.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

# 压缩jpg
cv2.imwrite('./static/upload/人物男头02.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])

