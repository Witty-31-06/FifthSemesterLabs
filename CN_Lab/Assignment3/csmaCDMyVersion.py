import random

class Node:
    pass


class Channel:
    def __init__(self):
        self.transmitting_nodes = []
        self.busy_time_left = 0  # Time slots remaining during which the channel is busy

    def is_free(self):
        """Check if the channel is free (no node transmitting)."""
        return len(self.transmitting_nodes) == 0 and self.busy_time_left == 0

    def detect_collisions(self):
        """Detect if there's a collision (more than one node transmitting)."""
        return len(self.transmitting_nodes) > 1

    def set_busy(self, transmission_time):
        """Set the channel as busy for a certain number of time slots."""
        self.busy_time_left = transmission_time

    def decrement_busy_time(self):
        """Decrement the busy time if the channel is currently busy."""
        if self.busy_time_left > 0:
            self.busy_time_left -= 1

    def clear(self):
        """Clears the list of transmitting nodes (after a successful transmission or collision)."""
        self.transmitting_nodes = []

class SimulationManager:
    def __init__(self, num_nodes=5, p=1, total_time=100):
        self.nodes = [Node(i, p) for i in range(num_nodes)]
        self.channel = Channel()
        self.total_time = total_time
        self.successful_transmissions = 0
        self.collisions = 0
    
    def run_simulation(self):
        for time_step in range(self.total_time):
            print(f"\n--- Time Step {time_step} ---")

            chosen_nodes = input("Enter node IDs to attempt transmission (comma separated), or leave blank for random: ")
            bytes_input = input("Enter the number of bytes to send for each node (comma separated): ")
            if chosen_nodes and bytes_input:
                chosen_nodes = [int(n.strip()) for n in chosen_nodes.split(",")]
                bytes_to_send = [int(b.strip()) for b in bytes_input.split(",")]
            else:
                chosen_nodes = []
                bytes_to_send = []
            if len(chosen_nodes) > 1:
                print(f"Frames by sender nodes: {chosen_nodes} collided....")
                print("Backing Off....")
                continue

            self.channel.decrement_busy_time()
            if not self.channel.is_free():
                print("Channel is busy due to an ongoing transmission.")
                continue
            