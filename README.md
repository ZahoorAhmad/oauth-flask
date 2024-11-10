# OAuth Integration with Flask

This repository provides a simple OAuth integration for various providers like **Google**, **GitHub**, **Microsoft**, **IBM**, **WC** and more using the **Flask** framework. The application allows users to authenticate via these providers and manage OAuth tokens efficiently.

The project also includes a Dockerized setup using **Docker Compose** with **Redis** for session management.

## Features

- OAuth authentication with multiple providers (Google, GitHub, Microsoft, etc.)
- Secure token management using OAuth 2.0
- User information retrieval after successful authentication
- Docker Compose setup for easy deployment and management

## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker** and **Docker Compose** for containerization
- Python 3.11 or higher (if running locally without Docker)

## Getting Started

### 1. Clone the repository

bash
git clone https://github.com/ZahoorAhmad/oauth-flask.git
cd oauth-flask


### 2. Setup environment variables

Create a .env file in the root of the project directory and add the following environment variables. These will be used by the Flask app for OAuth integration:

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:5000/callback/google
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration

WC_CLIENT_ID=your_wc_client_id
WC_CLIENT_SECRET=your_wc_client_secret
WC_REDIRECT_URI=http://localhost:5000/callback/wc
WC_DISCOVERY_URL=https://accounts.wanclouds.net/.well-known/openid-configuration


GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:5000/callback/github
GITHUB_DISCOVERY_URL=https://login.microsoftonline.com/common/.well-known/openid-configuration


MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_REDIRECT_URI=http://localhost:5000/callback/microsoft
MICROSOFT_DISCOVERY_URL=https://login.microsoftonline.com/common/.well-known/openid-configuration

IBM_CLIENT_ID=your_ibm_client_id
IBM_CLIENT_SECRET=your_ibm_client_secret
IBM_REDIRECT_URI=http://localhost:5000/callback/ibm
IBM_DISCOVERY_URL=https://iam.cloud.ibm.com/identity/.well-known/openid-configuration

SECRET_KEY=your_flask_secret_key
***NOTE*** = You can set all or any of the env at a time, depending on your requirements and you can skip SECRET_KEY if you don't want but recommended for security concern

### 3. Install dependencies

pip install -r requirements.txt


### 4. Running the application

docker-compose build -d --force-recreate


### Bonus: Running locally without Docker:

If you prefer to run the app directly on your local machine without Docker, simply run:

python app/app.py



This will start the Flask application on http://localhost:5000.
API Endpoints
1. Login via OAuth provider

Redirects to the OAuth provider's login page:

    Google: /login/google
    GitHub: /login/github
    Microsoft: /login/microsoft
    IBM: /login/ibm
    WC: /login/wc
    ............
    ............
    ............
    ABC: /login/abc

Example:

http://localhost:5000/login/google

After the user authenticates, they will be redirected to the callback URL you defined in the .env file.
2. OAuth Callback

Handles the callback from the OAuth provider, and exchanges the authorization code for an access token:

    Google: /callback/google
    GitHub: /callback/github
    Microsoft: /callback/microsoft
    IBM: /callback/ibm
    WC: /callback/wc
    ............
    ............
    ............
    ABC: /callback/abc

Example:

http://localhost:5000/callback/google?code=authorization_code

3. Get User Information

Fetches user information from the provider after authentication:

    Google: /user/google
    GitHub: /user/github
    Microsoft: /user/microsoft
    IBM: /user/ibm
    WC: /user/wc
    ............
    ............
    ............
    ABC: /user/abc


Example:

http://localhost:5000/user/google?access_token=your_access_token

Docker Setup

This project includes a Docker Compose configuration to run the Flask app and Redis. Follow these steps to set up the Docker containers:

    Build Docker images:

docker-compose build

Start the containers:

    docker-compose up

    This will start both the Flask application and Redis. The Flask app will be available at http://localhost:5000.

OAuth Providers

The project supports the following OAuth providers:

    Google
    GitHub
    Microsoft
    IBM
    WC

To add more providers, simply:

    Update the OAUTH_PROVIDERS dictionary in app/oauth.py with the provider's details.
    Add any provider-specific logic for token retrieval and user info if needed.

Session Management

Sessions are managed using Redis. When a user logs in via any OAuth provider, their session information is stored in Redis. This enables scalable, secure session management.
Redis Configuration

The application uses Redis to store session data. The default configuration assumes Redis is running locally on the default port 6379. This can be modified by changing the Redis URL in the .env file.
Troubleshooting

    If the application is not redirecting to the OAuth provider's login page, ensure that the redirect_uri in the .env file matches the callback URL defined in your OAuth provider's settings.
    If you encounter errors related to Redis, ensure that Redis is up and running, and the app can connect to it.
    Double-check your OAuth provider credentials (client ID, client secret, etc.) to ensure they're correct.

Contributing

If you'd like to contribute to this project, feel free to submit pull requests. Please make sure to:

    Follow Python and Flask best practices.
    Add tests for new features or bug fixes.
    Provide clear commit messages.
