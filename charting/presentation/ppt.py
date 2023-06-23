from pptx import Presentation
from os.path import dirname, abspath

from pptx.enum.text import MSO_AUTO_SIZE
from pptx.oxml import parse_xml
from pptx.util import Pt


class Ppt:

    def __init__(self, template: str = 'D&R Präsentation.pptx'):
        parent_dir = dirname(dirname(abspath(__file__)))
        self.prs = Presentation(pptx=f'{parent_dir}/templates/{template}')

    def add_title_slide(self, title: str, second_title: str, suptitle: str):
        slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(slide_layout)

        title_original = self.prs.slide_master.slide_layouts[0].placeholders[3]
        title_obj = slide.placeholders[0]
        original_text = title_original.text_frame.text
        self.set_text(title_obj, title, len(original_text))

        suptitle_original = self.prs.slide_master.slide_layouts[0].placeholders[4]
        suptitle_obj = slide.placeholders[14]
        original_text = suptitle_original.text_frame.text
        self.set_text(suptitle_obj, suptitle, len(original_text))

        second_title_obj = slide.placeholders[15]
        second_title_original = self.prs.slide_master.slide_layouts[0].placeholders[2]
        self.set_text(second_title_obj, second_title)
        original_text = second_title_original.text_frame.text
        self.set_text(suptitle_obj, suptitle, len(original_text))

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

    def set_text(self, shape, text, num_characters = 1):

        if shape.has_text_frame:

            original_left = shape.left
            original_top = shape.top
            original_height = shape.height
            original_width = (shape.width / num_characters) * 1.5

            shape.width = int(original_width * num_characters)
            shape.text = text

            shape.left = original_left
            shape.top = original_top
            shape.height = original_height

