import bs4
def get_grade_info(HTML:str)->str:
    librus = bs4.BeautifulSoup(HTML,"html.parser")
    lista = librus.select(".ocena")
    oceny = [int(x.get_text()) for x in lista if "title" in x.attrs if "Kategoria: śródroczna" in x["title"]]
    if len(oceny) == 0:
        raise ValueError("Nie podano odpowiedniej strony HTML, albo nie ma ocen śródrocznych")
    return "Liczba ocen wynosi: %s, a twoja średnia na półrocze wynosi: %s"%(len(oceny),round(sum(oceny)/len(oceny),2))