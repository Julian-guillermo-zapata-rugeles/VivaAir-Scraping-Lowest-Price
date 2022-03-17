import sys
sys.path.insert(0, '..')

from .colosus import Colossus
from settings.constants import Constants as CONST
import time


class VivaAir(Colossus):
    def __init__(self):
        super(VivaAir, self).__init__()
        self.local_time = time.localtime()[:5]
        self._url = CONST.DEFAULT_URL
        
        
    def set_days(self):
        self._url = f"https://reservas.vivaair.com/#/co/es/booking/resultados?DepartureCity={CONST.FROM}&ArrivalCity={CONST.TOWARDS}&DepartureDate=2022-{self.local_time[1]}-{self.local_time[2]}&ReturnDate=2022-{self.local_time[1]}-{self.local_time[2]}&Adults=1&Currency=COP"
    

    def get_day(self,string):
        n = ["1","2","3","4","5","6","7","8","9","0"]
        salida = ""
        add = False
        for i in string:
            if i not in n and add == False:
                salida=salida+" ; "
                add = True
            salida=salida+i

        return salida
    
    
    def obtener_precios_bajos_dia(self):
        self.set_days()
        self._get()
        results = self.soup.findAll('div',{'class':"lowest-fare__week-day"})
        data = self._procesar_respuestas(results)
        try:
            analiticas = open(CONST.PATH_DATA_COMPLETE,"a")
            analiticas2 = open(CONST.PATH_DATA_RECENT,"w")
            analiticas3 = open(CONST.PATH_DATA_SHORT,"w")
            
            for resultados in data:
                r = resultados.split(" ")
                r[1]=self.get_day(r[1])
                tiempo = ";".join(str(x) for x in time.localtime()[:4])
                salida = f"{tiempo};{r[0]};{r[1]};{r[2]};{CONST.FROM};{CONST.TOWARDS}\n"
                short  = f"{r[0]};{r[1]};{r[2]};{CONST.FROM};{CONST.TOWARDS}\n"
                analiticas.write(salida)
                analiticas2.write(salida)
                analiticas3.write(short)
                #print(f"{r[0]:<20}  {r[1]:<20}  {r[2]:<20} {tiempo:<20} {self.desde:<20}  {self.hacia}")
        except Exception as e:
            print(e)
            pass
        finally:
            analiticas.close()
            analiticas2.close()
            analiticas3.close()


    def obtener_todos_precios_dia(self):
        results = self.soup.findAll('app-flight',{'class':"flight"})
        selected = self.soup.findAll('div',{'class':"swiper-slide swiper-slide-active"})
        output = []
        for i in results:
            try:
                aeropuerto_s = i.find("h2",{"class":"departure__airport"}).text
                salida       = i.find("h2",{"class":"departure__time"}) .text
                aeropuerto_l = i.find("h2",{"class":"arrival__airport"}).text
                llegada      = i.find("h2",{"class":"arrival__time"}).text
                valor        = i.find("span",{"class":"lowest-fare__price"}).text
                dia          = selected[0].find("span",{"class":"lowest-fare__date"}).text
                mes          = selected[0].find("span",{"class":"lowest-fare__month"}).text
                

                print(f"{dia:<10} {mes:<20} {aeropuerto_s:<20} {salida:<10} {aeropuerto_l:<20} {llegada:<20} {valor}")
                linea = f"{dia};{mes};{aeropuerto_s};{salida};{aeropuerto_l};{llegada};{valor}"
                output.append(linea)
            except Exception as e:
                print(e)
                pass
            
            
    def close(self):
        self._driver.close()
