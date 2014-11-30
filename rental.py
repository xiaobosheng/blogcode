# -*- coding: utf-8 -*-
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

class CostcoRental(object):
    def __init__(self, pickupdate, pickuptime, returndate, returntime, pickuplocation, returnlocation, age=25):
        self.pickupdate = pickupdate
        self.pickuptime = pickuptime
        self.pickuplocation = pickuplocation
        self.returndate = returndate
        self.returntime = returntime
        self.returnlocation = returnlocation
        self.driverage = age
        self.url = 'http://www.costcotravel.com/carSearch.act'
        self.details = self.lookup()

    def lookup(self):
        params = {'cs': 1,
                  'driverAge': self.driverage,
                  'dropoffAsAirport': True,
                  'dropoffCity': self.returnlocation,
                  'dropoffDate': self.returndate,
                  'dropoffTime': self.returntime,
                  'pickupAsAirport': True,
                  'pickupCity': self.pickuplocation,
                  'pickupDate': self.pickupdate,
                  'pickupTime': self.pickuptime
        }
        res = requests.post(self.url, data=params)
        return res.text

    def get_prices(self):
        soup = BeautifulSoup(self.details)
        car_types = soup.find_all(lambda tag: tag.name == 'th' and tag.get('class') == ['tar'])
        result = defaultdict(list)
        for car_type in car_types:
            # include outer 'tr' which contains data we need
            prices_raw = car_type.find_parents("tr")
            # get key type and use as a result key
            result_car_key = prices_raw[0].find('th').text
            # get all prices that saved in a link with class = 'u '
            final_price_by_car = prices_raw[0].find_all("a", {'class': 'u'})
            # add prices to result set
            for price in final_price_by_car:
                result[result_car_key.lower()].append(price.text)
        return result

    def best_price(self, cartype):
        car_type = cartype.lower()
        price_chart = self.get_prices()
        if car_type not in price_chart:
            return 'Not Available'
        else:
            if not price_chart[car_type]:
                return 'Not Available'
            else:
                return sorted(price_chart[car_type], key=lambda x: float(x[1:].replace(',', '')))[0]


if __name__ == '__main__':
    #Sample usage
    mia = CostcoRental('12/21/2014', '01:00 PM', '12/27/2014', '10:00 AM', 'MIA', 'MIA')
    #This should print a best price
    print(mia.best_price('intermediate suv'))
    print(mia.best_price('standard car'))