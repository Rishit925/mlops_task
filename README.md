# MLOps Batch Processing Task

## Overview

This project is a minimal MLOps-style batch processing pipeline developed in Python. It demonstrates:

- Reproducible execution using a YAML configuration and fixed random seed
- Data validation and robust error handling
- Rolling mean computation on market data
- Binary signal generation
- Structured metrics output in JSON format
- Detailed logging for observability
- Dockerized deployment for one-command execution

---

## Project Structure

```text
mlops-task/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
├── run.log
├── .dockerignore
└── .gitignore (optional)
```

---

## Requirements

- Python 3.11 or later
- Docker Desktop

---

## Installation

Clone the repository or download the project.

### Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The configuration is stored in `config.yaml`.

Example:

```yaml
seed: 42
window: 5
version: "v1"
```

---

## Local Execution

Run the application using:

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## Docker Build

Build the Docker image:

```bash
docker build -t mlops-task .
```

---

## Docker Run

Run the Docker container:

```bash
docker run --rm mlops-task
```

The container will:

- Read the configuration
- Load the dataset
- Compute the rolling mean
- Generate binary signals
- Create `metrics.json`
- Create `run.log`
- Print the metrics JSON to the terminal

---

## Processing Pipeline

The application performs the following steps:

1. Load configuration from `config.yaml`
2. Validate required configuration fields
3. Set NumPy random seed
4. Load and validate the CSV dataset
5. Compute the rolling mean of the `close` column
6. Generate binary trading signals
7. Calculate processing metrics
8. Save metrics to `metrics.json`
9. Log execution details to `run.log`
10. Print the metrics JSON to stdout

---

## Example Output (`metrics.json`)

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4990,
    "latency_ms": 25,
    "seed": 42,
    "status": "success"
}
```

> **Note:** `value` and `latency_ms` may vary slightly depending on the dataset and machine.

---

## Logging

The application generates `run.log` containing:

- Job start timestamp
- Configuration validation
- Dataset loading
- Rolling mean computation
- Signal generation
- Metrics summary
- Job completion status
- Exception details (if any)

---

## Error Handling

The application gracefully handles:

- Missing configuration file
- Invalid configuration format
- Missing required configuration fields
- Missing input CSV
- Invalid CSV format
- Empty dataset
- Missing `close` column

In every failure case, a `metrics.json` file is still generated with an appropriate error message.

---

## Dependencies

- NumPy
- Pandas
- PyYAML

---

## Notes

- The application uses a fixed random seed (`seed: 42`) to ensure reproducibility.
- No file paths are hardcoded; all paths are provided through command-line arguments.
- The project is fully Dockerized for consistent execution across environments.

