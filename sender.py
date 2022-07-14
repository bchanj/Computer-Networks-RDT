# Brandon Chan
# Dr. Yang 
# CPSC 4510
# 5/3/2022
# sender.py


from socket import *
from util import *

PORT_NUMBER = 10214
TIMEOUT_WAIT = 15
SERVER_NAME = '127.0.0.1'


def corruption_message(msg, pkt_count):
    print("receiver acked the previous packet, resend\n")
    print("[ACK-Previous retransmission]: ", msg)
    print("packet num.", pkt_count, " is successfully sent to the receiver.")


def toggle_ackSeq(bit):
    return ((bit + 1) % 2)


class Sender:
  def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        self.ack_num = 0 # Necessary?
        self.seq_num = 0
        self.packet_count = 1


  def rdt_send(self, app_msg_str):
      """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
      # Create the packet to be sent
      packet = make_packet(app_msg_str, self.ack_num, self.seq_num)

      # Prepare socket and send packet
      print("Original message string: ", app_msg_str)
      sender_sock = socket(AF_INET, SOCK_DGRAM)
      sender_sock.settimeout(float(TIMEOUT_WAIT))
      print("packed created: ", packet)
      sender_sock.sendto(packet, (SERVER_NAME, PORT_NUMBER))
      print("packet num.", self.packet_count, " is successfully sent to the receiver.")

      try: # Try to see if there isn't a timeout, if there is, resend in except clause
          returned_pkt, receiver_addr = sender_sock.recvfrom(1024) # Get the ACK
          checksum_matched = verify_checksum(returned_pkt)
          new_ack = getAck(returned_pkt)

          done = False;
          while not done: # While we still need to resend
              if checksum_matched: # If packet is expected and everything works normally
                  if new_ack == self.ack_num:
                      print("packet is received correctly: seq. ", self.seq_num, " = ACK", self.ack_num, ". all done!\n")
                      done = True 
                  else: # For every 3rd packet to simulate corruption
                      self.packet_count += 1 
                      corruption_message(app_msg_str, self.packet_count)
                      
                      sender_sock.sendto(packet, (SERVER_NAME, PORT_NUMBER)) # Resend
                      returned_pkt, receiver_addr = sender_sock.recvfrom(1024)
                      new_ack = getAck(returned_pkt)
              else:
                  print("checksum error!")
                  
      except timeout: # For every 6th packet to simulate timeout
          # Resend packet
          self.packet_count += 1 
          new_ack = getAck(packet)
          print("socket timeout! Resend!")
          print("\n[timeout retransmission]: ", getMessage(packet))
          while(new_ack != self.ack_num):
              sender_sock.sendto(packet, (SERVER_NAME, PORT_NUMBER))
              returned_pkt, receiver_addr = sender_sock.recvfrom(1024) # Get the ACK
              new_ack = getAck(returned_pkt)
          print("packet is received correctly: seq. ", self.seq_num, " = ACK", self.ack_num, ". all done!")
          print("packet num.", self.packet_count, " is successfully sent to the receiver.\n")

      self.ack_num = toggle_ackSeq(self.ack_num)
      self.seq_num = toggle_ackSeq(self.seq_num)
      self.packet_count += 1 
      sender_sock.close()

      
            

  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT Change the function name.                    #######                    
  ####### You can have other functions as needed.                             #######   

