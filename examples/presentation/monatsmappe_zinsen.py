from charting.presentation.ppt import Ppt


if __name__ == '__main__':
    ppt = Ppt(title="Monatsmappe", subtitle="Ausgabe Zinsen", suptitle="Juni 2023")

    # Volatilitätsmärkte
    ppt.add_image_slide(title="Volatilitätsmärkte", subtitle="Eingepreise Volatilität aus Optionen", img="volatility/vix_v2x.png")
    ppt.add_image_slide(title="Volatilitätsmärkte", subtitle="Eingepreise Volatilität aus Optionen", img="volatility/vix_v2x.png")

    ppt.save('C:\\Users\\ssymhoven\\Projekte\\charting-lib\\examples\\presentation\\monatsmappe-zinsen-juli-2023.ppt')
