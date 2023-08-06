#!/usr/bin/env python2
"""
Stitch frames together into a video
"""

import argparse
import pathlib
import subprocess
import re
import logging
import math

LOG = logging.getLogger(__name__)


def stitch_frames(frame_dir: pathlib.Path, output_file: pathlib.Path,
                  start_idx: int, stop_idx: int, step=1,
                  fps=59.94,
                  overwrite=False,
                  frame_pattern=re.compile(r'.*jpg', re.IGNORECASE)):
    """
    Stitch a directory containing sequentially numbered frames into a
    video using FFMpeg

    Args:
        frame_dir: directory whose children are all frames
        output_file: path to video file composed from stitching all the frames in ``frame_dir``
        start_idx: index of the first frame to stitch after listing and sorting all frames with ``list.sort()``
        stop_idx: index of the last frame to stitch after listing and sorting all frames with ``list.sort()``, use -1
            to calculate the last frame based on the ``start_idx`` and ``step``
        step: step size between adjacent frames (use 1 for stitching all frames, 2 for skipping every other frame,
            -1 for reversing the video)
        fps: frames per second for the resulting video
        overwrite: overwrite the ``output_file`` if it already exists?
        frame_pattern: python regex pattern for selecting a subset of files, defaults to selecting everything

    Returns: None
    """
    if not frame_dir.exists():
        raise FileNotFoundError("Frame directory + " + str(frame_dir) + " does not exist")
    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True, exist_ok=True)
    assert not output_file.exists() or overwrite, f'{output_file} already exists, and `overwrite` wasn\'t set'
    frames = [str(frame) for frame in frame_dir.iterdir() if frame_pattern.search(str(frame))]
    frames.sort()  # iterdir doesn't guarantee files are listed in lexicographic order
    if stop_idx == -1:
        stop_idx = int(len(frames) / math.fabs(step))
    if step > 0:
        selected_frames = frames[start_idx:stop_idx:step]
    else:
        selected_frames = frames[stop_idx:start_idx:step]
    assert len(selected_frames) > 0, f'No selected frames in {frame_dir}, check the directory has frames,' + \
                                     'and the `frame_pattern` matches some files.'

    cat = subprocess.Popen(['cat'] + selected_frames, stdout=subprocess.PIPE)
    LOG.info(f'Stitching frames from {frame_dir} into video {output_file}')
    try:
        subprocess.check_output(('ffmpeg', '-framerate', str(fps), '-f', 'image2pipe', '-i', '-',
                                 '-c:v', 'libx264', '-y', str(output_file.resolve())),
                                stdin=cat.stdout, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("FFMpeg failed to stitch files:\n" +
              "Output:\n" + str(e.output))
        raise e
    # Signal SIGPIPE to ffmpeg call if the cat call fails
    # See https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline for more
    cat.stdout.close()
