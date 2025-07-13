from Comms import CommunicationInterface
from Notifs import MessageNotification

if __name__ == "__main__":
    # Create a communication interface
    comm_interface = CommunicationInterface()

    # Create message notification instances
    user1 = MessageNotification("User 1")
    user2 = MessageNotification("User 2")

    # Subscribe users to the communication interface
    comm_interface.subscribe(user1)
    comm_interface.subscribe(user2)

    # Simulate receiving a message
    comm_interface.receive_message("Hello, this is a test message!")
