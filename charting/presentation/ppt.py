import json
import ntpath

from pptx import Presentation
from os.path import dirname, abspath

import win32com.client as win32


class Ppt:

    def __init__(self, data: str, template: str = 'dr-template.pptm'):
        parent_dir = dirname(dirname(abspath(__file__)))
        self.prs = Presentation(pptx=f'{parent_dir}/templates/{template}')
        f = open(data, "rb")
        self.data = json.load(f)
        f.close()

        self.__add_title_slide()
        self.__add_chapter()
        self.__add_disclaimer()

    def __add_title_slide(self):
        slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(slide_layout)

        title_obj = slide.placeholders[0]
        title_frame = title_obj.text_frame
        title_frame.text = self.data.get('title')

        if self.data.get('subtitle') is not None:
            subtitle_obj = slide.placeholders[15]
            subtitle_frame = subtitle_obj.text_frame
            subtitle_frame.text = self.data.get('subtitle')

        if self.data.get('suptitle') is not None:
            suptitle_obj = slide.placeholders[14]
            suptitle_frame = suptitle_obj.text_frame
            suptitle_frame.text = self.data.get('suptitle')

    def __add_chapter(self):
        for chapter in self.data.get('chapter'):
            title = chapter.get('title')

            slide_layout = self.prs.slide_layouts[1]
            slide = self.prs.slides.add_slide(slide_layout)
            slide.placeholders[0].text = title

            note = slide.placeholders[14]
            sp = note.element
            sp.getparent().remove(sp)

            note = slide.placeholders[15]
            sp = note.element
            sp.getparent().remove(sp)

            for slide in chapter.get('slides'):
                slide_title = slide.get('title')
                chart = slide.get('chart')

                slide_layout = self.prs.slide_layouts[3]
                slide = self.prs.slides.add_slide(slide_layout)

                slide.placeholders[0].text = title
                slide.placeholders[13].text = slide_title
                slide.placeholders[19].insert_picture(chart)

    def __add_disclaimer(self):
        slide_layout = self.prs.slide_layouts[17]
        slide = self.prs.slides.add_slide(slide_layout)

        note = slide.placeholders[10]
        sp = note.element
        sp.getparent().remove(sp)

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


