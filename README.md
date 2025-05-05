# Encrypted Password Generator

A Python application to generate strong, random passwords with options for secure, encrypted saving.

## Overview

This application is a simple and user-friendly tool for generating strong passwords to meet your various security needs. In addition to password generation, the application provides an extra option to save passwords in an encrypted format using the `cryptography` library in Python, providing an additional layer of protection for your sensitive data.

The graphical user interface is designed using the `customtkinter` library, offering a modern and easy-to-use experience. The application currently supports both Arabic and English languages.

## Key Features

* **Strong Password Generation:** Create random passwords based on a specified length and options to include uppercase and lowercase letters, numbers, and special symbols.
* **Customizable Password Length:** Specify the desired length for the password.
* **Versatile Inclusion Options:** Control the types of characters to be included in the password.
* **Easy Copying:** Copy the generated password directly to the clipboard with a single click.
* **Save to Text File:** Option to save the password and associated username to a plain text file.
* **Encrypted Saving:** Option to save the username and password in an encrypted format in an internal database using the `cryptography.fernet` library.
* **View Encrypted Saved Passwords:** Browse and copy passwords saved in encrypted form within the application.
* **Multilingual Support:** User interface supports both Arabic and English with the ability to switch between them through the settings.
* **Settings Management:** Save language preferences for a personalized user experience.

## How to Use

1.  Run the main Python file (`.py`).
2.  In the application interface:
    * Specify the desired password length using the "Password Length" field.
    * Check the boxes to include letters, numbers, and symbols as needed.
    * Click the "Generate Password" button to create a new password.
    * You can click the "Regenerate" button to create another password with the same settings.
    * Click the "Copy" button to copy the password to the clipboard.
    * To save the password to a text file, click "Save to File" and you will be prompted to enter a username and choose a save location.
    * To save the password in encrypted form, click "Save Encrypted" and you will be prompted to enter a username; the data will be saved securely.
    * To view the encrypted saved passwords, click the "View Saved Passwords" button. You can copy any of the displayed passwords.
    * To change the language, click the settings icon (⚙️) in the top left corner and select the desired language from the menu.

## Requirements

* Python 3.x
* The following Python libraries (can be installed using pip):
    ```bash
    pip install customtkinter pyperclip cryptography
    ```

## Installation

1.  Clone this repository (if you are using Git version control).
    ```bash
    git clone <repository_link>
    cd <repository_name>
    ```
2.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
    (You can create a `requirements.txt` file containing `customtkinter`, `pyperclip`, `cryptography`)

## License

copyright adam rlsharkawy 2025


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at   

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the Licens



## Author

Parmagtee  company by adam elsharkawy


