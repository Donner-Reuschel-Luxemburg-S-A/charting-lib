from charting.presentation.ppt import Ppt


if __name__ == '__main__':
    ppt = Ppt()
    ppt.add_title_slide(title="Monatsmappe", second_title="Ausgabe Zinsen", suptitle="Juni 2023")
    ppt.save('C:\\Users\\ssymhoven\\Projekte\\charting-lib\\examples\\presentation\\output\\ppt-example.ppt')
