import ntpath

from pptx import Presentation
from os.path import dirname, abspath

import win32com.client as win32


class Ppt:

    def __init__(self, template: str = 'D&R Präsentation.pptm'):
        parent_dir = dirname(dirname(abspath(__file__)))
        self.prs = Presentation(pptx=f'{parent_dir}/templates/{template}')

    def add_title_slide(self, title: str, second_title: str, suptitle: str):
        slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(slide_layout)

        title_obj = slide.placeholders[0]
        title_frame = title_obj.text_frame
        title_frame.text = title

        suptitle_obj = slide.placeholders[14]
        suptitle_frame = suptitle_obj.text_frame
        suptitle_frame.text = suptitle

        second_title_obj = slide.placeholders[15]
        second_title_frame = second_title_obj.text_frame
        second_title_frame.text = second_title

    def add_image_slide(self, title: str, subtitle: str, comment: str = None):
        slide_layout = self.prs.slide_layouts[3]
        slide = self.prs.slides.add_slide(slide_layout)

        slide.placeholders[0].text = title
        slide.placeholders[13].text = subtitle

        if comment is not None:
            slide.placeholders[14].text = comment

    def get_layout(self):
        for slide in self.prs.slide_layouts:
            for shape in slide.placeholders:
                print('%d %d %s' % (self.prs.slide_layouts.index(slide), shape.placeholder_format.idx, shape.name))

    def save(self, path: str):
        self.prs.save(path)
        filename = ntpath.basename(path)

        powerpoint = win32.gencache.EnsureDispatch('PowerPoint.Application')
        powerpoint.Visible = True
        presentation = powerpoint.Presentations.Open(path)
        presentation.Application.Run(f"{filename}!Modul1.AdjustShapeWidthToFitText")

        presentation.Save()
        presentation.Close()

        powerpoint.Quit()

