# 사진 슬라이드

img_path = 'C:/Users/moonw/py_life/test_1.png'

two_layout = prs.slide_layouts[6] # 6 : 제목/내용이 없는 '빈'슬라이드
slide = prs.slides.add_slide(two_layout) # 슬라이드 추가

left = top = Inches(1)
width = height = Inches(1)
# width, heigh가 없을 경우 원본사이즈로
pic = slide.shapes.add_picture(img_path, left, top, width=width, height=height)

left = Inches(3)
width = Inches(5.5)
height = Inches(4)
pic = slide.shapes.add_picture(img_path, left, top, width=width, height=height)

# 저장 
prs.save('test.pptx')