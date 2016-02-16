#curl 'https://pqcc.soap.dslorder.nl/pqcc/v7.0/pqcc.aspx'
# -H 'Pragma: no-cache'
# -H 'Origin: https://pqcc.soap.dslorder.nl'
# -H 'Accept-Encoding: gzip, deflate'
# -H 'Accept-Language: en,nl;q=0.8,fr;q=0.6'
# -H 'Upgrade-Insecure-Requests: 1'
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
# -H 'Content-Type: application/x-www-form-urlencoded'
# -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
# -H 'Cache-Control: no-cache'
# -H 'Referer: https://pqcc.soap.dslorder.nl/pqcc/v7.0/pqcc.aspx'
# -H 'Connection: keep-alive'
# --data '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTExNjY2MDU5OTEPZBYCAgMPZBYCAgEPFgIeCWlubmVyaHRtbAUdVmVyc2lvbiA3LjEsIEZyaSAxNyBKdWwgMTM6NTJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQlTaG93RGVidWcFGENoZWNrZm9yVXBncmFkZURvd25HcmFkZadrpQNWL5nk7KwOV4zAatCv%2B18n
# &__VIEWSTATEGENERATOR=D8B62B3A
# &__EVENTVALIDATION=%2FwEWCAL01dzpAQLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgLo1KSVDwKE%2FfOFAgLO4PZGcfjOTnCgzFi7KmMTv8whoMIaIy4%3D
# &Postcode=1319CS&HouseNumber=105&Addition=&PhoneNumber=&ShowDebug=on&CheckButton=Check' --compressed

import HTMLParser
html_parser = HTMLParser.HTMLParser()

import requests

post_data = '__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTExNjY2MDU5OTEPZBYCAgMPZBYCAgEPFgIeCWlubmVyaHRtbAUdVmVyc2lvbiA3LjEsIEZyaSAxNyBKdWwgMTM6NTJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBQlTaG93RGVidWcFGENoZWNrZm9yVXBncmFkZURvd25HcmFkZadrpQNWL5nk7KwOV4zAatCv%2B18n&__VIEWSTATEGENERATOR=D8B62B3A&__EVENTVALIDATION=%2FwEWCAL01dzpAQLU4YLJCwLsu%2BfPCQL2soCpDQKJ%2BpbDCgLo1KSVDwKE%2FfOFAgLO4PZGcfjOTnCgzFi7KmMTv8whoMIaIy4%3D&Postcode=1319CS&HouseNumber=105&Addition=&PhoneNumber=&ShowDebug=on&CheckButton=Check'
data_url = 'https://pqcc.soap.dslorder.nl/pqcc/v7.0/pqcc.aspx'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'pqcc.soap.dslorder.nl',
    'Origin': 'https://pqcc.soap.dslorder.nl',
}
response = requests.post(url=data_url, data=post_data, headers=headers)
# print response
# print response.request.body
# print response.request.headers
# print response.content

import xml.etree.ElementTree as ET
#tree = ET.fromstring(response.content)
tree = ET.parse('1354EJ49.xml')
root = tree.getroot()
#print(tree.findall('Response')[0].findall('ExistingSituation')[0]
existing_dsl_service_id = tree.findall('Response')[0].findall('ExistingSituation')[0].attrib['ExistingDslServiceId']
name = tree.findall('Response')[0].findall('Cgb')[0].attrib['Name']
length_last_distributor = tree.findall('Response')[0].findall('Cgb')[0].attrib['LengthLastDistributor']
length_mdf = tree.findall('Response')[0].findall('Cgb')[0].attrib['LengthMdf']