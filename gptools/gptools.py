import guitarpro
import sys

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
