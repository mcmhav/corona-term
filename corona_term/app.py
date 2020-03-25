# https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
# curl "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true" | jq '.features'
# curl "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=(Confirmed%20%3E%200)%20AND%20(Country_Region%3D%27Norway%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true" | jq

# curl "https://www.vg.no/spesial/2020/corona-viruset/data/daily-reports/" | jq 'del(.data) | del(.diff)'
# curl "https://www.vg.no/spesial/2020/corona-viruset/data/norway-table-overview/?region=county" | jq '.totals'
from urllib.parse import urlencode

import requests

from corona_term.response import Response


class App():
    """Corona app."""

    def __init__(self, base: str = 'https://services1.arcgis.com'):
        self._base = base
        self._query_path = '0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query'

    @staticmethod
    def _create_where_clause(country_region: str = 'Norway') -> str:
        return f"(Confirmed > 0) AND (Country_Region = '{country_region}')"

    @staticmethod
    def _create_query(where: str) -> str:
        """
        f=json&
        where=(Confirmed%20%3E%200)%20AND%20(Country_Region%3D%27Norway%27)&
        returnGeometry=false&
        spatialRel=esriSpatialRelIntersects&
        outFields=*&
        outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&
        outSR=102100&
        cacheHint=true

        f=json&
        where=%28Confirmed%2520%253E%25200%29%2520AND%2520%28Country_Region%253D%2527Norway%2527%29&
        returnGeometry=false&
        spatialRel=esriSpatialRelIntersects&
        outFields=%2A&
        outStatistics=%255B%257B%2522statisticType%2522%253A%2522sum%2522%252C%2522onStatisticField%2522%253A%2522Confirmed%2522%252C%2522outStatisticFieldName%2522%253A%2522value%2522%257D%255D&
        outSR=102100&
        cacheHint=true
        """
        return urlencode({
            'f':
            'json',
            'where':
            where,
            'returnGeometry':
            'false',
            'spatialRel':
            'esriSpatialRelIntersects',
            'outFields':
            '*',
            'outStatistics': [{
                'statisticType': 'sum',
                'onStatisticField': 'Confirmed',
                'outStatisticFieldName': 'confirmed',
            }, {
                'statisticType': 'sum',
                'onStatisticField': 'Deaths',
                'outStatisticFieldName': 'deaths',
            }, {
                'statisticType': 'sum',
                'onStatisticField': 'Recovered',
                'outStatisticFieldName': 'recovered',
            }],
            'outSR':
            '102100',
            'cacheHint':
            'true',
        })

    def fetch(self) -> None:
        where = self._create_where_clause()
        query = self._create_query(where)
        r = requests.get(f'{self._base}/{self._query_path}?{query}')

        if r.status_code == 200:
            response = Response(**r.json())
            for feature in response.features:
                print(feature)
