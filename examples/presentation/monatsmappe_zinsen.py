from charting.presentation.ppt import Ppt


if __name__ == '__main__':
    ppt = Ppt(data="monatsmappe-juli.json")
    ppt.save('C:\\Users\\ssymhoven\\Projekte\\charting-lib\\examples\\presentation\\monatsmappe-zinsen-juli-2023.ppt')
