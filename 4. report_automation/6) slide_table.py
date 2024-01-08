# 표 슬라이드

title_only_slide_layout = prs.slide_layouts[5] 
slide = prs.slides.add_slide(title_only_slide_layout) # 슬라이드 추가
shapes = slide.shapes

title_shape = slide.placeholders[0]
title_shape.text = 'Adding a Table'

rows = cols = 2
left = Inches(2.0)
width = Inches(6.0)
height = Inches(0.8)

table = shapes.add_table(rows, cols, left, top, width, height).table

# set column widths
table.columns[0].width = Inches(2.0)
table.columns[1].width = Inches(4.0)

# write column widths
table.cell(0, 0).text = '안'
table.cell(0, 1).text = '녕'

# write body cells
table.cell(1, 0).text = '그'
table.cell(1, 1).text = '래'

# 저장 
prs.save('test.pptx')