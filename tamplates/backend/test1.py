import requests
import urllib3
import xml.dom.minidom
import xml.etree.ElementTree as ET

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

home_xml = "https://172.18.97.21/webpages/xml/home.xml"
info_battery_xml = "https://172.18.97.21/webpages/xml/ups/info_battery.xml"
info_io_xml = "https://172.18.97.21/webpages/xml/ups/info_io.xml"
info_ident_xml = "https://172.18.97.21/webpages/xml/ups/info_ident.xml"
info_status_xml = "https://172.18.97.21/webpages/xml/ups/info_status.xml"

home = requests.get("https://172.18.97.21/webpages/xml/home.xml", verify=False).text
index_ups = requests.get("https://172.18.97.21/webpages/xml/ups/index_ups.xml", verify=False) #xml-text
info_battery = requests.get("https://172.18.97.21/webpages/xml/ups/info_battery.xml", verify=False).text
info_io = requests.get("https://172.18.97.21/webpages/xml/ups/info_io.xml", verify=False).text
info_ident = requests.get("https://172.18.97.21/webpages/xml/ups/info_ident.xml", verify=False).text
info_status = requests.get("https://172.18.97.21/webpages/xml/ups/info_status.xml", verify=False).text

tree = ET.ElementTree(ET.fromstring(index_ups))
data_dict = {}
for element in tree.iter():
    # Игнорируем комментарии и текстовые узлы
    if element.tag is not ET.Comment and element.tag is not ET.Element:
        data_dict[element.tag] = element.text.strip() if element.text else ""

print(index_ups)

