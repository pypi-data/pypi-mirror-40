import requests
from lxml import html
import json
import re
import unicodedata

class GygReader:
    LOGIN_URL = 'https://supplier.getyourguide.com/en/login'
    DATA_URL = 'https://supplier.getyourguide.com/bookings_load'
    PARAMS = {
                'accept-encoding': 'gzip, deflate, br',
                'content-type': 'application/x-www-form-urlencoded',
                "authority": "supplier.getyourguide.com",
                "Origin": "https://supplier.getyourguide.com",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Referer": "https://supplier.getyourguide.com/en/bookings",
            }
    POST_DATA = {
                'action': 'filter',
                'tour_id': '-1',
                'dateFilterFrom': '-1',
                'dateFilterTo': '-1',
                'booking_reference': '',
                'number_of_loaded_bookings': '0'
                }

    def __init__(self, email, password):
        self.login =  {'email': email,'passwd': password}
        self.session = requests.Session()
        self.response = None
        self.gyg_login()

    def gyg_login(self):
        self.session.post(self.LOGIN_URL, data = self.login)

    def get_booking(self, gyg_id):
        self.POST_DATA["booking_reference"] = gyg_id
        self.response = self.session.post(self.DATA_URL, params=self.PARAMS, data=self.POST_DATA)
        return(self.get_booking_details(gyg_id))

    def get_booking_details(self, gyg_id):
        gyg_number = re.search('(GYG)(\d+)',gyg_id).group(2)
        html_response = html.fromstring(self.response.json()["bookings_list_html"])

        product = html_response.xpath(("//*[@id='b_{0}']/div[2]/div[1]/div[2]/div[1]/strong").format(gyg_number))
        customer_email = html_response.xpath(("//*[@id='b_{0}']/div[3]/div[1]/p[2]/span[2]").format(gyg_number))
        customer_name = html_response.xpath(("//*[@id='b_{0}']/div[3]/div[1]/p[2]/span[1]").format(gyg_number))
        customer_phone = html_response.xpath(("//*[@id='b_{0}']/div[3]/div[1]/p[2]/span[3]/text()").format(gyg_number))
        amount = html_response.xpath(("//*[@id='b_{0}']/div[2]/div[2]/div[3]/strong[1]").format(gyg_number))
        booking_details = {
                            "customer_email": customer_email[0].text.strip(),
                            "customer_name": customer_name[0].text.strip(),
                            "customer_phone": customer_phone[1].strip(),
                            "product": unicodedata.normalize("NFKD", product[0].text.strip()),
                            "amount": amount[0].text.strip(),
                        }
        return(booking_details)

