from abc import ABCMeta, abstractmethod
from requests import get
import requests
import re
from concurrent.futures.process import ProcessPoolExecutor as processar
import multiprocessing
class Interface(metaclass=ABCMeta):

    @abstractmethod
    def conteudo(self):
        pass

class Gestor(Interface):

    def __init__(self):
        self.url = None
        self.pagina = None
    
    def __get_resposta(self):
        self.consulta = self.url

        return self.consulta
    
    def __status(self):
        folha=self.__get_resposta().url 
      
        print( f'[ Status ] : Resposta servidor {self.__get_resposta().status_code} Okay' )
        if folha[27:-1] != 'block':
            print(f'[ Folha ] endereço : folha {folha}')
        else:
            print(f'[ Block ] endereço : folha "BLOCKEADO {folha}')
            


        return True
 
    def set_url(self, url, pagina):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.url = get(url+str(pagina),headers=headers)
    
    def filtro(self, html):
        return re.compile(str(html))
        
      
    def conteudo(self):
        if self.__status():
            texto = self.__get_resposta().text
            catalogo = self.filtro('<TD width="68%">(.*?)</TD>')
            info = self.filtro('<h5>(.*?)</h5>')
            dorkEh = self.filtro('Dork:</B>(.*?)</font>')
            for sqlI in catalogo.findall(texto):
                for titulo in info.findall(sqlI):
                    vul = str(titulo).lower()
                    for dork in dorkEh.findall(str(sqlI).replace('&nbsp;', '')):
                        todasDORKS = str(dork).replace("&quot;",'"')
                        print(todasDORKS)

            
            print(f'Pesquisa concluida')
            return True
        else:
            print('Não não')
            return False


class Agente(Interface):

    def __init__(self):
        self.Gestor = Gestor()
        self.tamanho_pool  = multiprocessing.cpu_count() * 4
    
    def conteudo(self,pagina):
        url = "https://cxsecurity.com/dorks/"
        pool = multiprocessing.Pool(processes=self.tamanho_pool, initializer=self.Gestor.set_url(url,str(pagina)))
        pool.close()
        pool.join()
        return self.Gestor.conteudo()


# Cliente
class Cliente():

    def __init__(self):
        print('1 - Iniciando Solicitação...')
        self.iniciar = Agente()
        self.consulta = None
    
    def conteudo(self):
        try:
            for i in range(1,50+1):
                self.consulta = self.iniciar.conteudo(str(i))
        except requests.exceptions.ConnectionError:
            pass
    
    def __del__(self):
        if self.consulta:
            print('2 - Sucesso!!!')
        else:
             print('1 - Não foi possivel iniciar conexao, verifique o proxy')

if __name__ == '__main__':
    cliente = Cliente()
    
    with processar() as chamada:
        chamada.submit(cliente.conteudo()).done
