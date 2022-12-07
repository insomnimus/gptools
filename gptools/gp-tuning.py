#!/usr/bin/env python
# Shows the tuning for tracks

def main():
	import argparse
	import sys
	import guitarpro

	p = argparse.ArgumentParser(
		prog = "tuning",
		description = "Display the tunings for tracks in a guitarpro tab",
	)
	p.add_argument("path", help = "Path to a guitarpro file")
	p.add_argument(
		"-g", "--guitar",
		help = "Show only the guitar tracks",
		action = "store_true",
	)
	p.add_argument(
		"-b", "--bass",
		help = "Show only the bass tracks",
		action = "store_true",
	)

	args = p.parse_args()

	def is_bass(no: int) -> bool:
		return (31 <= no <= 39)
	def is_guitar(no: int) -> bool:
		return (24 <= no <= 31)

	def format_strings(s: guitarpro.models.GuitarString) -> str:
		strings = []
		notes = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
		for x in reversed(s):
			strings.append(notes[x.value % 12])

		return " ".join(strings)

	t = None

	try:
		t = guitarpro.parse(args.path)
	except Exception as e:
		sys.stderr.write(f"error reading {args.path}: {e}")
		exit(1)

	if len(t.tracks) == 0:
		sys.stderr.write(f"no tracks in {args.path}")
		exit(2)

	for track in t.tracks:
		inst = track.channel.instrument
		if not args.bass and not args.guitar: None # do nothing
		elif args.bass and not is_bass(inst): continue
		elif args.guitar and not is_guitar(inst): continue
		elif track.isPercussionTrack: continue

		print(f"{track.name}: {format_strings(track.strings)}")

if __name__ == "__main__": main()