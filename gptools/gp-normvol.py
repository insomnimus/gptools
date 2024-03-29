#!/usr/bin/env python
# Normalizes track/song volumes

import argparse
import sys
import guitarpro
from gptools import *


def normalize_track(track: guitarpro.models.Track, target_peak: int) -> bool:
	peak = get_peak_velocity(track)
	if peak == target_peak: return False
	for m in track.measures:
		for v in m.voices:
			for b in v.beats:
				for n in b.notes:
					n.velocity = int(n.velocity * (target_peak / peak))
	return True


def normalize_song(song: guitarpro.models.Song, target_peak: int):
	peak = 1
	for t in song.tracks:
		peak = max(peak, t.channel.volume)

	if peak == target_peak: return False
	for t in song.tracks:
		t.channel.volume = int(t.channel.volume * (target_peak / peak))
	return True


def main():
	p = argparse.ArgumentParser(description="Normalize a guitarpro tabs volume", )

	p.add_argument(
		"-v",
		"--volume",
		required=True,
		type=int,
		help="The target peak volume (1-1023 in case of global, 1-127 in case of midi velocities)",
	)
	p.add_argument(
		"--midi-velocity",
		help="Normalize note velocities instead (1-127)",
		action="store_true",
	)
	p.add_argument(
		"input",
		help="Path to a guitarpro file",
	)
	p.add_argument(
		"out",
		help="The file to save to",
	)
	p.add_argument(
		"-f",
		"--force",
		action="store_true",
		help="Do not prompt for overwriting",
	)

	args = p.parse_args()
	if args.midi_velocity and not 1 <= args.volume <= 127:
		eprint("error: with `--midi-velocity`, the value of `--volume` must be between 1 and 127")
		exit(2)
	elif not args.midi_velocity and not 1 <= args.volume <= 1023:
		eprint(f"error: the value for `--volume` must be between 1 and 1023")
		exit(2)

	t = None
	try:
		t = guitarpro.parse(args.input)
	except Exception as e:
		eprint(f"error: {e}")
		exit(1)

	out = Path(args.out)
	inp = Path(args.input)
	if out.is_dir():
		out = Path(inp.name)

	if out.is_dir():
		eprint("error: the output path points to a directory")
		exit(1)

	if args.midi_velocity:
		for track in t.tracks:
			normalize_track(track, args.volume)
	else:
		normalize_song(t, args.volume)

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
