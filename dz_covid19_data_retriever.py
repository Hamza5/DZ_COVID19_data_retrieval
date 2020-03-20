import json
from abc import ABC, abstractmethod
from urllib.request import urlopen


class COVID19DataRetriever(ABC):

    NOT_IMPLEMENTED = NotImplementedError("COVID19DataRetriever methods can not be called directly."
                                          "This class has to be subclassed first.")

    @abstractmethod
    def retrieve_data(self):
        raise self.NOT_IMPLEMENTED


class COVID19Maghreb(COVID19DataRetriever):

    def __init__(self):
        self.DZA_url = 'https://covid19-algerie-be.herokuapp.com/cases/wilayas/DZA'

    def retrieve_data(self):
        with urlopen(self.DZA_url) as webpage:
            dz_data = json.load(webpage)
        return dict((int(x['wilaya_id']), dict((t, int(x[t])) for t in ['cases', 'deaths', 'recovered']))
                    for x in dz_data)


if __name__ == '__main__':
    r = COVID19Maghreb()
    data = r.retrieve_data()
    with open('COVID19_Maghreb.json', 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
