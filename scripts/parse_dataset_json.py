import numpy as np
from pathlib import Path


def parse_dataset_json(json_path, outpath, irange=None):
    # Load JSON data, assuming it's a list of dictionaries
    # create a directory task_{i:03d} for each entry
    # output the dictionary as a text file in that directory

    import json
    with open(json_path, "r") as f:
        data = json.load(f)
    print(f"Dataset total length: {len(data)}")

    if irange is None:
        irange = range(len(data))
    else:
        irange = range(irange[0], irange[1])
    for i in irange:
        # create a directory task_{i:03d}
        task_dir = Path(outpath) / f"task_{i:03d}"
        # remove if exists
        if task_dir.exists():
            import shutil
            shutil.rmtree(task_dir)
        task_dir.mkdir(parents=True, exist_ok=True)

        # output the dictionary as a text file in that directory
        # write question_text, answer_text, link, title, and question_id to a text file
        keys_to_write = ['question_text', 'answer_text', 'link', 'title', 'question_id']
        with open(task_dir / "raw_data.txt", "w") as f:
            for key in keys_to_write:
                f.write(f"{key}: {data[i][key]}\n\n")
        
    return 

if __name__ == "__main__":
    """
    python -u scripts/parse_dataset_json.py -i state/dataset.json -o shared_workspace/data_points --irange 0,20
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json-path',
        '-i',
        type=str,
        required=True,
        help='Path to the dataset JSON file'
    )
    parser.add_argument(
        '--outpath',
        '-o',
        type=str,
        required=True,
        help='Path to the output directory'
    )
    parser.add_argument(
        '--irange',
        '-r',
        type=str,
        default=None,
        help='Range of indices to process'
    )


    args = parser.parse_args()

    parse_dataset_json(args.json_path, args.outpath, irange=[int(x) for x in args.irange.split(",")] if args.irange else None)