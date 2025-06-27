"""Manage scheduled scan profiles stored in JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, Iterable, List

from .scheduler import AdaptiveScheduler

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
PROFILE_FILE = DATA_DIR / "profiles.json"


def load_profiles() -> List[Dict[str, any]]:
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_profiles(profiles: Iterable[Dict[str, any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(profiles), f, indent=2)


def add_profile(name: str, cidr: str, intensity: str = "low", interval: int = 3600) -> None:
    profiles = [p for p in load_profiles() if p.get("name") != name]
    profiles.append({"name": name, "cidr": cidr, "intensity": intensity, "interval": interval})
    save_profiles(profiles)


def remove_profile(name: str) -> None:
    profiles = [p for p in load_profiles() if p.get("name") != name]
    save_profiles(profiles)


def list_profiles() -> List[Dict[str, any]]:
    return load_profiles()


def run_scheduled(scan_func: Callable[[str, str], None]) -> None:
    """Run the scheduler with the given scanning function."""
    sched = AdaptiveScheduler()
    for p in load_profiles():
        sched.schedule_scan(p["cidr"], lambda cidr=p["cidr"], intensity=p.get("intensity", "low"): scan_func(cidr, intensity), p.get("interval", 3600))
    sched.run()
