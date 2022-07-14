# Brandon Chan
# Dr. Yang 
# CPSC 4510
# 5/3/2022
# receiver.py

from socket import *
from time import sleep
from util import *

PORT_NUMBER = 10214
TIMEOUT_WAIT = 15
ADDRESS = "127.0.0.1"
TIMEOUT_CASE = 6
CORRUPTION_CASE = 3

packet_count = 1
ack_num = 0
seq_num = 0
recv_socket = socket(AF_INET, SOCK_DGRAM)
recv_socket.bind(('', PORT_NUMBER))

print("********** READY TO SERVE **********\n")
while True:
    
    if packet_count % TIMEOUT_CASE == 0: # Simulate timeout (%6)
        pkt, client_addr = recv_socket.recvfrom(1024)
        print("packet num.", packet_count, "received: ", pkt)
        ack_num = getAck(pkt)
        seq_num = getSeq(pkt)

        print("TIMEOUT: simulating packet loss: sleep a while to trigger timeout event on the send side...")
        sleep(TIMEOUT_WAIT)

        while (getAck(pkt) != ack_num):
            pkt, client_addr = recv_socket.recvfrom(1024) # Received retransmitted packet
        ack_pack = make_packet(getMessage(pkt), ack_num, seq_num)
        recv_socket.sendto(ack_pack, client_addr)
        
    elif packet_count % CORRUPTION_CASE == 0: # Simulate corruption (%3)
        pkt, client_addr = recv_socket.recvfrom(1024)
        print("packet num.", packet_count, "received: ", pkt)
        ack_num = getAck(pkt)
        seq_num = getSeq(pkt)
        print("CORRUPT: simulating packet bit errors/corrupted: ACK the previous packet!")
        bad_ack = make_packet(getMessage(pkt), (ack_num+1) % 2, (seq_num + 1) % 2)
        recv_socket.sendto(bad_ack, client_addr)
        while getAck(bad_ack) == getAck(pkt):
            pkt, client_addr = recv_socket.recvfrom(1024) # Receive retransmitted packet

    else: # Simulate correct packet transfer
        pkt, client_addr = recv_socket.recvfrom(1024)
        print("packet num.", packet_count, "received: ", pkt)
        ack_num = getAck(pkt)
        seq_num = getSeq(pkt)
        normal_exchange_msg(pkt)
        ack_pack = make_packet(getMessage(pkt), ack_num, seq_num) # Create a packet with the new ack
        recv_socket.sendto(ack_pack, client_addr) # SEND ACK BACK
    
    print("all done for this packet!\n")
    packet_count +=1



