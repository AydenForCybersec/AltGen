# Roblox Account Creator

## Description

The **Roblox Account Creator** is a Python script that automates the creation of Roblox accounts with memorable usernames. It features a Text User Interface (TUI) for easy interaction and ensures that each username is available before attempting to register an account.

## Features

* **Memorable Username Generation:** Creates usernames based on common Roblox naming patterns.
* **Username Availability Check:** Verifies if a username is available before account creation.
* **Interactive TUI:** Guides users through the account creation process with a simple text-based interface.
* **Batch Account Creation:** Supports generating multiple accounts in a single session.

## Requirements

* Python 3.x
* `requests` library (install via pip)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/roblox-account-creator.git
   cd roblox-account-creator
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare username files:**

   * Ensure the following files are in the same directory as the script:

     * `username_bits.txt` — contains common username bits.
     * `username_schemas.txt` — defines patterns for generating usernames.

2. **Run the script:**

   ```bash
   python script.py
   ```

3. **Follow the on-screen instructions:**

   * Enter the number of accounts you want to create.
   * The script will generate usernames, check their availability, and create the accounts.
   * Progress and feedback will be displayed via the TUI.

## File Structure

```
roblox-account-creator/
├── script.py                # Main script for account creation
├── username_bits.txt        # List of username components
├── username_schemas.txt     # List of username generation schemas
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## License

Copyright (c) 2025 DaRealAyden

Permission is hereby granted for educational and research use only.
Commercial use, redistribution, or use for automated account creation on any platform
in violation of its Terms of Service is strictly prohibited.

