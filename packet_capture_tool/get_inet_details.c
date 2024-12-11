#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    char *device_name, *net_addr, *net_mask;
    int rcode;
    char *error[PCAP_ERRBUF_SIZE];

    bpf_u_int32 net_addr_inet, net_mask_inet;
    struct in_addr addr;

    device_name = pcap_lookupdev(error);
    if(device_name == NULL) {
        printf("%s\n", error);
        return -1;
    } else {
        printf("Device: %s\n", device_name);
    }

    rcode = pcap_lookupnet(device_name, &net_addr_inet, &net_mask_inet, error);
    if(rcode == -1) {
        printf("%s\n", error);
        return -1;
    }

    addr.s_addr = net_addr_inet;
    net_addr = inet_ntoa(addr);

    if(net_addr == NULL) {
        printf("inet_ntoa: Error converting IP\n");
        return -1;
    } else {
        printf("Net: %s\n", net_addr);
    }

    return 0;
}