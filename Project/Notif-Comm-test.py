from Project import Comms, Notifs


if __name__ == "__main__":
    # Create a communication interface
    comm_interface = Comms()

    # Create message notification instances
    user1 = Notifs.MessageNotification("User 1")
    user2 = Notifs.MessageNotification("User 2")

    # Subscribe users to the communication interface
    comm_interface.subscribe(user1)
    comm_interface.subscribe(user2)

    # Simulate receiving a message
    comm_interface.receive_message("Hello, this is a test message!")
