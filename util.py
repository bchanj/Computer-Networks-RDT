# Brandon Chan
# Dr. Yang 
# CPSC 4510
# 5/3/2022
# util.py

# The first 8 bytes of every packet (simulate Source and Destination address) 
#   containing the value: "COMPNETW"
PACKET_START = "COMPNETW"

# Total number of bytes of packet without message/data
HEADER_LENGTH = 12 
BYTE_SIZE = 8
TWO_POWER_SIXTEEN = 65535


def normal_exchange_msg(packet):
    print("packet is expected, message string delivered: ", getMessage(packet))
    print("packet is delivered, now creating and sending the ACK packet...")


def getMessage(packet):
    return packet[12:].decode('utf-8')


def getAck(packet):
    byte_to_int = bin(int.from_bytes(packet, 'big', signed=False))[2:]
    return int(byte_to_int[94])


def getSeq(packet):
    byte_to_int = bin(int.from_bytes(packet, 'big', signed=False))[2:]
    return int(byte_to_int[95])


def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """

    # Split up packet into byte pairs    
    two_byte_sections = []
    for i in range(0, len(packet_wo_checksum), 2):
        if len(packet_wo_checksum)%2 == 1 and (i+1) >= len(packet_wo_checksum):
            two_byte_sections.append(packet_wo_checksum[i] << 8)
        else:
            byte = packet_wo_checksum[i]
            byte = byte << BYTE_SIZE
            byte2 = packet_wo_checksum[i+1]
            byte = byte | byte2
            two_byte_sections.append(byte)
    
    # Calculate sum of byte pairs
    sum = 0
    for pair in two_byte_sections:
        sum += pair

    # Deal with wraparound
    if sum > TWO_POWER_SIXTEEN:
        overflow = sum >> 16
        sum += overflow # Isolate the overflow
        to_subt = overflow << 16
        sum -= to_subt

    # Take ones complement of sum and return
    return (~sum + 2**16).to_bytes(2, byteorder='big')


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
    
    original_checksum = packet[8:10]
    packet_wo_checksum = packet[:8] + packet[10:]
    checksum = create_checksum(packet_wo_checksum)
    if checksum == original_checksum:
        return True
    return False
    

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # Indexes of 'byte_list'
    #   0: b'COMPNETW'
    #   1: Data (message)
    #   2: Length with ACK and SEQ
    #   3: Checksum
    byte_list = []

    # 1. Handle first 8 bytes of packet
    source_destination = bytearray(PACKET_START, 'utf-8') # A mutable byte string
    byte_list.append(source_destination)

    # 2. Add the message, "data_str"
    data = bytearray(data_str, 'utf-8')
    byte_list.append(data)

    # 3. Add length(14 bits), ACK(1 bit) and SEQ(1 bit) (16 bits or 2 bytes)
    length = HEADER_LENGTH + len(bytes(data_str, 'utf-8')) 

    # 3b. Shift bits to add ACK and SEQ
    length = length << 1
    length = length | seq_num
    length = length << 1
    length = length | ack_num
    byte_list.append((length).to_bytes(2, byteorder= 'big'))

    # 4. Create checksum and add it to the packet
    finished_byte_str = bytearray("", 'utf-8')
    finished_byte_str += byte_list[0] + byte_list[2] + byte_list[1]
    returned_checksum = create_checksum(bytearray(finished_byte_str))
    byte_list.append(returned_checksum)

    # 5. Recombine all the pieces of the packet and return finished packet
    packet = bytearray("", 'utf-8')
    packet += byte_list[0] + byte_list[3] + byte_list[2] + byte_list[1]
    return bytes(packet)


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should not make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
