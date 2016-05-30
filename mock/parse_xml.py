import os
import xml.etree.ElementTree as ET

import xmltodict

with open('1273JT_50.xml', 'r') as file:
    content = file.read()
    tree = ET.fromstring(content)

    doc = xmltodict.parse(content)

    response = dict(
        deliverable_product=list()
    )

    # Search the dict for the dat that we need and transform it if needed
    pqcc_response = doc['PqccResponse']
    deliverable_products = pqcc_response['DeliverableProducts']
    deliverable_product = deliverable_products['DeliverableProduct']

    existing_situation = pqcc_response['ExistingSituation']
    existing_situation_copper = existing_situation['ExistingSituationCopper']
    existing_situation_fiber = existing_situation['ExistingSituationFiber']
    remarks = existing_situation['Remarks']

    # Output to the view that consumes it
    response['deliverable_product'] = deliverable_products['DeliverableProduct']
    response['existing_situation_copper'] = existing_situation_copper
    response['existing_situation_fiber'] = existing_situation_fiber
    response['remarks'] = remarks['Remark']

    print(tree.PqccResponse)
    print(tree.findall('DeliverableProducts'))