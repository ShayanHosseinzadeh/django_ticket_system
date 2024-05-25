# Ticket System

Welcome to the Ticket System project! This is a Django-based web application designed to facilitate ticket management. The system allows users to create tickets, support staff to manage them, and admins to have full control over the tickets. Additionally, it features a chat theme in the ticket details for seamless communication.

## Features

1. **Ticket Creation**: Users can create new tickets.
2. **Support Management**: Support staff can take open tickets and close pending ones.
3. **Admin Control**: Admins have full control over the tickets, including the ability to delete and close them.
4. **Ownership Restriction**: Users cannot accept their own tickets.
5. **Chat Theme**: Ticket details include a chat interface for communication.

## Technologies Used

- **Django**: The web framework used to build the application.
- **django-allauth**: For authentication and user management.
- **Bootstrap**: For responsive and modern user interface design.

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

Ensure you have the following installed:

- Python (3.11)
- Django
- virtualenv

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/ShayanHosseinzadeh/django_ticket_system.git
    cd django_ticket_system

    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

7. **Access the application**:

    Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

### User Roles

- **Users**: Can create tickets and view their status.
- **Support Staff**: Can take and close tickets but cannot accept their own tickets.
- **Admins**: Have full control over all tickets, including the ability to delete and close them.

### Creating Tickets

1. Log in to the application.
2. Navigate to the "Create Ticket" section.
3. Fill in the required details and submit the form.

### Managing Tickets (Support Staff)

1. Log in as a support staff member.
2. Go to the "Open Tickets" section.
3. Select a ticket to take it.
4. Communicate with the user through the chat interface if needed.
5. Close the ticket once the issue is resolved.

### Admin Controls

1. Log in as an admin.
2. Access the admin dashboard.
3. Manage tickets by deleting or closing them as necessary.



## Contact

For any inquiries or support, please contact [shayanhosseinzadeh1@gmail.com].

Thank you for using the Ticket System! We hope it helps streamline your ticket management process.
