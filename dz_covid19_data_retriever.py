import sys
import json
from abc import ABC, abstractmethod
from urllib.request import urlopen
from argparse import ArgumentParser, FileType


class COVID19DataRetriever(ABC):

    NOT_IMPLEMENTED = NotImplementedError("COVID19DataRetriever methods can not be called directly."
                                          "This class has to be subclassed first.")

    @abstractmethod
    def retrieve_data(self):
        raise self.NOT_IMPLEMENTED


class COVID19HistoricalDataRetriever(COVID19DataRetriever, ABC):

    @abstractmethod
    def retrieve_data(self, historical):
        raise self.NOT_IMPLEMENTED


class COVID19Maghreb(COVID19DataRetriever):
    """
    Data retriever that uses the data from: www.covid19-maghreb.live
    """

    def __init__(self):
        self.DZA_url = 'https://covid19-algerie-be.herokuapp.com/cases/wilayas/DZA'

    def retrieve_data(self):
        with urlopen(self.DZA_url) as webpage:
            dz_data = json.load(webpage)
        return dict((int(x['wilaya_id']),
                     dict((k1, int(x[k2])) for k1, k2 in [('confirmed', 'cases'), ('deaths',)*2, ('recovered',)*2]))
                    for x in dz_data)


class ArcGisMaps(COVID19HistoricalDataRetriever):
    """
    Data retriever that uses the data from:
    abdelghafour.maps.arcgis.com/apps/opsdashboard/index.html?fbclid=IwAR06TyO9BGI6r-V1yJ8JSgda-56rbO4o0rp3-l0-SmNeJJ_JD_q3Fb0mVBo#/ad57a9371f6a4bf7b1b7881be4cdb8ae
    """

    def __init__(self):
        self.wilayat_url = 'https://services9.arcgis.com/jaH8KnBq5el3w2ZR/arcgis/rest/services/Merge_Cas_confirm%C3%A9s_Alger_wilaya/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=9783&geometry={%22xmin%22%3A-0.000001903623342514038%2C%22ymin%22%3A0.000001903623342514038%2C%22xmax%22%3A5009377.085694846%2C%22ymax%22%3A5009377.085698653%2C%22spatialReference%22%3A{%22wkid%22%3A102100%2C%22latestWkid%22%3A3857}}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile'
        self.historical_url = 'https://services5.arcgis.com/sWkwsJZKv125vc6b/arcgis/rest/services/informations_coronavirus_alg%C3%A9rie/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=declardate%20desc&outSR=102100&resultOffset=0&resultRecordCount=1000&cacheHint=true'

    def retrieve_data(self, historical):
        if not historical:
            with urlopen(self.wilayat_url) as file:
                wilayat_data = json.load(file)['features']
            useful_data = dict()
            for wilaya_dict in wilayat_data:
                w = wilaya_dict['attributes']
                useful_data[w['WILAYA']] = {'confirmed': w['Cas_confirm'], 'deaths': w['Décés'],
                                            'recovered': w['Récupér'], 'active': w['active'] or 0,
                                            'males': w['Males'], 'females': w['Femelle'], 'date': w['Date_rapport']}
            return useful_data
        else:
            with urlopen(self.historical_url) as file:
                news_data = json.load(file)['features']
            useful_data = []
            for news_dict in reversed(news_data):
                n = news_dict['attributes']
                useful_data.append({
                    'date': n['declardate'],
                    'type': n['typecas'],
                    'type_cases': n['nbcas'],
                    'cumulative_type_cases': n['nbcascumules'],
                    'confirmed': n['confirmes'],
                    'recovered': n['retablis'],
                    'deaths': n['decedes'],
                    'total_confirmed': n['totalconfirmes'],
                    'total_recovered': n['totalretablis'],
                    'total_deaths': n['totaldecedes'],
                    'males': n['hommes'],
                    'females': n['femmes'],
                    'province': n['wilaya'],
                    'municipality': n['commune'],
                    'hospital': n['hopital'],
                    'title': n['titre'],
                    'description': n['description'],
                    'reference': n['reference'],
                })
            return useful_data


parser = ArgumentParser(description='A script to get data of COVID-19 in Algeria from different sources as JSON file.')
parser.add_argument('--source', '-s', required=True, choices=[COVID19Maghreb.__name__, ArcGisMaps.__name__],
                    help='The source used to get the data.')
parser.add_argument('--output-file', '-o', type=FileType('w', encoding='UTF-8'), default=sys.stdout,
                    help='The path of the output file used the store the data.')
parser.add_argument('--historical', '-t', action='store_true',
                    help='Get the full history of data, not just the last update (Not available in all sources).')

if __name__ == '__main__':
    args = parser.parse_args()
    data = dict()
    if args.source == COVID19Maghreb.__name__:
        retriever = COVID19Maghreb()
        data = retriever.retrieve_data()
    elif args.source == ArcGisMaps.__name__:
        retriever = ArcGisMaps()
        data = retriever.retrieve_data(args.historical)
    json_text = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
    print(json_text, file=args.output_file)
