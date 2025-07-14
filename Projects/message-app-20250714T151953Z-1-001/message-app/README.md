# message-app

This project is a messaging application built using Flet, designed to facilitate real-time communication between users. The application allows users to send and receive messages, as well as manage notifications related to their messaging activities.

## Project Structure

- **Messages-flet-app.py**: The main entry point for the Flet application. It initializes the app, sets up the user interface, and handles user interactions for sending and receiving messages.
  
- **Notifs.py**: Contains the `Notification` class that manages notification properties such as title, message, and timestamp. It includes methods for displaying notifications to the user.

- **communicative_messages.py**: Defines the `CommunicativeMessage` class, which includes properties for sender and receiver, as well as methods for formatting messages. This class allows for the creation and management of messages exchanged between users.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd message-app
   ```

3. Install the required dependencies:
   ```
   pip install flet
   ```

## Usage Guidelines

To run the application, execute the following command:
```
python Messages-flet-app.py
```

Once the application is running, users can interact with the interface to send and receive messages. Notifications will be displayed for new messages and other relevant events.

## Features

- Send and receive messages in real-time.
- Manage notifications for incoming messages.
- User-friendly interface built with Flet.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.