import paramiko
import json
import requests
from requests.auth import HTTPDigestAuth
from xml.etree import ElementTree
import os
import time
# import subprocess
from datetime import datetime
# import ipaddress
from pandas import *
# import netmiko
from multiprocessing import Pool
import multiprocessing

ipstart = ['10.20.48.9']
# import range from file in root location
data = read_csv("ip.csv")
# use ROW 1 with the title ip lowercased!

addresses = data['ip'].tolist()

# global scan
# scan = []
#
# for addr in ipaddress.IPv4Network('10.20.49.0/24'):
#     scan.append(str(addr))
user = "admin"
passwd = ["Birdseye123!", "bsi12345", "nepostoji"]
correct_passwd = ""
# device info start
b = ""
c = ""
d = ""
e = ""
f = ""
# device info end
# device stream start
g = ""
h = ""
# device stream end
# device network start
z = ""
x = ""
u = ""
v = ""
q = ""
y = ""
# device network end
starttime = time.time()
"""Format vremena za current_time"""
date_format = 'Year %Y Month %m Day %d Hour %H Minutes %M Seconds %S'
"""Za windows OS da nadje %USERNAME% i da sacuva fajl pod nazivom ping.txt"""
file_path = os.path.join(os.path.expanduser('~'), 'inventory.csv')

"""Da zapise trenutno sistemsko vreme"""
current_time = (datetime.now().strftime(date_format))
# print(ip)
try:
    f = open(file_path, 'r')
except IOError:
    f = open(file_path, 'w')
    f.write("Device Name,Device model,Device mac,Device serial #,firmware,resolution, encoding,"
            "IP address,Static/Dynamic,Default Gateway, Adapter Speed, Speed Auto Negotiation, Duplex Date\n")
    f.close()
finally:
    f.close()
use = ["IPproTech", "admin", "admin"]
pas = ["Birdseye123!", "bsi12345", "Nepostoji!"]
us = ""
pa = ""

count = 0
print(str(count) + " Original")


def user_password_finder(username, password, addr):
    for ussr in username:
        for p in password:
            try:
                global count
                count += 1
                print("Number of Tries " + str(count))
                global us
                global pa
                payload = {}
                headers = {}
                response_device_info = requests.request('GET', f"https://{addr}/ISAPI/System/deviceinfo",
                                                        auth=HTTPDigestAuth(ussr, p), headers=headers, data=payload,
                                                        verify=False, timeout=10)
                print("trying to connect via " + ussr + "" + p)
                print(response_device_info.status_code)
                print(response_device_info.text)
                if response_device_info.status_code == 200:
                    us = ussr
                    pa = p
                    print("successfully logged in with Username " + us + " and password " + pa)
                if count == 4:
                    time.sleep(300)
                    count = 0
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError):
                pass


# start password generator
# for _ in ipstart:
#     user_password_finder(use, pas, _)
def ssh_connect():
    hostname = "10.4.8.2"
    port = 22
    username = "ubnt"
    password = "Birdseye123!"
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        transport = client.get_transport()
        channel = transport.open_session()
        channel.get_pty()
        channel.invoke_shell()
        #time delayi n between commands
        t = 2
        time.sleep(t)
        print('pt1')
        channel.send("show version\n")
        time.sleep(t)
        x = channel.recv(65535).decode()
        x.splitlines()
        # replace the values with , (comma)
        x = x.replace("System Description............................. ", "")
        # replace the values with , (comma)
        x = x.replace("Machine Type................................... ", "")
        # replace the values with , (comma)
        x = x.replace("Serial Number.................................. ", "")
        # replace the values with , (comma)
        x = x.replace("Part Number.................................... ", "")
        # replace the values with , (comma)
        x = x.replace("Burned In MAC Address.......................... ", "")
        # replace the values with , (comma)
        x = x.replace("Software Version............................... ", "")
        # replace the values with , (comma)
        x = x.replace("Machine Model.................................. ", "")
        # replace the values with , (comma)
        x = x.replace("Hardware Revision.............................. ", "")
        print(x)

        print("original" + channel.recv(65535).decode())
        # Send enable command and get info
        # time.sleep(t)
        # print('pt1')
        # channel.send("enable\n")
        # time.sleep(t)
        # print(channel.recv(65535).decode())
        # time.sleep(t)
        # channel.send("Birdseye123!\n")
        # print('pt2')
        # time.sleep(t)
        # print(channel.recv(65535).decode())
        # time.sleep(t)
        # channel.send("show interface ethernet all\n")
        # time.sleep(t)
        # print(channel.recv(65535).decode())

        client.close()
    except Exception as err:
        print(err)



ssh_connect()


# Print Show mikrotik IP addresses that are assigned to different interfaces
def mikrotik_api(address, usr, pa):
    payload = {
        "Content-Type": "application/json",
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.request('GET', f"https://{address}/rest/ip/address",
                                    headers=headers, auth=(usr, pa),
                                    data=payload, verify=False, timeout=10)
        data = json.loads(json.dumps(response.json()))
        for d in data:
            stuff_addr = d['actual-interface']
            stuff_ip = d['address']
            print(stuff_addr)
            print(stuff_ip)

        # print(response.raise_for_status())
        # print(response.content)
        # print(data)
    #           print(json.loads(json.dumps(data)))
    except Exception as err:
        print(err)


# mikrotik_api("10.10.10.1", "admin", "Wishmaster91")
# ubiquiti_connect()


# example
# def get_cdp_neighbor_details(ip, username, password, enable_secret):
#     """
#     get the CDP neighbor detail from the given device using SSH
#
#     :param ip: IP address of the device
#     :param username: username used for the authentication
#     :param password: password used for the authentication
#     :param enable_secret: enable secret
#     :return:
#     """
#     # establish a connection to the device
#     ssh_connection = ConnectHandler(
#         device_type='cisco_ios',
#         ip=ip,
#         username=username,
#         password=password,
#         secret=enable_secret
#     )
#
#     # enter enable mode
#     ssh_connection.enable()
#
#     # prepend the command prompt to the result (used to identify the local host)
#     result = ssh_connection.find_prompt() + "\n"
#
#     # execute the show cdp neighbor detail command
#     # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
#     result += ssh_connection.send_command("show cdp neighbor detail", delay_factor=2)
#
#     # close SSH connection
#     ssh_connection.disconnect()
#
#     return result

def mikrotik(camera_ip):
    mikrotik_file_path = os.path.join(os.path.expanduser('~'), 'mikrotik_script.csv')
    try:
        f = open(mikrotik_file_path, 'r')
    except IOError:
        f = open(mikrotik_file_path, 'w')
        f.write("Terminal Script,\n")
        f.close()
    finally:
        f.close()

    camera_name = camera_ip
    d_pt1 = r"""/tool fetch http-method=post http-header-field=\"Content-type: application/json\" http-data=\"{\\\"text\\\":\\\"Camera """
    d_pt2 = r""" not responding to TCP query\\\"}\" url="""
    #  format is \\\"https://hooks.slack.com/services/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\\\"
    url = r'https://hooks.slack.com/services/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'

    down_script = d_pt1 + camera_name + d_pt2 + url
    u_pt1 = r"""/tool fetch http-method=post http-header-field=\"Content-type: application/json\" http-data=\"{\\\"text\\\":\\\"Camera """
    u_pt2 = r""" restored normal functionality\\\"}\" url="""
    #  format is "https://hooks.slack.com/services/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"
    up_script = u_pt1 + camera_name + u_pt2 + url
    webhook1 = f"""/tool netwatch add disabled=no down-script="{down_script}" host="{camera_ip}" http-codes="" interval=30s port=80 test-script="" type=http-get up-script="{up_script}"
"""
    print(d_pt1)
    with open(mikrotik_file_path, 'a') as file:
        file.write(webhook1 + "," + "\n")
        file.flush()


# for i in addresses:
#     mikrotik(i)


#  ("10.1.20.200")


def device_info(address, username, password):
    for x in password:
        print("Getting data from " + address)
        payload = {}
        headers = {}
        try:
            response_device_info = requests.request('GET', f"https://{address}/ISAPI/System/deviceinfo",
                                                    auth=HTTPDigestAuth(username, x), headers=headers, data=payload,
                                                    verify=False, timeout=10)
            #        print(response_device_info.raise_for_status())
            # print(str("trying password " + x))
            global correct_passwd
            global b
            global c
            global d
            global e
            global f
            if response_device_info.status_code == 200:
                correct_passwd = x
                tree = ElementTree.fromstring(response_device_info.content)
                for stuff in tree.findall('{*}deviceName'):
                    b = str(stuff.text)
                    print("device name is " + b)
                for stuff in tree.findall('{*}model'):
                    c = str(stuff.text)
                    print("device model is " + stuff.text)
                for stuff in tree.findall('{*}macAddress'):
                    d = str(stuff.text)
                    print("device mac " + stuff.text)
                for stuff in tree.findall('{*}serialNumber'):
                    e = str(stuff.text)
                    print("device serial # " + stuff.text)
                for stuff in tree.findall('{*}firmwareVersion'):
                    f = str(stuff.text)
                    print("device is running on firmware " + stuff.text)
                    print(str("Password is : " + correct_passwd))
                #                     with open(file_path, 'a') as file:
                #                         file.write(b + "," + c + "," + d + "," + e + "," + f + ",")
                #                         file.flush()
                break

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError):
            try:
                print('Trying HTTP call for device_info ')
                response_device_info = requests.request('GET', f"http://{address}/ISAPI/System/deviceinfo",
                                                        auth=HTTPDigestAuth(username, x), headers=headers, data=payload,
                                                        verify=False, timeout=10)
                print(response_device_info.text)
                if response_device_info.status_code == 200:
                    correct_passwd = x
                    tree = ElementTree.fromstring(response_device_info.content)
                    for stuff in tree.findall('{*}deviceName'):
                        b = str(stuff.text)
                        print("device name is " + b)
                    for stuff in tree.findall('{*}model'):
                        c = str(stuff.text)
                        print("device model is " + stuff.text)
                    for stuff in tree.findall('{*}macAddress'):
                        d = str(stuff.text)
                        print("device mac " + stuff.text)
                    for stuff in tree.findall('{*}serialNumber'):
                        e = str(stuff.text)
                        print("device serial # " + stuff.text)
                    for stuff in tree.findall('{*}firmwareVersion'):
                        f = str(stuff.text)
                        print("device is running on firmware " + stuff.text)
                        print(str("Password is : " + correct_passwd))
                    #                     with open(file_path, 'a') as file:
                    #                         file.write(b + "," + c + "," + d + "," + e + "," + f + ",")
                    #                         file.flush()
                    break
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError,
                    requests.exceptions.HTTPError):
                pass


def device_stream(address, username):
    payload = {}
    headers = {}
    try:
        response_video_stream = requests.request('GET', f"https://{address}/ISAPI/Streaming/channels/101",
                                                 auth=HTTPDigestAuth(username, correct_passwd), headers=headers,
                                                 data=payload, verify=False, timeout=10)
        #    print(response_video_stream.raise_for_status())
        print(str("using password saved in " + correct_passwd))
        global g
        global h
        if response_video_stream.status_code == 200:

            tree = ElementTree.fromstring(response_video_stream.content)
            for stuff in tree.findall('{*}Video'):
                w = stuff.find('{*}videoResolutionWidth')
                h = stuff.find('{*}videoResolutionHeight')
                g = str((w.text + " x " + h.text))
                print(str("Video resolution is " + w.text + " x " + h.text))
            for stuff in tree.findall('{*}Video'):
                t = stuff.find('{*}videoCodecType')
                h = str(t.text)
                print(str("Camera is using encoding " + t.text))
                #                 with open(file_path, 'a') as file:
                #                     file.write(g + "," + h + ",")
                #                     file.flush()
                break

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError,
            requests.exceptions.HTTPError):
        try:
            print("Trying HTTP call for device_streaming")
            response_video_stream = requests.request('GET', f"http://{address}/ISAPI/Streaming/channels/101",
                                                     auth=HTTPDigestAuth(username, correct_passwd), headers=headers,
                                                     data=payload, verify=False, timeout=10)
            #    print(response_video_stream.raise_for_status())
            print(response_video_stream.status_code)
            if response_video_stream.status_code == 200:
                tree = ElementTree.fromstring(response_video_stream.content)
                for stuff in tree.findall('{*}Video'):
                    w = stuff.find('{*}videoResolutionWidth')
                    h = stuff.find('{*}videoResolutionHeight')
                    g = str((w.text + " x " + h.text))
                #                print(str("Video resolution is " + w.text + " x " + h.text))
                for stuff in tree.findall('{*}Video'):
                    t = stuff.find('{*}videoCodecType')
                    h = str(t.text)
                    print(str("Camera is using encoding " + t.text))
                    break
                    # with open(file_path, 'a') as file:
                    #     file.write(g + "," + h + ",")
                    #     file.flush()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError,
                requests.exceptions.HTTPError):
            pass


def device_network(address, username):
    payload = {}
    headers = {}
    try:
        response_network = requests.request('GET', f"https://{address}/ISAPI/System/Network/interfaces/1/capabilities",
                                            auth=HTTPDigestAuth(username, "Birdseye123!"), headers=headers,
                                            data=payload, verify=False, timeout=10)
        #        print(str("using password saved in " + correct_passwd))
        #        print(response_network.status_code)
        #       print(response_network.text)
        global z
        global x
        global u
        global v
        global q
        global y

        print(response_network.text)
        if response_network.status_code == 200:

            tree = ElementTree.fromstring(response_network.content)
            for stuff in tree.findall('{*}IPAddress'):
                t = stuff.find('{*}ipAddress')
                w = stuff.find('{*}addressingType')
                z = str(t.text)
                x = str(w.text)
            #                print(str("Camera is using a " + t.text + " IP " + w.text))
            for stuff in tree.findall('{*}IPAddress'):
                t = stuff.find('{*}DefaultGateway')
                w = t.find('{*}ipAddress')
                u = str(w.text)
            #                print(str("Camera is using IPv4 gateway " + w.text))
            for stuff in tree.findall('{*}Link'):
                t = stuff.find('{*}speed')
                w = stuff.find('{*}autoNegotiation')
                v = str(t.text)
                q = str(w.text)
            #                print(
            #                    str("Network adapter is operating on " + t.text + " mbps," + "
            #                    auto negotiation is set to "
            #                        + w.text))
            for stuff in tree.findall('{*}Link'):
                t = stuff.find('{*}duplex')
                y = str(t.text)
                break

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError,
            requests.exceptions.HTTPError):
        try:
            response_network = requests.request('GET',
                                                f"http://{address}/ISAPI/System/Network/interfaces/1/capabilities",
                                                auth=HTTPDigestAuth(username, "Birdseye123!"), headers=headers,
                                                data=payload, verify=False, timeout=10)
            if response_network.status_code == 200:

                tree = ElementTree.fromstring(response_network.content)
                for stuff in tree.findall('{*}IPAddress'):
                    t = stuff.find('{*}ipAddress')
                    w = stuff.find('{*}addressingType')
                    z = str(t.text)
                    x = str(w.text)
                #                print(str("Camera is using a " + t.text + " IP " + w.text))
                for stuff in tree.findall('{*}IPAddress'):
                    t = stuff.find('{*}DefaultGateway')
                    w = t.find('{*}ipAddress')
                    u = str(w.text)
                #                print(str("Camera is using IPv4 gateway " + w.text))
                for stuff in tree.findall('{*}Link'):
                    t = stuff.find('{*}speed')
                    w = stuff.find('{*}autoNegotiation')
                    v = str(t.text)
                    q = str(w.text)
                for stuff in tree.findall('{*}Link'):
                    t = stuff.find('{*}duplex')
                    y = str(t.text)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, TypeError,
                requests.exceptions.HTTPError):
            pass


def write_data():
    with open(file_path, 'a') as file:
        file.write(b + "," + c + "," + d + "," + e + "," + f + "," + g + "," + h + "," + z + "," + x + "," + u + "," +
                   v + "," + q + "," + y + "\n")
        file.flush()
        file.close()


def inventory(addr):
    for a in addr:
        device_info(a, user, passwd)
        device_stream(a, user)
        device_network(a, user)
        write_data()

# inventory(ipstart)
# device_network(ipstart, user)
# inventory(addresses)
