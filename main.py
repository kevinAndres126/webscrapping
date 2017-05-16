from bs4 import BeautifulSoup
import requests
import json

lista = []
listaCarros = []

class Car:
    def __init__(self, CarMarca,Ano,Precio,Cilindrada,Estilo,Combustible,Transmision,Kilometraje,Placa,Color,NumPuertas,PrecioNegociable,Recibe,FechaIngreso):
        self.Marca = CarMarca
        self.Ano = Ano
        self.Precio = Precio
        self.Cilindrada = Cilindrada
        self.Estilo = Estilo
        self.Combustible = Combustible
        self.Transmision = Transmision
        self.Kilometraje = Kilometraje
        self.Placa = Placa
        self.Color = Color
        self.NumPuertas = NumPuertas
        self.Negociable = PrecioNegociable
        self.Recibe = Recibe
        self.FechaIngreso = FechaIngreso
        self.listalinkimg = []




def scraHref():
    page = requests.get("http://crautos.com/rautosusados/")
    status_code = page.status_code


    if status_code == 200:
        html = BeautifulSoup(page.text, "html.parser")
        for link in html.find_all('a',{'inventory mainhlcar'}):
            lista.append("http://crautos.com/rautosusados/"+link.get('href'))

        for link in html.find_all('a',{'inventory dealerhlcar'}):
           lista.append("http://crautos.com/rautosusados/"+link.get('href'))

    else:
        print "Status Code %d" % status_code

def scrapearPage():
    for i in lista:
        page = requests.get(i)
        status_code1 = page.status_code
        if status_code1 == 200:
            html = BeautifulSoup(page.text, "html.parser")
            Modelotemp = str(html.find_all('h2').__getitem__(0))
            precio = str(html.find_all('h2').__getitem__(1))
            Modelo = ""
            Ano = ""

            for x in Modelotemp[4:]:
                if x == '<':
                    break
                Modelo += x
            cont1=0
            cont2=0
            for y in Modelotemp:
                if y == '<':
                    cont1 +=1
                elif y == '>':
                    cont2 +=1
                elif cont2 == 2 and cont1 == 2:
                    Ano += y
                elif cont1 == 3:
                    break

            data = []
            table = html.find('table', attrs={'class': 'technical table-striped'})
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

            newcar = Car(Modelo,Ano,precio[4:-5],data[0][1],data[1][1],data[2][1],data[3][1],data[5][1],data[6][1],data[7][1],data[9][1],data[11][1],data[12][1],data[14][1])

            links = html.find_all('img', src=True)
            for link in links:
                link = link["src"].split("src=")[-1]
                if link[0] == '/' and link[1]== 'c':
                    if newcar.listalinkimg.__contains__(link) == False :
                        newcar.listalinkimg.append("http://crautos.com"+link)
            listaCarros.append(newcar)

        else:
            print "Status Code %d" % status_code1

def postDB():
    for x in listaCarros:
        from firebase import firebase
        data = {'Marca': x.Marca, 'Precio': x.Precio,'Ano': x.Ano,'Cilindrada': x.Cilindrada,'Estilo':x.Estilo,'Combustible':x.Combustible,'Transmision':x.Transmision,'Kilometraje':x.Kilometraje,
                'Placa':x.Placa,'Color':x.Color,'NumPeurtas':x.NumPuertas,'Negociable':x.Negociable,'Recibe':x.Recibe,'FechaIngreso':x.FechaIngreso}
        newCar = json.dumps(data)
        firebase = firebase.FirebaseApplication('https://webscrapping-c2c62.firebaseio.com', None)
        result = firebase.post('/Cars',newCar)




def requestFirebase():
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://webscrapping-c2c62.firebaseio.com', None)
    result = firebase.get('/Cars',None)
    print("BAse de DAtos")
    print result





#scraHref()
#scrapearPage()
#postDB()
#requestFirebase()
