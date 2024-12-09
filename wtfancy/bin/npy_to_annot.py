"""
Small utility script that converts .npy arrays into .annot format files.

This script takes a directory of .npy files containing sleep stage probabilities
and converts them into tab-delimited .annot files, following the Luna annotation format.

"""

from argparse import ArgumentParser
from glob import glob
import os
import numpy as np
from datetime import timedelta, datetime
from wtfancy.logging import Logger


def get_argparser():
    """
    Returns an argument parser for this script.
    """
    parser = ArgumentParser(description='Convert .npy sleep staging files to .annot format.')
    parser.add_argument("--input_files", type=str,
                        help='A glob statement matching all .npy files to convert.')
    parser.add_argument("--out_dir", type=str,
                        help="Directory to save the .annot output files.")
    parser.add_argument("--channel", type=str, default=".",
                        help="Optional channel identifier to include in the .annot file.")
    parser.add_argument("--format", type=str, choices=["standard", "model"], default="standard",
                        help="Output format: 'standard' or 'model'.")
    parser.add_argument("--time_encoding", type=str, choices=["elapsed_seconds", "clock_time", "elapsed_hms", "epoch"],
                        default="elapsed_seconds",
                        help="Time encoding format: 'elapsed_seconds', 'clock_time', 'elapsed_hms', or 'epoch'.")
    parser.add_argument("--start_time", type=str, default="00:00:00",
                        help="Start time for clock_time or elapsed_hms formats (e.g., '23:05:00').")
    parser.add_argument("--model", type=str, default=".",
                        help="Model name for instance metadata in 'model' format.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files of identical name")
    return parser


def parse_time_str(time_str):
    """
    Converts a HH:MM:SS string into a timedelta object.
    """
    h, m, s = map(int, time_str.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)


def format_time(start_seconds, time_encoding, start_time_obj, epoch_index=None):
    """
    Formats time based on the specified encoding.

    Args:
        start_seconds (int): Start time in seconds.
        time_encoding (str): The desired time encoding format.
        start_time_obj (timedelta): Start time for clock or elapsed_hms formats.
        epoch_index (int, optional): Epoch index for epoch encoding.

    Returns:
        (start_time, stop_time): Formatted start and stop times.
    """
    if time_encoding == "elapsed_seconds":
        return start_seconds, start_seconds + 30

    elif time_encoding == "clock_time":
        start_clock = (start_time_obj + timedelta(seconds=start_seconds)).strftime("%H:%M:%S")
        stop_clock = (start_time_obj + timedelta(seconds=start_seconds + 30)).strftime("%H:%M:%S")
        return start_clock, stop_clock

    elif time_encoding == "elapsed_hms":
        start_hms = f"0+{str(timedelta(seconds=start_seconds))}"
        stop_hms = f"0+{str(timedelta(seconds=start_seconds + 30))}"
        return start_hms, stop_hms

    elif time_encoding == "epoch":
        start_epoch = f"e{epoch_index}"
        stop_epoch = f"e{epoch_index + 1}"
        return start_epoch, stop_epoch


def convert_to_annot(input_file, output_file, logger, channel, fmt, time_encoding, start_time, model):
    """
    Converts a single .npy file to .annot format based on the chosen output format.

    Args:
        input_file (str): Path to the .npy file.
        output_file (str): Path to the output .annot file.
        logger (Logger): Logger instance for logging messages.
        channel (str): Channel identifier to include in the .annot file.
        fmt (str): Output format ('standard' or 'model').
        time_encoding (str): Time encoding format.
        start_time (str): Start time for clock_time or elapsed_hms formats.
        model (str): Model name for instance metadata in 'model' format.
    """
    logger(f"Processing file: {input_file}")

    try:
        # Load the .npy file
        data = np.load(input_file)

        # Check for expected shape [n, 5]
        if data.ndim != 2 or data.shape[1] != 5:
            logger(f"Error: Unexpected shape {data.shape}. Expected (n, 5).")
            return

        # Define the sleep stage order in the .npy file and the desired output order
        npy_stages = ["W", "N1", "N2", "N3", "R"]
        annot_stages = ["N1", "N2", "N3", "R", "W"]
        reordered_data = data[:, [npy_stages.index(stage) for stage in annot_stages]]

        lines = []
        start_seconds = 0
        start_time_obj = parse_time_str(start_time)

        for i, probs in enumerate(reordered_data):
            # Format start and stop times
            start_time_str, stop_time_str = format_time(start_seconds, time_encoding, start_time_obj, i)

            # Standard format
            if fmt == "standard":
                meta = ";".join([f"p{stage}={prob:.2f}" for stage, prob in zip(annot_stages, probs)])
                max_stage = annot_stages[np.argmax(probs)]  # Most likely stage
                lines.append(f"stage\t{max_stage}\t{channel}\t{start_time_str}\t{stop_time_str}\t{meta}")

            # Model-specific format
            elif fmt == "model":
                meta = f"p{annot_stages[np.argmax(probs)]}={np.max(probs):.2f}"  # Only the max stage
                max_stage = annot_stages[np.argmax(probs)]
                lines.append(f"{max_stage}\t{model}\t{channel}\t{start_time_str}\t{stop_time_str}\t{meta}")

            start_seconds += 30  # Increment by 30 seconds

        # Add header depending on the format
        lines.insert(0, "class\tinstance\tchannel\tstart\tstop\tmeta")

        # Write to the output file
        with open(output_file, "w") as f:
            f.write("\n".join(lines))

        logger(f"File saved: {output_file}")

    except Exception as e:
        logger(f"Error processing {input_file}: {str(e)}")


def run(args):
    """
    Main function to handle the conversion of all matched .npy files.
    """
    files = glob(args.input_files)
    out_dir = os.path.abspath(args.out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    logger = Logger(out_dir,
                    active_file='convert_to_annot_log',
                    overwrite_existing=args.overwrite,
                    print_calling_method=False)

    logger(f"Args dump: {vars(args)}")
    logger(f"Found {len(files)} files matching glob statement.")

    if len(files) == 0:
        logger("No files to process. Exiting.")
        return

    for input_file in files:
        output_file = os.path.join(out_dir, os.path.splitext(os.path.basename(input_file))[0] + ".annot")
        if os.path.exists(output_file) and not args.overwrite:
            logger(f"Skipping existing file (overwrite not set): {output_file}")
            continue

        convert_to_annot(input_file, output_file, logger, args.channel, args.format, args.time_encoding,
                         args.start_time, args.model)


def entry_func(args=None):
    """
    Entry function for the script.
    """
    parser = get_argparser()
    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    entry_func()
