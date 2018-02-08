# Created by Max on 2/8/18
from zheye import zheye

z = zheye()
positions = z.Recognize('captcha(10).gif')
print(positions)
