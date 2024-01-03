
# MFA-implementation

This project demonstrates a secure login system between a client and a server, incorporating Time-Based One-Time Password (TOTP) verification and the Diffie-Hellman key exchange protocol.

## Table of Contents

- [Introduction](#introduction)
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

MFA-implementation is a project aimed at enhancing the security of user authentication by implementing Multi-Factor Authentication. It provides an additional layer of security by requiring users to provide multiple forms of identification.

## Overview

The authentication process involves the following steps:

1. **Diffie-Hellman Key Exchange:**
   - The server and client establish a shared secret key using the Diffie-Hellman key exchange protocol.
   - A random key is generated on the server and shared securely with the client.

2. **TOTP Verification:**
   - After establishing the shared secret key, the client generates a Time-Based One-Time Password (TOTP) using the shared secret and a timestamp.
   - The server validates the received TOTP against its own calculation to verify the client's identity.

3. **Key Recycling:**
   - The secret key used for communication is recycled for a time period every session, enhancing security.

## Project Structure
- **client.py**                  # Client-side implementation
- **server.py**                  # Server-side implementation
- **prime.py**                   # For generating P and G
- **users.json**                 # For keeping track of users on the server
## Installation

To install and run this project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/MFA-implementation.git`
2. Install the dependencies
3. Start the server
4. Start the client
5. Observe how the key exchange and verification happens 
## Usage

Once the application is running, users can access the MFA-implementation by visiting the provided URL. They will be prompted to provide their username, password, and an additional factor of authentication (such as a verification code sent to their mobile device).

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE)


