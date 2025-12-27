# app/logger.py
import logging
from pathlib import Path

# Création du dossier logs si absent
Path("app/logs").mkdir(parents=True, exist_ok=True)

# Configuration du logger
logging.basicConfig(
    filename="app/logs/predictions.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("prediction_logger")


def log_success(prediction, mae, elapsed_time, input_data):

    if mae >=100000 and mae <=1000000:
        mae_error="SUCCESS"
    elif mae >1000000:
        mae_error="WARNING"
    else:
        mae_error="CRITICAL"



    logger.info(
        f"SUCCESS | Prediction={prediction} | "
        f"Time={elapsed_time}s | Input={input_data} | RATIO_SEUIL={mae} | ERROR_LEVEL={mae_error}"
    )


def log_error(error_message, input_data):
    logger.error(
        f"ERROR | {error_message} | Input={input_data}"
    )
