#!/usr/bin/env python3
import hashlib
import json
import time
import logging
import os
import sys
from pathlib import Path


# ANSI Color Codes for terminal aesthetics
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'


# Items to exclude from monitoring to prevent infinite loops and reduce noise
EXCLUDED_ITEMS = [".venv", ".idea", "baseline.json", "__pycache__", "shadowwatch_alerts.log"]

# Configure the logging architecture for enterprise-level record keeping
logging.basicConfig(
    filename="shadowwatch_alerts.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def print_banner():
    """
    Displays the ASCII art banner with terminal colors.
    Provides a professional command-line interface look.
    """
    banner = f"""{Colors.CYAN}
      ___ _            _          _      __      __   _      _   
     / __| |_  __ _ __| |_____ __| |__   \\ \\    / /_ _| |_ __| |_ 
     \\__ \\ ' \\/ _` / _` / _ \\ V  V /_ \\   \\ \\/\\/ / _` |  _/ _| ' \\
     |___/_||_\\__,_\\__,_\\___/\\_/\\_/ __/    \\_/\\_/\\__,_|\\__\\__|_||_|
    {Colors.MAGENTA}
    [*] File Integrity Monitoring (FIM) Agent - v1.0
    [*] Developed by Nox
    {Colors.RESET}"""
    print(banner)


def radar_wait(seconds):
    """
    Creates a dynamic terminal spinner and countdown timer.
    Improves UX by showing the agent is still active during the sleep cycle.
    """
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + seconds
    idx = 0

    while time.time() < end_time:
        remaining = int(end_time - time.time())
        sys.stdout.write(
            f"\r{Colors.CYAN}[{spinner_chars[idx % len(spinner_chars)]}] System active. Next scan in {remaining}s...{Colors.RESET}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

    # Clear the line when the timer finishes
    sys.stdout.write("\r" + " " * 60 + "\r")


def calculate_file_hash(file_path):
    """
    Calculates the SHA-256 hash of a given file.
    Reads the file in 4KB chunks to prevent memory overflow (OOM) on large files.
    """
    target_path = Path(file_path).expanduser()
    hash_object = hashlib.sha256()
    with open(target_path, 'rb') as file:
        while True:
            chunk_data = file.read(4096)
            if not chunk_data:
                break
            hash_object.update(chunk_data)
    return hash_object.hexdigest()


def file_detect(file_path):
    """
    Scans the target directory recursively.
    Filters out excluded items and returns a dictionary mapping file paths to their hashes.
    """
    system_state = {}
    target_path = Path(file_path).expanduser()
    for file_obj in target_path.rglob("**/*"):
        if file_obj.is_file():
            file_str = str(file_obj)
            is_excluded = any(excluded in file_str for excluded in EXCLUDED_ITEMS)
            if not is_excluded:
                system_state[file_str] = calculate_file_hash(file_obj)
    return system_state


def save_baseline(data, output_file):
    """
    Saves the system state dictionary to a JSON file for persistent storage.
    """
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


def load_baseline(input_file):
    """
    Loads the previously saved system state from a JSON file.
    """
    with open(input_file, "r") as f:
        data = json.load(f)
    return data


def compare_states(old_state, current_state):
    """
    Compares the current system state against the loaded baseline.
    Logs warnings for modified files and info for newly added files.
    """
    for file_path, current_hash in current_state.items():
        if file_path in old_state:
            if old_state[file_path] != current_hash:
                logging.warning(f"Modified File Detected -> {file_path}")
                print(f"{Colors.RED}[!] ALERT: Modified File Detected -> {file_path}{Colors.RESET}")
        else:
            logging.info(f"New File Detected -> {file_path}")
            print(f"{Colors.GREEN}[+] INFO: New File Detected -> {file_path}{Colors.RESET}")


# ==========================================
# MAIN AGENT EXECUTION
# ==========================================

if __name__ == "__main__":
    print_banner()

    # Define target and configuration
    target_dir = input(f"{Colors.YELLOW}[>] Enter the directory path to monitor: {Colors.RESET}")
    baseline_file = "baseline.json"

    # Initialize or load baseline
    if not os.path.exists(baseline_file):
        print(f"\n{Colors.CYAN}[*] Baseline not found. Creating a new baseline for {target_dir}...{Colors.RESET}")
        initial_state = file_detect(target_dir)
        save_baseline(initial_state, baseline_file)
        print(f"{Colors.GREEN}[*] Baseline created successfully.{Colors.RESET}")
        previous_state = initial_state
    else:
        print(f"\n{Colors.CYAN}[*] Existing baseline loaded.{Colors.RESET}")
        previous_state = load_baseline(baseline_file)

    # Start continuous monitoring
    logging.info("ShadowWatch Continuous Monitoring Started...")
    print(f"{Colors.CYAN}[*] ShadowWatch Continuous Monitoring Started... (Press Ctrl+C to stop)\n{Colors.RESET}")

    try:
        while True:
            current_state = file_detect(target_dir)
            compare_states(previous_state, current_state)
            previous_state = current_state

            # Dynamic UI radar for the waiting period
            radar_wait(10)

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print(f"\n{Colors.MAGENTA}[*] ShadowWatch Stopped by User. Stay safe!{Colors.RESET}")
        logging.info("ShadowWatch Stopped by User.")