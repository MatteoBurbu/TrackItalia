import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

# Create the URL for the requests
# [STAZIONEPARTENZA] = BOLOGNA CENTRALE: Il nome della stazione di partenza, come restituito dall'autocompletamento
#                       stazione (vedi sotto)
# [STAZIONEARRIVO]: Il nome della stazione di arrivo
# [AR]: Può valere 'A' oppure 'R', la prima se si stanno cerando viaggi di sola andata, la seconda per viaggi a/r
# [DATA]: Data in formato dd/mm/yyyy
# [ORA]: L'ora di partenza in formato hh
# [OFFSET]: Se specificato, ritorna le soluzioni a partire dalla n-esima trovata fino alla n+5-esima.
#                       Essenziale per espandere la finestra di ricerca oltre le prime 5 soluzioni ritornate di default,
#                       che potrebbero non coprire tutte quelle esistenti nell'ora selezionata
# [ADULTI]/[BAMBINI]: Rispettivamente il numero di adulti o bambini per cui cercare il viaggio
# [DIRECTION]: Può valere solo 'A' se [AR] è 'A', altrimenti vale 'A' oppure 'R' a seconda se si stanno cercando le
#                       soluzioni di andata o di ritorno in un viaggio a/r
# [FRECCE]/[REGIONALI]: Booleani, 'true' per cercare solo soluzioni con alta velocità / treni regionali,
#                       'false' altrimenti. Settarli entrambe a true non ha effetto. (Sì, ci ho provato :P)
# [DATARITORNO]/[ORARITORNO]: Questi campi sono omessi se [AR] è 'A', altrimenti sono il duale di [DATA] e [ORA] per
#                       il viaggio di ritorno
# [CODICE_CARTAFRECCIA]: Campo opzionale. Se fornito verranno mostrati i prezzi al netto di eventuali promozioni attive
#                       per quella specifica cartafreccia. Il codice deve essere valido. Se il parametro viene
#                       specificato, va aggiunto in coda all'url '&positions=0', altrimenti restituisce un errore

def train_solution_url(station_start, station_end, ar_flag="A", date="01/01/2020", time="0", offset="0", n_adults="1",
                       n_children="0", direction="A", is_frecce="true", is_regional="false", date_r="0",
                       time_r=str(int("0") + 2), freccia_card="0"):
    station_start = station_start.upper()
    station_end = station_end.upper()
    station_start = station_start.split(' ')
    station_end = station_end.split(' ')
    if len(station_start) == 2:
        station_start = station_start[0] + "%20" + station_start[1]
    else:
        station_start = str(station_start[0])
    if len(station_end) == 2:
        station_end = station_end[0] + "%20" + station_end[1]
    else:
        station_end = str(station_end[0])
    url = "https://www.lefrecce.it/msite/api/solutions?origin=" + station_start + \
          "&destination=" + station_end + \
          "&arflag=" + ar_flag + \
          "&adate=" + date + \
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
    return url

# s = 1587578460000 / 1000.0
# d = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
# print(d)

# numdays = 30
# base = datetime.datetime.today()
# date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
# date_lst = []
# for d in date_list:
#     date_lst.append(str(d.strftime("%d/%m/%Y")))
# print(date_lst)

# test = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/228/458/2015-01-26T00:00:00')
# test = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/5043/458/2020-04-18T00:00:00')
# print(test.json())

# name = requests.get('http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/BOLO')
# print(name.text)

# https://www.lefrecce.it/msite/api/solutions?origin=MILANO%20CENTRALE&destination=ROMA%20TERMINI&arflag=A&adate=28/04/2020&atime=17&adultno=1&childno=0&direction=A&frecce=false&onlyRegional=false

# modena = requests.get('https://www.lefrecce.it/msite/api/geolocations/locations?name=mode')
# print(modena.json())
# modena_txt = modena.text
# print(modena_txt)
# # modena_text = json.dumps(modena)
# modena_dct = json.loads(modena_txt)
# for dct in modena_dct:
#     if dct.get("name") == "MODENA":
#         print(dct.get("id"))
#         modena_id = dct.get("id")

#
# bologna = requests.get('https://www.lefrecce.it/msite/api/geolocations/locations?name=bolo')
# bologna_txt = bologna.text
# bologna_dct = json.loads(bologna_txt)
# print(bologna.json())
# for dct in bologna_dct:
#     if dct.get("name") == "BOLOGNA CENTRALE":
#         print(dct.get("id"))
#         bologna_id = dct.get("id")

# url = []
# url_dct = []
# price = []
# for d in date_lst:
#     response = requests.get(train_solution_url("BOLOGNA CENTRALE", "ROMA TERMINI", date=d, time="20"))
#     url.append(response)
#     #print(response.text)
#     response_txt = response.text
#     url_dct.append(json.loads(response_txt))
#     modena_dct = json.loads(modena_txt)
#     i = date_lst.index(d)
#     for trip in url_dct[i]:
#         price_trip = trip.get("minprice")
#         print(price_trip)
#         if price_trip != 0.0:
#             price.append(price_trip)
#
# response = requests.get(train_solution_url("ROMA TIBURTINA", "ROMA TERMINI", date="23/04/2020", time="03",offset = "13", is_regional = "false", is_frecce = "true"))
# print("offset 10")
# print(response.text)
# print("min " + str(min(price)))
# print(price)
#

# Define the trip
station_start = "Bologna Centrale"
station_end = "Roma Tiburtina"
# date_start = datetime.datetime.today() # or any date using datetime.datetime(yyyy, mm, dd)
date_start = datetime.datetime(2020, 6, 10)
date_end = datetime.datetime(2020, 6, 20)

# Create a list of string date
delta = date_end - date_start
num_days = delta.days
base = date_start
date_list = [base + datetime.timedelta(days=x) for x in range(num_days)]
date_lst = []
for d in date_list:
    date_lst.append(str(d.strftime("%d/%m/%Y")))

trip_lst = []
trip_price = []
idsol_lst = []
trip_min_price_lst = []
for d in date_lst:
    restart = True
    while restart:
        n = "0"
        trip_daily_lst = []
        trip_daily_price = []
        trip_daily_min_price = []
        idsol_daily = []
        i = 0
        while i == 0:
            trip = requests.get(train_solution_url(station_start, station_end,
                                                   offset=n, date=d, time="04", is_regional="false", is_frecce="true"))
            return_msg = str(trip)
            # Check for errors on the requests, in that case it repeats the requests
            if return_msg == "<Response [200]>":
                restart = False
            elif return_msg == "<Response [400]>":
                print("Syntax Error")
                restart = False
                break
            else:
                print("Error on " + d)
                print(trip)
                restart = True
                break
            print(return_msg + " " + d)
            trip_txt = trip.text
            trip_dct = json.loads(trip_txt)
            # Check for case of good requests but empty response due to the offset
            if len(trip_dct) == 0:
                i = 1
                break
            departure_date = []
            today_date = datetime.datetime.today().strftime('%d/%m/%Y')
            selected_date = d
            for dct in trip_dct:
                departure_time = dct.get("departuretime") / 1000
                departure_date.append(datetime.datetime.fromtimestamp(departure_time).strftime('%d/%m/%Y'))
                # Save data for trips on that day
                if departure_date[-1] == selected_date:
                    trip_daily_lst.append(dct)
                    min_price = dct.get("minprice")
                    trip_daily_price.append(dct.get("minprice"))
                    idsol_daily.append(dct.get('idsolution'))
                    if min_price != 0.0:
                        trip_daily_min_price.append(min_price)
            # Check if we need to do more requests for that day
            if departure_date[-1] == selected_date and len(trip_dct) == 5:
                n = str(int(n) + 5)
            else:
                print("Trip in this day " + str(len(trip_daily_lst)))
                i = 1
        print("Daily price " + str(trip_daily_price))
        trip_lst.append(trip_daily_lst)
        trip_price.append(trip_daily_price)
        trip_min_price_lst.append(trip_daily_min_price)
        idsol_lst.append(idsol_daily)

# Create a list with the minimum price for each day
min_price_lst = []
for lst_price in trip_price:
    if len(lst_price) != 0:
        min_price_lst.append(min(lst_price))
    else:
        min_price_lst.append(0)  # 0 on days when no trips are available

for d in idsol_lst:
    for id_trip in d:
        details = requests.get("https://www.lefrecce.it/msite/api/solutions/" + id_trip + "standardoffers[?codeFiltered=true]")
        # print(id_trip)
        print(details.text)
# print(trip_lst)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(range(0, len(min_price_lst)), min_price_lst)  # Plot some data on the axes.
print(min_price_lst)
plt.show()

# print()
# print("full trip")
# print(trip)
# print(departure_date)
#
# print(trip_price)
# plt.show()
