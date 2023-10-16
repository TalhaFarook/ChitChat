# ChitChat
ChitChat is a chat messaging application powered by Django, designed to bring people together. With user-friendly controls, it enables users to exchange messages and images effortlessly. 

## Features

- **User Authentication**: Secure user registration and login system.
- **Private Messaging**: Send direct messages to other users.
- **Group Messaging**: Create groups, add members, and engage in group conversations.
- **Image Support**: Send and receive images along with text messages.
- **Message Status**: See message status (sent, delivered, read) for each message.
- **User Activity**: Display user activity status, including online and last active.

## Installation

1. Clone the repository to your local machine:
```sh
  git clone https://github.com/TalhaFarook/ChitChat
```

2. Install project dependencies:
```sh
    pip install -r requirements.txt
```

3. Apply database migrations:
```sh
    python manage.py migrate
```

4. Start the Django development server:
```sh
    python manage.py runserver
```

5. Access the application in your web browser at
```sh
    http://localhost:8000
```