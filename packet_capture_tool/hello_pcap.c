#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <time.h>
#include <net/ethernet.h>

int main() {
    char *device_name;
    char error[PCAP_ERRBUF_SIZE];
    pcap_t* pack_desc;
    const u_char *packet;
    pcap_if_t *interfaces, *temp;
    struct pcap_pkthdr header;
    struct ether_header *eptr;
    int i = 1;

    device_name = pcap_lookupdev(error);
    if (device_name == NULL) {
        printf("%s\n", error);
        return -1;
    } else {
        printf("Device: %s\n", device_name);
    }

    pack_desc = pcap_open_live(device_name, BUFSIZ, 0, 1, error);
    if (pack_desc == NULL) {
        printf("%s\n", error);
        return -1;
    }

    packet = pcap_next(pack_desc, &header);
    if (packet == NULL) {
        printf("Error: Cannot capture packet\n");
        return -1;
    } else {
        printf("Received a packet with length: %d\n", header.len);
        printf("Received at %s\n", ctime((const time_t*) &header.ts.tv_sec));
        printf("Ethernet Address Constant Length: %d\n", ETHER_HDR_LEN);

        eptr = (struct ether_header*)packet;

        if (ntohs(eptr->ether_type) == ETHERTYPE_IP) {
            printf("Ethernet type hex: %x; dec: %d is an IP Packet", ETHERTYPE_IP, ETHERTYPE_IP);
        } else if (ntohs(eptr->ether_type) == ETHERTYPE_ARP) {
            printf("Ethernet type hex: %x; dec: %d is an IP Packet", ETHERTYPE_ARP, ETHERTYPE_ARP);
        } else {
            printf("Ethernet type hex: %x; dec: %d is an IP Packet", ntohs(eptr->ether_type), ntohs(eptr->ether_type));
            return -1;
        }
    }
    return 0;
}