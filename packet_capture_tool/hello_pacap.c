#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    char *device_name;
    char error[PCAP_ERRBUF_SIZE];
    pcap_t* pack_desc;
}