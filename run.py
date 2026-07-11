import argparse
import json
import logging
import os
import time

import numpy as np
import pandas as pd
import yaml


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' not found.")

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config


def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("Invalid configuration format.")

    required_keys = ["seed", "window", "version"]

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config field: {key}")


def load_dataset(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' not found.")

    try:
        df = pd.read_csv(input_path)
    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format.")
    except Exception as e:
        raise ValueError(f"Unable to read CSV: {e}")

    return df


def validate_dataset(df):
    if df.empty:
        raise ValueError("Input CSV file is empty.")

    if "close" not in df.columns:
        raise ValueError("Required column 'close' is missing.")


def main():
    parser = argparse.ArgumentParser(
        description="MLOps Batch Processing Task"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to config YAML"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to metrics JSON"
    )

    parser.add_argument(
        "--log-file",
        required=True,
        help="Path to log file"
    )

    args = parser.parse_args()

    setup_logging(args.log_file)

    logging.info("Job started")

    start_time = time.perf_counter()

    try:

        # Load configuration
        config = load_config(args.config)
        validate_config(config)

        logging.info(
            f"Config loaded successfully: "
            f"seed={config['seed']}, "
            f"window={config['window']}, "
            f"version={config['version']}"
        )

        # Set deterministic seed
        np.random.seed(config["seed"])

        # Load dataset
        df = load_dataset(args.input)
        validate_dataset(df)

        logging.info(f"Rows loaded: {len(df)}")

        # Rolling Mean
        logging.info("Calculating rolling mean")

        df["rolling_mean"] = (
            df["close"]
            .rolling(window=config["window"])
            .mean()
        )

        # Signal Generation
        logging.info("Generating signals")

        df["signal"] = (
            df["close"] > df["rolling_mean"]
        ).astype(int)

        # Metrics
        rows_processed = len(df)

        signal_rate = df["signal"].mean()

        latency_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        metrics = {
            "version": config["version"],
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        # Write metrics
        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        # Print metrics (required by Docker)
        print(json.dumps(metrics, indent=4))

    except Exception as e:

        logging.exception("Job failed")
        logging.info("Job ended with status: error")

        version = "v1"

        if "config" in locals() and isinstance(config, dict):
            version = config.get("version", "v1")

        metrics = {
            "version": version,
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4)

        print(json.dumps(metrics, indent=4))

        raise


if __name__ == "__main__":
    main()