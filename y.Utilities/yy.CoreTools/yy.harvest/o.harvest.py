def run(depth=3, dry_run=True):
    """
    STUB – world-model extractor placeholder.
    Writes a dummy DATA/P_hat_* file when dry_run is False.
    """
    if dry_run:
        print("[harvest] stub – nothing extracted")
    else:
        import json, datetime, pathlib
        ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        pathlib.Path("DATA").mkdir(exist_ok=True)
        (pathlib.Path("DATA") / f"P_hat_stub_{ts}.json").write_text(
            json.dumps({"stub": True, "depth": depth}))
