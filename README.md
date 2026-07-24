# ML/MLOps Engineering Internship - Task 0

## Project Overview

This project is a minimal MLOps-style batch processing pipeline developed as part of the ML/MLOps Engineering Internship Technical Assessment.

The application reads a financial dataset, computes a rolling mean on the `close` price, generates binary trading signals, and outputs structured metrics along with detailed execution logs.

The project demonstrates:

- Reproducible execution using a YAML configuration file
- Input validation and error handling
- Structured logging for observability
- Machine-readable metrics output
- Dockerized deployment for consistent execution

---

## Project Structure

```
.
├── run.py              # Main application
├── config.yaml         # Configuration file
├── data.csv            # Input dataset
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── metrics.json        # Sample output metrics
├── run.log             # Sample execution log
└── README.md
```

---

## Features

- YAML-based configuration
- Deterministic execution using random seed
- Input validation and error handling
- Rolling mean computation
- Binary signal generation
- Structured JSON metrics
- Detailed execution logging
- Dockerized execution

---

## Requirements

- Python 3.9+
- pip

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

The application reads parameters from `config.yaml`.

Example:

```yaml
seed: 42
window: 5
version: "v1"
```

---

## Running Locally

Execute the application using:

```bash
python run.py \
    --input data.csv \
    --config config.yaml \
    --output metrics.json \
    --log-file run.log
```

---

## Docker

### Build Docker Image

```bash
docker build -t mlops-task .
```

### Run Docker Container

```bash
docker run --rm mlops-task
```

The container will:

- Load `data.csv`
- Read configuration from `config.yaml`
- Generate `metrics.json`
- Generate `run.log`
- Print the final metrics JSON to the terminal

---

## Processing Pipeline

The application performs the following steps:

1. Load and validate the YAML configuration.
2. Set the random seed for reproducibility.
3. Load and validate the input CSV file.
4. Verify that the required `close` column exists.
5. Compute the rolling mean using the configured window size.
6. Generate binary trading signals:
   - `1` if `close > rolling_mean`
   - `0` otherwise
7. Calculate execution metrics.
8. Write metrics to `metrics.json`.
9. Record execution details in `run.log`.

---

## Validation Performed

The application validates:

- Configuration file exists
- Required configuration fields are present
- Input CSV exists
- CSV is readable
- CSV is not empty
- Required `close` column exists

If any validation fails:

- An error is logged
- An error `metrics.json` is generated
- The application exits with a non-zero status code

---

## Output Files

### metrics.json

Contains structured execution metrics.

Example:

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4990,
    "latency_ms": 127,
    "seed": 42,
    "status": "success"
}
```

In case of failure:

```json
{
    "version": "v1",
    "status": "error",
    "error_message": "Description of the error"
}
```

---

### run.log

The log file contains:

- Job start time
- Configuration details
- Dataset loading information
- Processing steps
- Metrics summary
- Job completion status
- Exception details (if any)

---

## Technologies Used

- Python
- Pandas
- NumPy
- PyYAML
- Docker
- Logging

---

## Reproducibility

The application ensures deterministic execution by:

- Loading parameters from `config.yaml`
- Setting the random seed before processing
- Avoiding hard-coded paths
- Producing structured outputs for every execution

---



