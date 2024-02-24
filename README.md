# Cloud Security Posture Management (CSPM) Framework Mapper

This repository contains scripts to map security control frameworks to various cloud service providers' security posture management (CSPM) reports.

## Overview

Cloud service providers (CSPs) such as Azure, AWS, and GCP offer security posture management reports that help users assess their security controls against various compliance frameworks such as SOC 2 Type II and PCI DSS. However, interpreting and comparing these reports across different CSPs can be challenging. This repository provides scripts to streamline the process by mapping security controls from CSPM reports to standardized frameworks.

## Features

- Automatically maps security controls from CSPM reports to standardized frameworks.
- Supports multiple cloud service providers including Azure, AWS, and GCP.
- Outputs the mapped controls in JSON format for easy consumption and integration with other tools.

## Usage

To use the scripts in this repository:

1. Ensure you have Python installed on your system.
2. Clone the repository to your local machine.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Place your CSPM reports in the respective cloud directories (`AZURE_CSPM`, `AWS_CSPM`, `GCP_CSPM`).
5. Run the main script `map_controls.py` with the desired framework name as an argument.

Example usage:

```bash
python map_controls.py "SOC 2 Type II"
```

## File Structure

├── AZURE_CSPM
│ ├── SOC 2 Type II.json
│ └── PCI.json
├── AWS_CSPM
│ ├── SOC 2 Type II.json
│ └── PCI.json
├── GCP_CSPM
│ ├── SOC 2 Type II.json
│ └── PCI.json
├── CONTROL_MAPPINGS
│ ├── azure_SOC 2 Type II.json
│ ├── aws_SOC 2 Type II.json
│ ├── gcp_SOC 2 Type II.json
│ ├── azure_PCI.json
│ ├── aws_PCI.json
│ └── gcp_PCI.json
├── map_controls.py
└── README.md

## Contributing

Contributions to this repository are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request & use [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
You can customize this README according to your specific project details and requirements.
