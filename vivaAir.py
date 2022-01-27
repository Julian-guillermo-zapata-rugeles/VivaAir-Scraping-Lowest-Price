from colosus import Colossus
import time

class VivaAir(Colossus):
    def __init__(self,desde,hacia):
        super(VivaAir, self).__init__()
        self.desde=desde;
        self.hacia=hacia;
        self.local_time = time.localtime()[:5]
        self._url = "https://reservas.vivaair.com/#/co/es/booking/resultados?DepartureCity=SMR&ArrivalCity=MDE&DepartureDate=2022-02-01&ReturnDate=2022-02-28&Adults=1&Currency=COP"




    def set_days(self):
        print("--------------------------------------------")
        mes_s = int(input("Mes de salida   : "))
        dia_s = int(input("Dia de salida   : "))
        print("--------------------------------------------")
        mes_r = int(input("Mes de regreso  : "))
        mes_r = int(input("Dia de regreso  : "))
        self._url = f"https://reservas.vivaair.com/#/co/es/booking/resultados?DepartureCity={self.desde}&ArrivalCity={self.hacia}&DepartureDate=2022-{self.local_time[1]}-{self.local_time[2]}&ReturnDate=2022-{self.local_time[1]}-{self.local_time[2]}&Adults=1&Currency=COP"
    



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
        self._get()
        results = self.soup.findAll('div',{'class':"lowest-fare__week-day"})
        data = self._procesar_respuestas(results)
        try:
            analiticas = open("AnaliticasVivaAir.csv","a")
            analiticas2 = open("AnaliticasVivaAir_latest.csv","a")
            for resultados in data:
                r = resultados.split(" ")
                r[1]=self.get_day(r[1])
                tiempo = ";".join(str(x) for x in time.localtime()[:4])
                salida = f"{tiempo:<10} ; {r[0]:<20} ; {r[1]:<20} ; {r[2]:<10} ; {self.desde:<20} ; {self.hacia}  \n"
                analiticas.write(salida)
                analiticas2.write(salida)
                print(f"{r[0]:<20}  {r[1]:<20}  {r[2]:<20} {tiempo:<20} {self.desde:<20}  {self.hacia}")
        except Exception as e:
            print(e)
            pass
        finally:
            analiticas.close()
            analiticas2.close()



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
                linea = f"{dia};{mes};{aeropuerto_s};{salida};{aeropuerto_l:<20} {llegada:<20} {valor}"
            except Exception as e:
                print(e)
                pass
            


    def close(self):
        self._driver.close()



reset = open("AnaliticasVivaAir_latest.csv","w")
reset.close() 


viva = VivaAir("SMR","MDE")
viva.obtener_precios_bajos_dia()
viva.close()



viva2 = VivaAir("MDE","SMR")
viva2.obtener_precios_bajos_dia()
viva2.close()
