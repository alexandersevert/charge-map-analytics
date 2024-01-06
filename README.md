# Charge Map Analytics

## Overview

`charge-map-analytics` is a project focused on analyzing and visualizing data related to charging stations for electric vehicles. This README provides comprehensive instructions for setting up the development environment, including package installation and database configuration.

## Architecture Diagram

[![Architecture Diagram](./architecture_diagrams/architecture_diagram.drawio.svg)](https://app.diagrams.net/#Halexandersevert%2Fcharge-map-analytics%2Fmain%2Farchitecture_diagrams%2Farchitecture_diagram.drawio.svg)

## Getting Started

### Prerequisites

Before beginning, ensure you have the following installed:
- Python 3.6 or higher
- PostgreSQL server
- Git (for version control)

### Installation

**1. Clone the repository**

Clone the repository to your local machine to get started with `charge-map-analytics`:

```bash
git clone https://github.com/alexandersevert/charge-map-analytics
cd charge-map-analytics
```

**2. Install Python Dependencies:**

`charge-map-analytics` uses several Python packages. Install them by executing the following command:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages as per the requirements.txt file in the project root.

**3. Database Environment Setup:**

The setup subfolder contains scripts for setting up the database. Follow these steps to configure your database environment:

a. Refer to the README in the setup folder for detailed instructions on creating and configuring the database:

```bash
less setup/README.md
```

Follow the instructions in setup/README.md to properly set up your database for `charge-map-analytics`.

## Usage

[Include instructions on how to use the application or execute `charge-map-analytics` main functionalities.]

## Contributing

We welcome contributions to the `charge-map-analytics` project! Please read our Contributing Guidelines for details on how to submit pull requests, adhere to coding standards, and more.

## Security

[Include any specific security concerns or guidelines related to `charge-map-analytics`.]

## License

[Specify the type of license under which `charge-map-analytics` is released, if applicable.]