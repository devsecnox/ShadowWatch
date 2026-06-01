# ShadowWatch FIM

**A lightweight, continuous File Integrity Monitoring (FIM) agent for Linux environments.**

## Overview
ShadowWatch is a Python-based security tool designed to detect unauthorized file modifications in real-time. By utilizing SHA-256 hashing algorithms, it creates a secure baseline of your target directory and continuously monitors for any deviations, logging potential breaches instantly. Developed with a focus on both security and enterprise-level reliability.

## Features
* **Continuous Monitoring**: 24/7 background scanning with a low CPU footprint.
* **Smart Whitelisting**: Automatically ignores noisy directories (e.g., .venv, .idea) to prevent alert fatigue and infinite feedback loops.
* **Enterprise Logging**: Maintains detailed, timestamped records in shadowwatch_alerts.log for SIEM integration.
* **Dynamic UX**: Features an interactive terminal radar and ANSI-colored alerts for an immersive command-line experience.

## Quick Install (One-Liner)
You can install ShadowWatch globally on your Linux system using this single command:

```bash
curl -sL https://raw.githubusercontent.com/devsecnox/ShadowWatch/main/install.sh | bash
```

## Usage
Once installed, simply type the following command anywhere in your terminal:

```bash
shadowwatch
```

1. Enter the absolute path of the directory you want to monitor (e.g., /etc or ~/Desktop/Target).
2. The agent will automatically generate a baseline.json if it is the first run.
3. Leave it running in the background to catch any unauthorized modifications. Press Ctrl+C to gracefully stop the agent.

## Requirements
* Python 3.x
* Linux Environment (Arch Linux / Ubuntu / Debian etc.)
* Root privileges (only required during the one-liner installation)

## License
This project is licensed under the GNU GPLv3 License. You are free to use, modify, and distribute this software, provided that any derivative works are also made open-source under the same license.
