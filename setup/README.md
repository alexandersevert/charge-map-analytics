# Environment Setup for Charge Map Analytics

This section of the repository, located in the setup folder, contains scripts for initial environment setup, including creating a PostgreSQL database. These scripts are the first step in preparing your environment for charge-map-analytics and are designed for easy configuration of the necessary database components.

## Prerequisites

- Python 3.6 or higher.
- PostgreSQL server installed and running.
- psycopg2 Python library.

## Folder Structure
```
charge-map-analytics/
│
├── setup/
│   ├── create_credentials_json.py
│   ├── create_postgres_db.py
│   └── README.md
│
└── [other project directories]
```

## Initial Setup

### 1. Database Credentials Configuration

**a. Create Credentials File**

Run `create_credentials_json.py` inside the setup folder to generate a credentials.json file. This file will store your PostgreSQL server credentials.

```bash
cd setup
python create_credentials_json.py
```

Follow the prompts to enter your database credentials: database name, user, password, host, and port.

**b. Security of Credentials File**

The credentials.json file is already included in the .gitignore to prevent it from being committed to version control. Ensure this file is kept secure and not shared publicly.

### 2. Creating the Database

Run `create_postgres_db.py` to create a new PostgreSQL database.

```bash
python create_postgres_db.py
```

Enter the name of the new database when prompted. Verify the creation of the database by logging into your PostgreSQL server.

## Next Steps

After setting up the database, proceed to the next steps in the `charge-map-analytics` setup process as outlined in the main README.md.

## Security Considerations

Handle all credentials and sensitive information securely:

- Avoid committing sensitive data to version control.
- Consider stronger security measures for production environments, such as environment variables or a secure vault system.

## Contributing

We welcome contributions to `charge-map-analytics`. For changes to the setup process, please fork the repository, make your changes in a separate branch, and submit a pull request.