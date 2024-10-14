# Network Configuration Scripts

This repository contains two Python scripts designed to help automate network configuration and validation tasks. These scripts generate shell scripts based on user inputs, streamlining the process of managing network devices.

## Scripts

### 1. Environment Configuration Script

**File:** `generate_environment_script.py`

This script generates a shell script that modifies the environment configuration of network devices based on user input.

#### Features
- Accepts user-defined hostname patterns.
- Configures environment settings for multiple devices.
- Generates a shell script for executing the changes.

#### Usage
To use the environment configuration script:

1. Ensure you have Python installed.
2. Run the script in your terminal:
   ```bash
   python generate_environment_script.py
