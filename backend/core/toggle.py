import os

TRUE_SET = {"1", "true", "yes", "on"}
FALSE_SET = {"0", "false", "no", "off", ""}

def toggle(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    val = str(raw).strip().lower()

    if val in TRUE_SET:
        return True

    if val in FALSE_SET:
        return False

    return default