import requests
import json
import datetime

s = 1236472051807 / 1000.0
d = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
print(d)

numdays = 30
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_lst = []
for d in date_list:
    date_lst.append(str(d.strftime("%d/%m/%Y")))
print(date_lst)

# test = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/228/458/2015-01-26T00:00:00')
# test = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/5043/458/2020-04-18T00:00:00')
# print(test.json())

# name = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/BOLO')
# print(name.text)

# https://www.lefrecce.it/msite/api/solutions?origin=MILANO%20CENTRALE&destination=ROMA%20TERMINI&arflag=A&adate=28/04/2020&atime=17&adultno=1&childno=0&direction=A&frecce=false&onlyRegional=false

modena = requests.get('https://www.lefrecce.it/msite/api/geolocations/locations?name=mode')
print(modena.json())
modena_txt = modena.text
print(modena_txt)
# modena_text = json.dumps(modena)
modena_dct = json.loads(modena_txt)
for dct in modena_dct:
    if dct.get("name") == "MODENA":
        print(dct.get("id"))
        modena_id = dct.get("id")
#
# bologna = requests.get('https://www.lefrecce.it/msite/api/geolocations/locations?name=bolo')
# bologna_txt = bologna.text
# bologna_dct = json.loads(bologna_txt)
# print(bologna.json())
# for dct in bologna_dct:
#     if dct.get("name") == "BOLOGNA CENTRALE":
#         print(dct.get("id"))
#         bologna_id = dct.get("id")


# [STAZIONEPARTENZA] = BOLOGNA CENTRALE: Il nome della stazione di partenza, come restituito dall'autocompletamento stazione (vedi sotto)
# [STAZIONEARRIVO]: Il nome della stazione di arrivo
# [AR]: Può valere 'A' oppure 'R', la prima se si stanno cerando viaggi di sola andata, la seconda per viaggi a/r
# [DATA]: Data in formato dd/mm/yyyy
# [ORA]: L'ora di partenza in formato hh
# [OFFSET]: Se specificato, ritorna le soluzioni a partire dalla n-esima trovata fino alla n+5-esima. Essenziale per espandere la finestra di ricerca oltre le prime 5 soluzioni ritornate di default, che potrebbero non coprire tutte quelle esistenti nell'ora selezionata
# [ADULTI]/[BAMBINI]: Rispettivamente il numero di adulti o bambini per cui cercare il viaggio
# [DIRECTION]: Può valere solo 'A' se [AR] è 'A', altrimenti vale 'A' oppure 'R' a seconda se si stanno cercando le soluzioni di andata o di ritorno in un viaggio a/r
# [FRECCE]/[REGIONALI]: Booleani, 'true' per cercare solo soluzioni con alta velocità / treni regionali, 'false' altrimenti. Settarli entrambe a true non ha effetto. (Sì, ci ho provato :P)
# [DATARITORNO]/[ORARITORNO]: Questi campi sono omessi se [AR] è 'A', altrimenti sono il duale di [DATA] e [ORA] per il viaggio di ritorno
# [CODICE_CARTAFRECCIA]: Campo opzionale. Se fornito verranno mostrati i prezzi al netto di eventuali promozioni attive per quella specifica cartafreccia. Il codice deve essere valido. Se il parametro viene specificato, va aggiunto in coda all'url '&positions=0', altrimenti restituisce un errore

# https://www.lefrecce.it/msite/api/solutions?origin=%5BSTAZIONEPARTENZA%5D&destination=%5BSTAZIONEARRIVO%5D&arflag=%5BAR%5D&adate=%5BDATA%5D&atime=%5BORA%5D&offset=%5BOFFSET%5D&adultno=%5BADULTI%5D&childno=%5BBAMBINI%5D&direction=%5BDIREZIONE%5D&frecce=%5BFRECCE%5D&onlyRegional=%5BREGIONALI%5D&rdate=%5BDATARITORNO%5D&rtime=%5BORARITORNO%5D&codeList=%5BCODICE_CARTAFRECCIA%5D
#
# url = "https://www.lefrecce.it/msite/api/solutions?origin=%5" + station_start + "%5D&destination=%5" + station_end + "%5D&arflag=%5B" + AR_flag + "%5D&adate=%5BDATA%5D&atime=%5BORA%5D&offset=%5BOFFSET%5D&adultno=%5BADULTI%5D&childno=%5BBAMBINI%5D&direction=%5BDIREZIONE%5D&frecce=%5BFRECCE%5D&onlyRegional=%5BREGIONALI%5D&rdate=%5BDATARITORNO%5D&rtime=%5BORARITORNO%5D&codeList=%5BCODICE_CARTAFRECCIA%5D"
# url(partenza = Bologna, arrivo = modena)

def train_solution_url(station_start, station_end, ar_flag="A",date="01/01/2020",time="0",offset="0",n_adults="1",n_children="0",direction="A",is_frecce="true",is_regional="false",date_r="0",time_r=str(int("0")+2),freccia_card="0"):
    url = "https://www.lefrecce.it/msite/api/solutions?origin="+ station_start + \
          "&destination=" + station_end + \
          "&arflag=" + ar_flag + \
          "&adate=" + date+ \
          "&atime=" + time + \
          "&offset=" + offset + \
          "&adultno=" + n_adults + \
          "&childno=" + n_children + \
          "&direction=" + direction + \
          "&frecce=" + is_frecce + \
          "&onlyRegional=" + is_regional
    if ar_flag == "R":
        date_r = date
        url.append("&rdate=" + date_r + "&rtime=" + time_r)
    if freccia_card != "0":
        url.append("&codeList=" + freccia_card)
    # print(url)
    return url

url = []
url_dct = []
price = []
for d in date_lst:
    # response = requests.get(train_solution_url("BOLOGNA%20CENTRALE", "ROMA%20TERMINI", date=d, time="10")
    # url.append(response)
    # # url.append(response)
    # print(response.json())

    # requests.get(train_solution_url("BOLOGNA%20CENTRALE", "ROMA%20TERMINI", date=d, time="10")
    response = requests.get(train_solution_url("BOLOGNA%20CENTRALE", "ROMA%20TERMINI", date=d, time="20"))
    url.append(response)
    #print(response.text)
    response_txt = response.text
    url_dct.append(json.loads(response_txt))
    modena_dct = json.loads(modena_txt)
    i = date_lst.index(d)
    for trip in url_dct[i]:
        print(trip.get("minprice"))
        price.append(float(trip.get("minprice")))

response = requests.get(train_solution_url("BOLOGNA%20CENTRALE", "ROMA%20TERMINI", date="21/04/2020", time="20"))
print(response.text)
print("min" + str(min(price)))