# coding:utf-8
import os
import requests
import common_patterns
import profig
import geoip2.database
import xprint as xp

URL_IP_API = 'http://ip-api.com/json/'
URL_MYIP = 'https://api.myip.com/'
IP_DICT = {
    'ip': None,
    'country': None,
    'country_code': None,
    'asn': None,
    'aso': None,
}


class IPu:
    def __init__(self, path_to_config: str = 'config.ini'):
        self._cfg = profig.Config(path_to_config)
        self._cfg.init('geoip2.path_to_country', '/data/storage/GeoLite2/GeoLite2-Country.mmdb')
        self._cfg.init('geoip2.path_to_city', '/data/storage/GeoLite2/GeoLite2-City.mmdb')
        self._cfg.init('geoip2.path_to_asn', '/data/storage/GeoLite2/GeoLite2-ASN.mmdb')
        self._cfg.init('ip_query.timeout', 10)
        self._cfg.sync()

        for key in ['path_to_country', 'path_to_city', 'path_to_asn']:
            if not os.path.exists(self._cfg['geoip2.{}'.format(key)]):
                raise Exception('GeoLite2 DB file "{}" does not exist'.format(self._cfg['geoip2.{}'.format(key)]))

    def __result_geo_update(self, result):
        if result:
            geoip = self.geoip(result['ip'])
            if geoip:
                for key in IP_DICT.keys():
                    if geoip[key]:
                        result[key] = geoip[key]
            return result

        return None

    def get_ip(self, requests_proxies: dict = None):
        result = self.get_by_myip(requests_proxies=requests_proxies)

        if not result:
            result = self.query_by_ip_api(requests_proxies=requests_proxies)

        if result:
            return result

        return None

    def query_by_ip_api(self, ip_address: str = None, requests_proxies: dict = None):
        url = URL_IP_API

        if ip_address:
            url += ip_address

        try:
            resp = requests.post(url,
                                 params={'fields': 651263},
                                 proxies=requests_proxies,
                                 timeout=self._cfg['ip_query.timeout'])

            if 200 == resp.status_code:
                data = resp.json()
                if 'success' == data['status']:
                    result = IP_DICT.copy()
                    result['ip'] = data['query']
                    result['country'] = data['country']
                    result['country_code'] = data['countryCode']
                    # r['region'] = data['regionName']
                    # r['region_code'] = data['region']
                    # r['city'] = data['city']
                    # r['district'] = data['district']
                    # r['zip'] = data['zip']
                    # r['lon'] = data['lon']
                    # r['lat'] = data['lat']
                    # r['timezone'] = data['timezone']
                    # r['isp'] = data['isp']
                    # r['org'] = data['org']
                    # r['as'] = data['as']
                    result['asn'] = common_patterns.find_asn(data['as'])
                    result = self.__result_geo_update(result)
                    return result

        except Exception as e:
            xp.error('IPQuery-query_by_ip_api error: {}'.format(e))
            return None

        return None

    def get_by_myip(self, requests_proxies: dict = None):
        try:
            resp = requests.post(URL_MYIP,
                                 proxies=requests_proxies,
                                 timeout=self._cfg['ip_query.timeout'])

            if 200 == resp.status_code:
                data = resp.json()

                result = IP_DICT.copy()
                result['ip'] = data['ip']
                result['country'] = data['country']
                result['country_code'] = data['cc']
                result = self.__result_geo_update(result)
                return result

        except Exception as e:
            xp.error('IPQuery-get_by_myip error: {}'.format(e))
            return None

        return None

    def geoip(self, ip_address):
        result = IP_DICT.copy()
        result['ip'] = ip_address

        # # country
        # with geoip2.database.Reader(self._cfg['geoip2.path_to_country']) as reader:
        #     resp = reader.country(ip_address)
        #     result['country'] = resp.country.name
        #     result['country_code'] = resp.country.iso_code

        # city
        with geoip2.database.Reader(self._cfg['geoip2.path_to_city']) as reader:
            resp = reader.city(ip_address)
            result['country'] = resp.country.name
            result['country_code'] = resp.country.iso_code

        # asn
        with geoip2.database.Reader(self._cfg['geoip2.path_to_asn']) as reader:
            resp = reader.asn(ip_address)
            result['asn'] = resp.autonomous_system_number
            result['aso'] = resp.autonomous_system_organization

        return result
