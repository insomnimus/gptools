from typing import Tuple, Optional
import guitarpro
import sys
from pathlib import Path
from os import PathLike


def eprint(msg):
	sys.stderr.write(f"{msg}\n")


def get_peak_velocity(track: guitarpro.models.Track) -> int:
	peak = 0
	for m in track.measures:
		for v in m.voices:
			for b in v.beats:
				for n in b.notes:
					peak = max(n.velocity, peak)
	return peak


def prompt_bool(msg: str) -> bool:
	while True:
		answer = input(f"{msg} [y/n]: ").strip().lower()
		if answer == "": continue
		return (answer == "y" or answer == "yes")


def infer_version(path: PathLike) -> Optional[Tuple[int, int, int]]:
	ext = Path(path).suffix
	if ext == ".gp5": return (5, 1, 0)
	elif ext == ".gp4": return (4, 0, 0)
	elif ext == ".gp3": return (3, 0, 0)
	else: return None
