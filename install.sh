#!/bin/bash

# ANSI Color Codes
CYAN='\033[96m'
GREEN='\033[92m'
RESET='\033[0m'

echo -e "${CYAN}[*] Installing ShadowWatch FIM Agent...${RESET}"

# Download the raw Python script from your GitHub repo and place it in global bin
sudo curl -sL "https://raw.githubusercontent.com/devsecnox/ShadowWatch/main/shadowwatch.py" -o /usr/local/bin/shadowwatch

# Grant execution permissions
sudo chmod +x /usr/local/bin/shadowwatch

echo -e "${GREEN}[+] Installation Complete!${RESET}"
echo -e "${CYAN}[*] You can now start the agent by typing 'shadowwatch' anywhere in your terminal.${RESET}"
