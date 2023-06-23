from charting.presentation.ppt import Ppt


if __name__ == '__main__':
    ppt = Ppt()
    ppt.add_title_slide(title="Monatsmappe", second_title="Ausgabe Zinsen", suptitle="Juni 2023")
    ppt.add_image_slide(title="Arbeitsmarkt", subtitle="USA")
    ppt.save('output/ppt-example.pptx')
