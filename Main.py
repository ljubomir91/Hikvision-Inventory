import requests
from requests.auth import HTTPDigestAuth
from xml.etree import ElementTree

IP = "10.20.48.47"

# Get Different Information via API calls
streamstatus = f"https://{IP}/ISAPI/Streaming/status"
videostream = f"https://{IP}/ISAPI/Streaming/channels/101"
workingstatus = f"https://{IP}/ISAPI/System/workingstatus/chanStatus?format=json"
deviceinfo = f"https://{IP}/ISAPI/System/deviceinfo"
network_interface = f"https://{IP}/ISAPI/System/Network/interfaces/1"
camera_reboot = f"https://{IP}/System/reboot"
http_call = f"http://{IP}/ISAPI/System/deviceinfo"
login_page = f"http://{IP}/doc/page/login.asp"
# webpower = "http://10.144.20.49/index.htm"
# webpower2 = "http://10.49.20.243/index.htm/outlet?a=CCL"
# webpower3 ="http://10.49.20.243/restapi/relay/outlets/=0,1,4/state/"
# curl -u admin:1234 -X POST -H "X-CSRF: x"  --digest "http://192.168.0.100/restapi/relay/outlets/0/cycle/
# outlet?a=CCL
# auth = HTTPBasicAuth('admin', '1234')
payload = """<Link version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
<MACAddress>24:0f:9b:ce:f1:5c</MACAddress>
<autoNegotiation>false</autoNegotiation>
<speed>100</speed>
<duplex>full</duplex>
<MTU>1500</MTU>
</Link>
"""
data = {'userName':'admin', 'password':'Birdseye123!'}
headers = {}
# data = {
#     'j_username': 'admin',
#     'j_password': '1234'
# }
#
# data2 = {
#     'value': 'true'
# }


# responses2 = requests.request('GET', webpower, auth=HTTPDigestAuth('admin', '1234'), headers=headers,
#                             data=payload, verify=False)
# x = requests.Session()
# print(x)
# headers2 = {
#     'X-CSRF':'x'
# }
# print(responses2.status_code)
# responses = requests.request('GET', streamstatus, auth=HTTPDigestAuth('admin', 'Birdseye123!'), headers=headers,
#                               data=payload, verify=False, timeout=10)
#
# print(responses.status_code, responses.text)
# Get XML
session = requests.Session()
r = session.post(login_page, headers=headers, data=data)
print(r.status_code, r.text)


# responses = requests.request('GET', login_page, auth=HTTPDigestAuth('admin', 'Birdseye123!'), headers=headers,
#                              data=data, verify=False, timeout=10)
#
# print(responses.status_code, responses.text)
# edit field
# a = responses.text.replace("<autoNegotiation>true</autoNegotiation>","<autoNegotiation>false</autoNegotiation>")
# b = a.replace("<speed>10</speed>","<speed>100</speed>")
# c = b.replace("<duplex>half</duplex>","<duplex>full</duplex>")
#
# # upload new xml and change the settings that you want
# editedpayload = c
# print(editedpayload)
# editing = requests.request('PUT', network_interface, auth=HTTPDigestAuth('admin', 'Birdseye123!'), headers=headers,
#                              data=editedpayload, verify=False, timeout=10)
# tree = ElementTree.fromstring(responses.content)
# for stuff in tree.findall('{*}Link'):
#     t = stuff.find('{*}speed')
#     t.insert(0,'100')
#     print(t)
#     w = stuff.find('{*}autoNegotiation')
#     w.insert(0,'true')
#     print(w)
# reset = requests.request('POST', webpower3r, headers=headers, data=data, verify=False)
#
# print("trying to reboot" + reset.text)
# Show XML Structure
# tree = ElementTree.fromstring(responses.content)


# Show Child elements in XML
# for child in tree:
#    print(child.tag, child.attrib)
# Print Data From Specific child element (fifth child elemnt and fifth fow from it)
# print(tree[4][4].text)

# find specific Data in specific row
# for Video in tree.findall('{*}Video'):
#     t = Video.find('{*}videoResolutionWidth')
#     print(t.text)


# Open original file
# et = xml.etree.ElementTree.parse('file.xml')

# Append new tag: <a x='1' y='abc'>body text</a>
# new_tag = xml.etree.ElementTree.SubElement(et.getroot(), 'a')
# new_tag.text = 'body text'
# new_tag.attrib['x'] = '1' # must be str; cannot be an int
# new_tag.attrib['y'] = 'abc'
#
# # Write back to file
# #et.write('file.xml')
# et.write('file_new.xml')