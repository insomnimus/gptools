#!/usr/bin/env python

import guitarpro
import argparse
import sys
from gptools import *


def main():
	p = argparse.ArgumentParser(
		description = "Show volume of tracks in a guitarpro file",
	)

	p.add_argument(
		"path",
		help = "One or more guitarpro files",
		nargs = "+",
	)

	args = p.parse_args()

	n_err = 0
	for path in args.path:
		t = None
		try:
			t = guitarpro.parse(path)
		except Exception as e:
			eprint(f"error reading {path}: {e}")
			n_err += 1
			continue

		print(f"# {path}:")
		for track in t.tracks:
			peak = get_peak_velocity(track)
			print(f"\t{track.name}: volume = {track.channel.volume}, velocity peak = {peak}")
	exit(n_err)

if __name__ == "__main__": main()
