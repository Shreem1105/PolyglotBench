from langdetect import DetectorFactory, LangDetectException, detect

DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    candidate = text.strip()
    if len(candidate) < 3:
        return "unknown"

    try:
        return detect(candidate)
    except LangDetectException:
        return "unknown"
    except Exception:
        return "unknown"
