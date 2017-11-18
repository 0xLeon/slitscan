import argparse
import os
import sys

import cv2
import numpy as np


__version__ = '1.0.0rc1'
"""str: slitscan version"""

class BreakException(Exception):
	"""Utility exception used to break out of loops"""
	pass

def slitscan(imsequence, height=400, frame_aggr=5):
	"""Generates a color strip of a given image sequence and returns the result as image object.

	Using OpenCV, this function creates a color slit scan from the given input
	file. By default, the average color of 5 frames is condensed into one stripe
	in the output image.

	If you encounter errors, this is probably due to unsupported video formats.
	Check if your Python OpenCV bindings are compiled using ffmpeg. If not,
	you have to manually compile OpenCV with Python bindings including ffmpeg.
	This is usually true for Linux and OS X because the PyPi installed OpenCV
	bindings do not support ffmpeg for these plattforms. The Windows version
	does support ffmpeg, but with the limitation of LGPL licensed code. If
	in doubt, convert your video to uncrompressed AVI or comparable.

	Args:
		imsequence (cv2.VideoCapture): Input image sequence
		height (int): Height of the output color strip, must be higher than 0
		frame_aggr (int): Number of frames to aggregate into one stipe, must be higher than 0

	Raises:
		ValueError: If any of the input parameters is invalid
	"""
	if frame_aggr < 1:
		raise ValueError('Invalid frame aggregation count {:d}'.format(frame_aggr))

	if height < 1:
		raise ValueError('Invalid output image height of {:d}'.format(height))

	bgr = []

	print('Reading frames')

	try:
		while imsequence.isOpened():
			bgrLocal = np.array([0, 0, 0], dtype=np.float)
			c = 0

			for i in range(0, frame_aggr):
				try:
					_, frame = imsequence.read()
					bgrLocal = bgrLocal + frame.mean(axis=0).mean(axis=0)
					c = c + 1
				except (TypeError, AttributeError):
					if c > 0:
						bgr.append((bgrLocal / c).round().astype(np.uint8))

					raise BreakException()

			bgr.append((bgrLocal / c).round().astype(np.uint8))
	except BreakException:
		pass
	finally:
		imsequence.release()

	print('Generating slit scan image')

	im = np.zeros((height, len(bgr), 3), dtype=np.uint8)

	for i in range(0, len(bgr)):
		im[:, i, :] = bgr[i]

	return im

def slitscanf(infile, height=400, frame_aggr=5, outfile=None):
	"""Generates a color strip of a given input video file and writes result as PNG image.

	Args:
		infile (str): Input video file
		height (int): Height of the output color strip, must be higher than 0
		frame_aggr (int): Number of frames to aggregate into one stipe, must be higher than 0
		outfile (str): Output file name relative to input file, can be specified absolute

	Raises:
		ValueError: If any of the input parameters is invalid
	"""

	if not os.path.isabs(infile):
		infile = os.path.abspath(infile)

	if outfile is None:
		outfile = os.path.abspath(os.path.join(os.path.dirname(infile), 'slitscan.png'))
	elif not os.path.isabs(outfile):
		outfile = os.path.abspath(os.path.join(os.path.dirname(infile), outfile))

	if len(outfile) < 4 or outfile[-4:].lower() != '.png':
		raise ValueError('Invalid output file path {:s}'.format(outfile))


	cap = cv2.VideoCapture(infile)

	im = slitscan(cap, height, frame_aggr)

	cv2.imwrite(outfile, im)

def main(argv=None):
	"""Function encapsulating the colorstrip generation function for command line access"""

	parser = argparse.ArgumentParser()
	parser.add_argument('--outfile', help='Output file name relative to input file, can be specified absolute')
	parser.add_argument('--height', default=400, type=int, help='Height of the output slit scan image')
	parser.add_argument('--frame-aggr', default=5, type=int, help='Number of frames to aggregate into one stipe')
	parser.add_argument('infile', help='Input video file')
	argv = parser.parse_args(argv)

	slitscanf(argv.infile, argv.height, argv.frame_aggr, argv.outfile)

if __name__ == '__main__':
	main(sys.argv[1:])
