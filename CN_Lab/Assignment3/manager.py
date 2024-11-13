import random

class Node:
    def __init__(self, node_id, p=0.1):
        self.node_id = node_id
        self.p = p  # Transmission probability in p-persistent CSMA/CD
        self.state = "idle"  # Possible states: idle, transmitting, collided, backoff
        self.backoff_time = 0  # Time node waits after collision
        self.bytes_to_send = 0  # Number of bytes the node wants to send
        self.transmission_time_left = 0  # Time slots remaining for the current transmission

    def attempt_transmission(self, channel, force_send=False):
        """Attempt to send data with p-persistent strategy or based on user input."""
        if self.state == "idle":
            if force_send or (channel.is_free() and random.random() < self.p):
                if channel.is_free():
                    self.state = "transmitting"
                    channel.transmitting_nodes.append(self.node_id)
                else:
                    self.state = "collided"
            else:
                self.state = "idle"

    def handle_collision(self, total_time):
        """Handles collision by setting the node to backoff state with random time."""
        self.state = "backoff"
        self.backoff_time = random.randint(1, total_time - 1)

    def decrement_backoff(self):
        """Decrements the backoff time and sets state to idle when backoff is done."""
        if self.backoff_time > 0:
            self.backoff_time -= 1
        if self.backoff_time == 0:
            self.state = "idle"  # Ready to retry after backoff

    def start_transmission(self, bytes_to_send):
        """Set the node to start sending data and calculate transmission time."""
        self.bytes_to_send = bytes_to_send
        self.transmission_time_left = (bytes_to_send + 9) // 10  # Round up to nearest time slot for byte count

    def continue_transmission(self):
        """Continue sending if there are bytes left to transmit."""
        if self.transmission_time_left > 0:
            self.transmission_time_left -= 1
        if self.transmission_time_left == 0:
            self.state = "idle"  # Transmission is complete


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

            
            if not self.channel.is_free():
                print("Channel is busy due to an ongoing transmission.")
                continue
            chosen_nodes = input("Enter node IDs to attempt transmission (comma separated), or leave blank for random: ")
            bytes_input = input("Enter the number of bytes to send for each node (comma separated): ")
            
            if chosen_nodes and bytes_input:
                chosen_nodes = [int(n.strip()) for n in chosen_nodes.split(",")]
                bytes_to_send = [int(b.strip()) for b in bytes_input.split(",")]
            else:
                chosen_nodes = []
                bytes_to_send = []

            # Handle busy channel due to ongoing transmission
            self.channel.decrement_busy_time()
            else:
                # Retry nodes that are out of backoff
                for node in self.nodes:
                    if node.state == "idle" and node.backoff_time == 0:
                        node.attempt_transmission(self.channel)

                # Force chosen nodes to transmit simultaneously
                for idx, node_id in enumerate(chosen_nodes):
                    node = self.nodes[node_id]
                    if node.state == "idle":
                        node.start_transmission(bytes_to_send[idx])
                        node.attempt_transmission(self.channel, force_send=True)

            # Detect collisions
            if self.channel.detect_collisions():
                self.collisions += 1
                print(f"Collision detected between nodes: {self.channel.transmitting_nodes}")
                for node_id in self.channel.transmitting_nodes:
                    self.nodes[node_id].handle_collision(self.total_time)
                self.channel.clear()  # Clear the channel after handling collision
            elif len(self.channel.transmitting_nodes) == 1:
                # Successful transmission
                transmitting_node = self.nodes[self.channel.transmitting_nodes[0]]
                if transmitting_node.transmission_time_left > 0:
                    print(f"Node {self.channel.transmitting_nodes[0]} is transmitting {transmitting_node.bytes_to_send} bytes.")
                    self.channel.set_busy(transmitting_node.transmission_time_left)
                    transmitting_node.continue_transmission()
                else:
                    self.successful_transmissions += 1
                    print(f"Node {self.channel.transmitting_nodes[0]} successfully transmitted.")
                    self.channel.clear()  # Clear after successful transmission
                    transmitting_node.state = "idle"

            # Handle backoff for nodes in collision
            for node in self.nodes:
                if node.state == "backoff":
                    node.decrement_backoff()
                    if node.backoff_time == 0:
                        print(f"Node {node.node_id} is out of backoff and ready to retry.")

            # We no longer clear the channel unconditionally at the end of each time step
            # The channel will be cleared only after successful transmissions or collisions

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    p = float(input("Enter the p-persistence value (0 < p <= 1): "))
    total_time = int(input("Enter the total simulation time: "))
    
    sim = SimulationManager(num_nodes=num_nodes, p=p, total_time=total_time)
    sim.run_simulation()
