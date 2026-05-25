# src/utils/audit_logger.py
# Save compliance decisions to audit logs for traceability, accountability and auditability.

import json
import os
from datetime import datetime

AUDIT_FOLDER = "audit_logs"

os.makedirs(AUDIT_FOLDER, exist_ok=True)


def log_audit_event(explanation):
    """
    Save compliance decision to audit log.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{AUDIT_FOLDER}/audit_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(explanation, f, indent=4)

    return filename