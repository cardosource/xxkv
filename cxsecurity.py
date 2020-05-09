import sys
import re
import requests


def bannercxsecurity():
    cxsecurity= """
cxsecurity
    """
    return cxsecurity
def filtro(htmlespecifico):
    return re.compile(str(htmlespecifico))
lista_fonts=[]


def cxsecurity(paginas):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    pagina = "{}{}".format("https://cxsecurity.com/dorks/",paginas)
    url = requests.get(pagina,headers=user_agent)
    catalogo = filtro('<TD width="68%">(.*?)</TD>')
    info = filtro('<h5>(.*?)</h5>')
    dorkEh = filtro('Dork:</B>(.*?)</font>')
    for sqlI in catalogo.findall(url.text):
        for titulo in info.findall(sqlI):
            vul = str(titulo).lower()
            for dork in dorkEh.findall(str(sqlI).replace('&nbsp;', '')):
                todasDORKS = str(dork).replace("&quot;",'"')
                print(vul, " :==> ",todasDORKS)
                lista_fonts.append(todasDORKS)



if __name__ == '__main__':
    bannercxsecurity()
    try:
        pagina = sys.argv[1]
        cxsecurity(pagina)
    except:
        print(":/")
        bannercxsecurity()
