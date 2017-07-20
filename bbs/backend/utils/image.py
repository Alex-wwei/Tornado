from PIL import Image,ImageDraw, ImageFont, ImageFilter
import random

class VerifyCode():

    def __init__(self):
        self._letter_cases = 'abcdefghjkmnpqrstuvwxy'
        self._upper_cases = self._letter_cases.upper()
        # self._numbers = ''.join(map(str, range(3, 10)))

    def generate_vertification_code(self, number):
        '''
        生成num位的验,此处使用列表的序列化方式生成验证码的列表，之后通过random模块读取
        '''
        list_sample = [str(num) for num in range(2, 10)] + [chr(num) for num in range(65, 91)] + [chr(num) for num in
                                                                                                  range(97, 123)]
        vertification_code = "".join(random.sample(list_sample, number))
        return vertification_code

    def createCodeImage(self,size=(85,30),img_type='jpg',
                        mode='RGB',bg_color=(255,255,215),fg_color=(0,0,255),
                            font_size=18,font_type='arial.ttf',
                            length=4,draw_lines=True,n_line=(1,2),
                            draw_points=True,point_chance=2):
        width,height = size
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)

        def get_chars():
            return random.sample(self._letter_cases,length)

        def creat_line():
            line_num = random.randint(*n_line)#sign that the param is a list

            for i in range(line_num):
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            chance = min(100, max(0, int(point_chance)))
            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            c_chars = self.generate_vertification_code(length)
            strs = ' %s ' % ' '.join(c_chars)
            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)
            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                        strs, font=font, fill=fg_color)
            return ''.join(c_chars)


        if draw_lines:
            creat_line()
        if draw_points:
            create_points()
        strs = create_strs()

        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 220,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return img, strs
#
if __name__ == '__main__':
    vc = VerifyCode()
    code_img,capacha_code= vc.createCodeImage()
    print(capacha_code)
    code_img.save('../../models/1.jpg','JPEG')
