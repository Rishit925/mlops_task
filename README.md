# MLOps Batch Processing Task

## Overview

This project is a minimal MLOps-style batch processing pipeline built in Python. It demonstrates:

- Reproducible execution using a YAML configuration and fixed random seed
- Data validation and error handling
- Rolling mean computation
- Binary signal generation
- Structured metrics output in JSON format
- Logging for observability
- Dockerized deployment for one-command execution

---

## Project Structure

```
mlops-task/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```

---

## Requirements

- Python 3.11 (or compatible version)
- Docker Desktop (for containerized execution)

---

## Installation

Clone the repository or download the project.

Create a virtual environment (optional):

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

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

- Read the dataset
- Process the rolling mean
- Generate binary signals
- Create `metrics.json`
- Create `run.log`
- Print the metrics JSON to the terminal

---

## Processing Pipeline

The application performs the following steps:

1. Load configuration from YAML
2. Validate configuration fields
3. Set NumPy random seed
4. Load CSV dataset
5. Validate dataset
6. Compute rolling mean on the `close` column
7. Generate binary trading signals
8. Calculate performance metrics
9. Write metrics to `metrics.json`
10. Log execution details to `run.log`

---

## Output

### Sample metrics.json

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4989,
    "latency_ms": 19,
    "seed": 42,
    "status": "success"
}
```

---

## Logging

The application generates `run.log` containing:

- Job start timestamp
- Configuration details
- Dataset validation
- Processing steps
- Metrics summary
- Job completion status
- Exceptions and validation errors (if any)

---

## Error Handling

The application handles the following errors gracefully:

- Missing configuration file
- Invalid YAML configuration
- Missing required configuration fields
- Missing input CSV
- Invalid CSV format
- Empty dataset
- Missing `close` column

In every case, a `metrics.json` file is generated containing an appropriate error message.

---

## Dependencies

- pandas
- numpy
- PyYAML

---

