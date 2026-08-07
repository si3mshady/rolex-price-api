import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Union

from app.models.watch import Watch

logger = logging.getLogger(__name__)


def load_rolex_data(file_path: Union[str, Path]) -> List[Watch]:
    """
    Loads and normalizes Rolex watch data from a JSON file.

    Args:
        file_path: Path to the JSON data file.

    Returns:
        List of Watch domain model objects.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Rolex data file not found at path: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw_data: List[Dict[str, Any]] = json.load(f)

    watches: List[Watch] = []

    for idx, item in enumerate(raw_data, start=1):
        reference = str(item.get("Reference", "")).strip()
        collection = str(item.get("Collection", "")).strip()
        description = str(item.get("Description", "")).strip()
        size = int(item.get("Size", 0))
        rrp_raw = str(item.get("RRP", "")).strip()

        # Parse RRP & Numeric Price
        is_por = rrp_raw.upper() == "POR"
        price: Union[float, None] = None

        if not is_por:
            try:
                price = float(rrp_raw)
            except ValueError:
                logger.warning(
                    f"Unexpected RRP format '{rrp_raw}' at index {idx} for ref {reference}. Treating as POR."
                )
                is_por = True
                price = None

        # Parse & normalize Complications
        complications_raw = item.get("Complication")
        complications: List[str] = []
        if isinstance(complications_raw, list):
            complications = [
                str(comp).strip()
                for comp in complications_raw
                if comp and str(comp).strip()
            ]

        # Generate unique watch ID
        watch_id = f"watch-{idx:03d}-{reference.lower()}"

        watch = Watch(
            id=watch_id,
            reference=reference,
            collection=collection,
            description=description,
            size=size,
            rrp=rrp_raw,
            price=price,
            is_por=is_por,
            complications=complications,
        )
        watches.append(watch)

    logger.info(f"Successfully loaded {len(watches)} Rolex watch records from {path}")
    return watches
