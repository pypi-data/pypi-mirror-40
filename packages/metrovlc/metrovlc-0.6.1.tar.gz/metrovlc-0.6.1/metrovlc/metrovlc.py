# -*- coding: utf-8 -*-

import re
import time
import certifi
import json
import urllib.request

from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from metrovlc import buildparser


def card_balance(bono):
    """ retorna el saldo de un bono de metrovalencia """

    # titulo = None
    bonoinfo = {'cardNumber': bono}

    urlapi = 'https://www.metrovalencia.es/tools_consulta_tsc.php?tsc='

    # try:
    url = '{_urlapi}{_bono}'.format(_urlapi=urlapi, _bono=bono)
    r = urllib.request.urlopen(url, cafile=certifi.where())
    enc = r.info().get_content_charset('utf-8')
    data = r.read()
    html = data.decode(enc)

    # tipo de titulo
    f = re.findall('Título: (.*)<br>', html)
    if f:
        # titulo = f[0]
        bonoinfo['cardZones'] = f[0]

    # saldo
    f = re.findall('Saldo.*: (.*) <', html)
    if f:
        if '€' in str(f[0]):
            bonoinfo['cardCurrency'] = 'Euros'
        else:
            bonoinfo['cardCurrency'] = None

        # el saldo viene algo sucio
        s = str(f[0]).replace('€', '')
        s = s.replace(' ', '')
        s = s.replace(',', '.')

        bonoinfo['cardBalance'] = float(s)

    return bonoinfo


def stations():
    """ recupera todas las estaciones """

    sts = dict()
    url = 'https://www.metrovalencia.es/tools_horarios.php'
    r = urllib.request.urlopen(url, cafile=certifi.where())
    enc = r.info().get_content_charset('utf-8')
    data = r.read()
    html = data.decode(enc)

    for f in re.findall('<option value="(\d*)">(.+?(?=<))', html):
        sts[f[0]] = f[1]

    return sts


def key_station(st):
    """ recuperamos el id de una estación """

    sts = stations()

    for k, v in sts.items():
        if SequenceMatcher(None, v, st).ratio() > 0.65:
            return k, v

    return None, None


def routes(origen, destino, fecha=None, hini='00:00', hfin='23:59'):
    """ Obtiene los horarios desde origen a destino """

    route = dict()

    # verificamos tanto el origen como el destino
    k_station_orig, value_station_orig = key_station(origen)
    k_station_dest, value_station_dest = key_station(destino)

    # Si alguna de las dos es None, salimos
    if not k_station_orig or not k_station_dest:
        return None

    urlapi = 'https://www.metrovalencia.es/horarios.php'
    apiparam = '?origen=%s&hini=%s&hfin=%s&destino=%s&fecha=%s&calcular=1'

    # Recuperamos la fecha y hora de la consulta
    if not fecha:
        fecha = time.strftime('%d%%2F%m%%2F%Y')
    else:
        fecha = fecha.replace('/', '%2F')
    hini = hini.replace(':', '%3A')
    hfin = hfin.replace(':', '%3A')

    # # Empezamos a completar los datos del diccionario
    route['routeId'] = 0
    route['fromStation'] = k_station_orig
    route['toStation'] = k_station_dest
    route['fromStationText'] = value_station_orig
    route['toStationText'] = value_station_dest

    # completamos los parámetros
    param = apiparam % (k_station_orig, hini, hfin, k_station_dest, fecha)

    url = urlapi + param

    r = urllib.request.urlopen(url, cafile=certifi.where())
    enc = r.info().get_content_charset('utf-8')
    data = r.read()
    html = data.decode(enc)

    soup = BeautifulSoup(html, "html.parser")
    consulta = soup.body.find('div', attrs={'class': 'consulta'})

    # Recupero los li
    for li in consulta.findAll('li'):
        for r in re.findall('Día: (\d\d\/\d\d\/\d\d\d\d)', str(li)):
            route['date'] = r

        for r in re.findall('Franja horaria: de (\d\d:\d\d) a (\d\d:\d\d)',
                            str(li)):
            route['initHour'] = r[0]
            route['finalHour'] = r[1]

        for r in re.findall('trayecto: (\d*)', str(li)):
            route['duration'] = int(r)

        for r in re.findall('zonas: (\w*)', str(li)):
            route['zoneTickets'] = r

    # cuantos transbordos hay
    route['journey'] = list()
    transbordos = soup.body.findAll('span',
                                    attrs={'class': 'texto_transbordo'})
    j = 0
    for transbordo in transbordos:
        for r in re.findall('De (.*) a (.*)<', str(transbordo)):
            journey = dict()
            journey['journeyId'] = j
            journey['journeyFromStation'] = key_station(r[0])
            journey['journeyToStation'] = key_station(r[1])
            route['journey'].append(journey)
            j = j + 1

    # los trenes que hay en cada uno de los transbordos
    j = 0
    for h3 in consulta.findAll('h3'):
        for r in re.findall('con destino: (.*)<', str(h3)):
            route['journey'][j]['journeyTrains'] = r.split(', ')
            j = j + 1

    # y ahora los horarios...
    j = 0
    for table in consulta.findAll('table'):
        route['journey'][j]['journeyHours'] = list()
        for td in table.findAll('td'):
            for r in re.findall('(\d\d:\d\d)', str(td)):
                route['journey'][j]['journeyHours'].append(str(r))
        j = j + 1

    # guardamos aquí todos los cambios que queremos
    reemplazos = [['<td>', ''],
                  ['</td>', ' | '],
                  ['<tr>', ''],
                  ['</tr>', '\n'],
                  ['---', '-----'],
                  ['</li>', '\n'],
                  ['Trenes con destino', ', Trenes con destino'],
                  ['Hora de salida', ', Hora de salida\n'],
                  ['Imprimir la consulta', ''],
                  ['Paso ', '\nPaso '],
                  ['td>', ' | ']]

    for reemplazo in reemplazos:
        consulta = str(consulta).replace(reemplazo[0], reemplazo[1])

    route['text'] = BeautifulSoup(consulta, "html.parser").get_text()

    return route


def plan(origen, destino, fecha=None, hora='00:00', tipohora='S'):
    """ Obtiene la ruta para llegar o salir a una hora dada """

    p = dict()

    # Convertimos el flag tipo de hora en algo entendible:
    # S: Salida
    # L: Llegada
    if tipohora == 'S':
        tipohora = 'D'
    else:
        tipohora = 'A'

    # verificamos tanto el origen como el destino
    k_station_orig, value_station_orig = key_station(origen)
    k_station_dest, value_station_dest = key_station(destino)

    # Si alguna de las dos es None, salimos
    if not k_station_orig or not k_station_dest:
        return None

    p['routeId'] = 0
    p['fromStation'] = k_station_orig
    p['toStation'] = k_station_dest
    p['fromStationText'] = value_station_orig
    p['toStationText'] = value_station_dest
    p['zoneTickets'] = ''
    p['journey'] = list()
    p['hour'] = hora

    urlapi = 'https://www.metrovalencia.es/planificador.php'
    apiparam = ('?origen=%s&destino=%s&dir_origen=&origen_x=&origen_y='
                '&dir_destino=&destino_x=&destino_y=&hora=%s&tipo_hora=%s'
                '&fecha=%s&calcular=1')

    # Recuperamos la fecha y hora de la consulta
    if not fecha:
        fecha = time.strftime('%d%%2F%m%%2F%Y')
    else:
        fecha = fecha.replace('/', '%2F')
    hora = hora.replace(':', '%3A')

    p['date'] = fecha.replace('%2F', '/')

    # completamos los parámetros
    param = apiparam % (k_station_orig, k_station_dest, hora, tipohora, fecha)
    url = urlapi + param

    r = urllib.request.urlopen(url, cafile=certifi.where())
    enc = r.info().get_content_charset('utf-8')
    data = r.read()
    html = data.decode(enc, errors='ignore')
    # html = data.decode('ISO-8859-1')

    soup = BeautifulSoup(html, "html.parser")

    # general
    sheet = soup.body.find('div', attrs={'class': 'sheet'})

    for strong in sheet.findAll('strong'):
        rx = '> (\d+) minu.*salida a las (\d\d:\d\d) llegada a las (\d\d:\d\d)'
        for r in re.findall(rx, str(strong)):
            p['duration'] = int(r[0])
            p['exitHour'] = r[1]
            p['arrivalHour'] = r[2]

    # steps (journeys...)
    steps = sheet.findAll('div', attrs={'class': 'step'})

    # ñapa total, revisar
    for i in range(1, len(steps) - 1):

        journey = dict()
        journey['journeyId'] = i - 1

        rx = 'línea (\d+).*dirección (.+) en la estación (.+)<br'
        for r in re.findall(rx, str(steps[i])):
            journey['journeyTrains'] = [(r[1])]

        rx = 'time">(\d\d:\d\d).*alt="(\d+)".* Salida de (.+)<br'
        for r in re.findall(rx, str(steps[i])):
            journey['journeyFromStation'] = key_station(str(r[2]))
            journey['journeyFromStationText'] = str(r[2])
            journey['journeyHours'] = str(r[0])

        rx = 'time">(\d\d:\d\d).*alt="(\d+)".* Llegada a (.+)<br'
        for r in re.findall(rx, str(steps[i])):
            journey['journeyToStation'] = key_station(str(r[2]))
            journey['journeyToStationText'] = str(r[2])
            journey['journeyHours'] = str(r[0])

        rx = 'Transbordo en (.+) y toma la línea (\d+) en dirección (.+)<br'
        for r in re.findall(rx, str(steps[i])):
            journey['journeyTrains'] = [(r[2])]

        # No utilizo por ahora estos datos
        # for r in re.findall('"duration">(\d+) minutos', str(steps[i])):
        #     print('duracion minutos: ', r)

        p['journey'].append(journey)

    return p


def main():

    """Run the command-line interface."""
    parser = buildparser.build_parser()
    options = parser.parse_args()

    if options.bono:
        # Para metrovalencia, únicamente son importantes los 10 primeros
        # dígitos, cosa bastante marciana
        bono = options.bono[0:10]
        card = card_balance(bono)
        if options.json:
            print(json.dumps(card))
        else:
            if ('cardZones' in card
               and 'cardBalance' in card
               and 'cardCurrency' in card):
                strformat = 'Bono:{}, Título:{}, saldo:{} {}'
                print(strformat.format(bono,
                                       card['cardZones'],
                                       card['cardBalance'],
                                       card['cardCurrency']))

    if options.horario:
        origen = options.horario[0]
        destino = options.horario[1]
        ruta = routes(origen, destino, options.fecha)
        if options.json:
            ruta['text'] = ''
            print(json.dumps(ruta))
        else:
            if ruta:
                print(ruta['text'])
            else:
                print('No se encuentra horario: {} -> {}'.format(origen,
                                                                 destino))

    if options.estaciones:
        sts = stations()
        if options.json:
            print(json.dumps(sts))
        else:
            print('Estaciones disponibles:')
            for st in sts:
                print(sts[st])

    if options.plan:
        origen = options.plan[0]
        destino = options.plan[1]
        hora = options.plan[2]
        tipo = options.plan[3]

        p = plan(origen, destino, hora=hora, tipohora=tipo)

        if options.json:
            print(json.dumps(p))
        else:
            print(('Viaje de {} a {}, para el día {}: '
                   'Salida a las {}, '
                   'llegada a las {}'.format(p['fromStationText'],
                                             p['toStationText'],
                                             p['date'],
                                             p['exitHour'],
                                             p['arrivalHour'])))


if __name__ == '__main__':
    main()
