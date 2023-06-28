#!/usr/bin/env python

from typing import Optional
from pathlib import Path
import argparse
import sys
import guitarpro
from gptools import *


def retune_track(track: guitarpro.models.Track, amount: int) -> Optional[str]:
	for s in track.strings:
		n = s.value + amount
		if n <= 0:
			return "can't tune lower"
		elif n > 128:
			return "can't tune higher"
		s.value = n
	return None


def main():
	p = argparse.ArgumentParser(description="Transpose and change the tuning of all instruments in a guitarpro file")

	p.add_argument(
		"-a",
		"--amount",
		required=True,
		type=int,
		help="Transposition amount in semi-tones",
	)

	p.add_argument(
		"input",
		help="Path to a guitarpro file",
	)

	p.add_argument(
		"out",
		help="The path to save the changes to",
	)

	p.add_argument(
		"-f",
		"--force",
		action="store_true",
		help="Do not prompt for overwrites",
	)

	args = p.parse_args()
	if not -127 <= args.amount <= 127:
		eprint("error: the value for --amount must be between -127 and 127")
		exit(2)

	t = None
	try:
		t = guitarpro.parse(args.input)
	except Exception as e:
		eprint(f"error parsing input file: {e}")
		exit(1)

	out = Path(args.out)
	inp = Path(args.input)
	if out.is_dir():
		out = Path(inp.name)

	if out.is_dir():
		eprint("error: the output path points to a directory")
		exit(1)

	for track in t.tracks:
		if track.isPercussionTrack: continue
		res = retune_track(track, args.amount)
		if res:
			eprint(f"error retuning track {track.name}: {res}")
			exit(1)

	if not args.force and out.exists() and not prompt_bool(f"the file {out} already exists; overwrite it?"):
		eprint("not overwriting - exiting")
		exit(4)

	version = None if inp.suffix == out.suffix else infer_version(out)

	try:
		guitarpro.write(t, out, version=version, encoding="UTF8")
	except Exception as e:
		eprint(f"error saving modifications: {e}")
		exit(1)


if __name__ == "__main__": main()
