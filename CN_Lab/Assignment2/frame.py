import checksum
class Frame:
    def __init__(self, src, dst, payload, length, frame_no):
        self.src = src
        self.dst = dst
        self.payload = payload #binary string
        self.length = length
        self.frame_no = frame_no
    def __mac_to_binary__(self, mac):
        try:
            return ''.join(format(int(x, 16), '08b') for x in mac.split(':'))
        except:
            raise ValueError("Invalid MAC address")
    def frame_to_binary(self):
        src = self.__mac_to_binary__(self.src) #8 bits src mac
        dst = self.__mac_to_binary__(self.dst) #8 bits dst mac
        length = format(self.length, '016b') #16 bits length (2 bytes)
        frame_no = format(self.frame_no, '08b') #8 bits frame number (1 byte)
        header = src + dst + length + frame_no
        trailor = checksum.generate_checksum_codeword(header + self.payload) #32 bits checksum of header + payload
        return header + self.payload + trailor
        
    
    def __str__(self):
        return f"Frame {self.frame_no}: {self.src} -> {self.dst}, {self.length} bytes"
    
    