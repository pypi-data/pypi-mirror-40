import pandas as pd

def joke():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')

def pandas_joke(number):
	return pd.DataFrame({"a":["aa"]*number, "b":["bb"]*number})
