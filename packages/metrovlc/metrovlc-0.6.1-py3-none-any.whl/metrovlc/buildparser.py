# -*- coding: utf-8 -*-

import argparse

from metrovlc import __version__


class BonoAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) != 12 and len(values) != 10:
            parser.error('Número de bono debe tener 10 o 12 dígitos')

        setattr(namespace, self.dest, values)


def build_parser():
    """ Parser args """
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--bono', type=str,
                        action=BonoAction,
                        dest='bono', default=None,
                        help='Número de bonometro (10 o 12 dígitos)')

    parser.add_argument('-f', '--fecha', type=str,
                        dest='fecha', default=None,
                        help='Fecha para el horario (Formato dd/mm/yyyy)')

    parser.add_argument('-d', '--horario', nargs=2, type=str,
                        dest='horario', default=None,
                        metavar=('ORIGEN', 'DESTINO'),
                        help='Horarios para ORIGEN -> DESTINO')

    parser.add_argument('-l', '--estaciones', action='store_true',
                        dest='estaciones', default=False,
                        help='Lista todas las estaciones')

    parser.add_argument('-j', '--json', action='store_true',
                        dest='json', default=False,
                        help='Muestra los resultados en formato JSON')

    parser.add_argument('-ps', '--plan', nargs=4, type=str,
                        dest='plan', default=None,
                        metavar=('ORIGEN', 'DESTINO', 'HORA', 'S|L'),
                        help='Plan para ORIGEN DESTINO HORA S|L')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    return parser
