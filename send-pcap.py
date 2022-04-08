from scapy.all import *
global src_ip, dst_ip
src_ip = "192.168.10.149"
dst_ip = "192.168.10.148" # change to local IP of your computer
infile = "/Downloads/f1pc.pcap"


def my_send(rd, count=40000):
    pkt_cnt = 0
    p_out = []

    for p in rd:
        pkt_cnt += 1
        np = p.payload
        #clearprint(np)
        #if hasattr(np, 'IP'):
        print(pkt_cnt)
        if np.haslayer(IP) == 1 :
            np[IP].dst = dst_ip
            np[IP].src = src_ip
            del np[IP].chksum
                #p_out.append(np)
            send(np)
                #p_out = []

    # Send remaining in final batch
    #send(PacketList(p_out))
    print ("Total packets sent",pkt_cnt)

try:
    my_reader = PcapReader(infile)
    my_send(my_reader)
except IOError:
    print ("Failed reading  contents", infile)
    sys.exit(1)