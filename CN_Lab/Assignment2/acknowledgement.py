class ACK:
    def __init__(self, seq_num):
        self.seq_num = seq_num
            
    def __str__(self):
        return f"ACK#{self.seq_num}"
    def get_ack_no(ack: str):
        return int(ack.split("#")[1])
class NAK:
    def __init__(self, seq_num):
        self.seq_num = seq_num
            
    def __str__(self):
        return f"NAK#{self.seq_num}"