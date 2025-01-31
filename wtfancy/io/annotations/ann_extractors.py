import os
import pandas as pd

from wtfancy.hypnogram.formats import StartDurationStageFormat
from wtfancy.hypnogram.utils import sparse_hypnogram_from_ids_format

def _from_txt_Gamma(file_path, **kwargs):
    import pandas as pd
    import numpy as np
    stage_dict = {
        0: "W",
        1: "N1",
        2: "N2",
        3: "N3",
        4: "N3",
        5: "REM",
        6: "UNKNOWN",
        7: "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    df_ann = pd.read_csv(file_path, delimiter='\t')

    # try:
    #     # Try to access the column
    #     print(df_ann['Epoch'])
    # except KeyError:
    #     # If the Epoch is not present, skip to the next iteration
    #     print(f"Column Epoch not found in {file_path}, adding column names...")
    #     # Define column names
    #     column_names = ['Epoch', 'User-Defined Stage', 'CAST-Defined Stage']
    #     # Function to add column names
    #     def add_column_names(df, column_names):
    #         """
    #         Add column names to a DataFrame if they are not already present.
    #
    #         Parameters:
    #         df (pd.DataFrame): The DataFrame to which column names are to be added.
    #         column_names (list): A list of column names.
    #
    #         Returns:
    #         pd.DataFrame: DataFrame with the added column names.
    #         """
    #
    #         if df.columns.tolist() == list(range(len(df.columns))):
    #             df.columns = column_names
    #         return df
    #
    #     # Add column names
    #     df_ann = add_column_names(df_ann, column_names)

    # Check continuity - Check if all differences are 1
    check_diff = np.diff(df_ann['Epoch'].to_numpy())
    try:
        assert (check_diff == 1).all(), f"Discontinuity detected in the labels in {file_path}"
    except AssertionError as e:
        # Handle the exception, log the issue
        print(f"Warning: {str(e)}. Proceeding with available data.")
    # except AssertionError as e:
    #     # Raise an error if the assertion fails
    #     raise ValueError(str(e))
    # Iterate over DataFrame rows using itertuples()
    for index, row in df_ann.iterrows():
        stage = stage_dict[row["User-Defined Stage"]]
        start = int((row['Epoch'] - 1) * 30)
        dur = 30
        stages.append(stage)
        starts.append(start)
        durs.append(dur)
    return starts, durs, stages

def _from_txt_Twin(file_path, **kwargs):
    import pandas as pd
    stage_dict = {
        "STAGE - W": "W",
        "STAGE - N1": "N1",
        "STAGE - N2": "N2",
        "STAGE - N3": "N3",
        "STAGE - R": "REM",
        "STAGE - ?": "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    # whilst reading replace problematic characters with a placeholder
    df_ann = pd.read_csv(file_path, delimiter='\t', header=None, encoding='utf-8', encoding_errors='replace')
    check_start_rec = False
    start_hms_tmp = None
    # Iterate over DataFrame rows using itertuples()
    for index, row in df_ann.iterrows():
        if not check_start_rec and row[1]=="START RECORDING":
            start_rec = pd.to_datetime(row[0])
            check_start_rec = True
        if row[1] in stage_dict:
            if start_hms_tmp:
                dur = (pd.to_datetime(row[0]) - start_hms_tmp).seconds
                try:
                    assert dur % 30 == 0, "Discontinuity detected in the labels"
                except AssertionError as e:
                    # Raise an error if the assertion fails
                    raise ValueError(str(e))
                durs.append(dur)
            stage = stage_dict[row[1]]
            start_hms_tmp = pd.to_datetime(row[0])
            start = (start_hms_tmp - start_rec).seconds
            stages.append(stage)
            starts.append(start)
        if row[1] == "LIGHTS ON":
            dur = (pd.to_datetime(row[0]) - start_hms_tmp).seconds
            if dur < 30:
                stages = stages[:-1]
                starts = starts[:-1]
                continue
            if dur >= 30 and dur % 30 != 0:
                dur -= (dur % 30)
            durs.append(dur)
    return starts, durs, stages

def _from_xml_learn(file_path, **kwargs):
    import xml.etree.ElementTree as ET
    events = ET.parse(file_path).findall('SleepStages')
    assert len(events) == 1
    stage_dict = {
        "0": "W",
        "1": "N1",
        "2": "N2",
        "3": "N3",
        "4": "N3",
        "5": "REM",
        "6": "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    for i, event in enumerate(events[0]):
        if not event.text in stage_dict:
            continue
        stage = stage_dict[event.text]
        start = int(i * 30)
        dur = 30
        starts.append(start)
        durs.append(dur)
        stages.append(stage)
    return starts, durs, stages

def _from_xml_Compumedics(file_path, **kwargs):
    import xml.etree.ElementTree as ET
    events = ET.parse(file_path).findall('ScoredEvents')
    assert len(events) == 1
    stage_dict = {
        "Wake|0": "W",
        "Stage 1 sleep|1": "N1",
        "Stage 2 sleep|2": "N2",
        "Stage 3 sleep|3": "N3",
        "Stage 4 sleep|4": "N3",
        "REM sleep|5": "REM",
        "Movement|6": "UNKNOWN",
        "Unscored|9": "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    for event in events[0]:
        if not event[0].text == "Stages|Stages":
            continue
        stage = stage_dict[event[1].text]
        start = int(float(event[2].text))
        dur = int(float(event[3].text))
        starts.append(start)
        durs.append(dur)
        stages.append(stage)
    return starts, durs, stages

def _from_xml_Luna(file_path, **kwargs):
    import xml.etree.ElementTree as ET
    events = ET.parse(file_path).findall('Instances')
    assert len(events) == 1
    stage_dict = {
        "wake": "W",
        "NREM1": "N1",
        "NREM2": "N2",
        "NREM3": "N3",
        "NREM4": "N3",
        "REM": "REM",
        "unscored": "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    for event in events[0]:
        if not event.attrib['class'] in stage_dict:
            continue
        stage = stage_dict[event.attrib['class']]
        start = int(float(event[1].text))
        dur = int(float(event[2].text))
        starts.append(start)
        durs.append(dur)
        stages.append(stage)
    return starts, durs, stages

def extract_hyp_from_annot(file_path, **kwargs):
    """
    Extracts hypnograms from NSRR annot formatted annotation files.

    Returns:
        A StartDurationStageFormat object
    """
    import csv
    stage_dict = {
        "W": "W",
        "N1": "N1",
        "N2": "N2",
        "N3": "N3",
        "R": "REM",
        "?": "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        check_start_rec = False
        for row in csv_reader:
            if not check_start_rec and row['class'] in stage_dict:
                start_rec = pd.to_datetime(row['start'], format='%H:%M:%S')
                check_start_rec = True
            if row['class'] in stage_dict:
                stage = stage_dict[row['class']]
                start = (pd.to_datetime(row['start'], format='%H:%M:%S') - start_rec).seconds
                dur = (pd.to_datetime(row['stop'], format='%H:%M:%S')
                       - pd.to_datetime(row['start'], format='%H:%M:%S')).seconds
                if dur % 30 != 0:
                    break
                if start < 0 and not check_start_rec:
                    from shutil import copyfile
                    dts_dir = os.path.split(file_path)[0] + '_NegStartRec'
                    if not os.path.exists(dts_dir):
                        os.mkdir(dts_dir)
                    file_name = os.path.split(file_path)[1]
                    copyfile(file_path, os.path.join(dts_dir, file_name))
                    check_start_rec = True
                    continue
                stages.append(stage)
                starts.append(start)
                durs.append(dur)
        try:
            # Assert that the stages list is not empty
            assert stages, "The sleep stages list is empty! No annotations in file."
        except AssertionError as e:
            # Raise an error if the assertion fails
            raise ValueError(str(e))
    return StartDurationStageFormat((starts, durs, stages))

def extract_hyp_from_edf(file_path, **kwargs):
    """
    Loader for hypnogram stored in EDF files in the EDF Annotations channel.
    Uses BaseEDFReader from .dhedreader to extract the data as
    Start-Duration-Stage lists. Returns data of type StartDurationStageFormat.

    See wtfancy.hypnogram.formats.StartDurationStageFormat

    Returns:
        A StartDurationStageFormat object
    """

    # TODO - Add dictionary for sleep stages
    # e.g., stage_dict = {
    #     "Sleep stage W": "W",
    #     "Sleep stage N1": "N1",
    #     "Sleep stage N2": "N2",
    #     "Sleep stage N3": "N3",
    #     "Sleep stage R": "REM",
    #     "Sleep stage ?": "UNKNOWN",
    #     "Sleep stage 1": "N1",
    #     "Sleep stage 2": "N2",
    #     "Sleep stage 3": "N3",
    # }
    from .dhedreader import BaseEDFReader
    with open(file_path, "rb") as in_f:
        # Get raw header
        base_edf = BaseEDFReader(in_f)
        base_edf.read_header()
        ann = tuple(zip(*tuple(base_edf.records())[0][-1]))
    return StartDurationStageFormat(ann)

def extract_hyp_from_sta(file_path, **kwargs):
    """
    Extracts hypnograms from sta formatted annotation files.

    Returns:
        A StartDurationStageFormat object
    """
    import numpy as np
    stage_dict = {
        0: "W",
        1: "N1",
        2: "N2",
        3: "N3",
        4: "N3",
        5: "REM",
        6: "UNKNOWN",
        7: "UNKNOWN",
        8: "UNKNOWN",
        9: "UNKNOWN",
        10: "UNKNOWN"
    }
    starts, durs, stages = [], [], []
    ann = np.loadtxt(file_path)
    # Check continuity - Check if all differences are 1
    check_diff = np.diff(ann[:, 0])
    try:
        assert (check_diff == 1).all(), "Discontinuity detected in the labels"
    except AssertionError as e:
        # Raise an error if the assertion fails
        raise ValueError(str(e))
    for row in ann:
        stage = stage_dict[row[1]]
        start = int((row[0]-1)*30)
        dur = 30
        stages.append(stage)
        starts.append(start)
        durs.append(dur)
    return StartDurationStageFormat((starts, durs, stages))

def _from_nsrr_tsv(file_path, **kwargs):
    import csv
    start_rec_found = False
    stage_dict = {
        "Sleep stage W": "W",
        "Sleep stage N1": "N1",
        "Sleep stage N2": "N2",
        "Sleep stage N3": "N3",
        "Sleep stage R": "REM",
        "Sleep stage ?": "UNKNOWN",
        "Sleep stage 1": "N1",
        "Sleep stage 2": "N2",
        "Sleep stage 3": "N3",
    }
    starts, durs, stages = [], [], []
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        check_start_rec = False
        for row in csv_reader:
            if row['description'] == 'Start Recording' and not start_rec_found:
                start_rec = float(row['onset'])
                start_rec_found = True
            if row['description'][:11] == 'Sleep stage':
                # if not start_rec_found:
                #     raise ValueError("No Start Recording found!")
                stage = stage_dict[row['description']]
                start = round(float(row['onset']) - (start_rec if start_rec_found else 0))
                dur = round(float(row['duration']))
                try:
                    assert dur % 30 == 0, "duration must a multiple of 30"
                except AssertionError as e:
                    raise ValueError(str(e))
                if start < 0 and not check_start_rec:
                    from shutil import copyfile
                    dts_dir = os.path.split(file_path)[0] + '_NegStartRec'
                    if not os.path.exists(dts_dir):
                        os.mkdir(dts_dir)
                    file_name = os.path.split(file_path)[1]
                    copyfile(file_path, os.path.join(dts_dir, file_name))
                    check_start_rec = True
                    continue
                stages.append(stage)
                starts.append(start)
                durs.append(dur)
        try:
            # Assert that the stages list is not all with UNKNOWN annotations
            assert any(
                element != "UNKNOWN" for element in stages), "The sleep stages list contains only 'UNKNOWN' values"
        except AssertionError as e:
            # Raise an error if the assertion fails
            raise ValueError(str(e))
    return starts, durs, stages

def _from_bswr_tsv(file_path, **kwargs):
    import csv
    stage_dict = {
        "SLEEP-S0": "W",
        "SLEEP-S1": "N1",
        "SLEEP-S2": "N2",
        "SLEEP-S3": "N3",
        "SLEEP-S4": "N3",
        "SLEEP-?": "UNKNOWN",
        "SLEEP-REM": "REM"
    }
    starts, durs, stages = [], [], []
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            if row['trial_type'] in stage_dict:
                # Easy check for multiple series of stages
                if not starts:
                    ch_stages = row['channels']
                else:
                    if (round(float(row['onset'])) - starts[-1]) < 30 and ch_stages != row['channels']:
                        continue
                stage = stage_dict[row['trial_type']]
                start = round(float(row['onset']))
                dur = round(float(row['duration']))
                try:
                    assert start >= 0 and dur % 30 == 0, "start must be >= 0 and duration must a multiple of 30"
                except AssertionError as e:
                    raise ValueError(str(e))
                stages.append(stage)
                starts.append(start)
                durs.append(dur)
        try:
            # Assert that the stages list is not all with UNKNOWN annotations
            assert any(
                element != "UNKNOWN" for element in stages), "The sleep stages list contains only 'UNKNOWN' values"
        except AssertionError as e:
            # Raise an error if the assertion fails
            raise ValueError(str(e))
    return starts, durs, stages

def extract_hyp_from_tsv(file_path, **kwargs):
    """
    Extracts hypnograms from tsv formatted annotation files.

    Returns:
        A StartDurationStageFormat object
    """
    starts, durs, stages = [], [], []
    if os.path.basename(file_path).split('.')[-2].split('_')[-1] == 'events':
        starts, durs, stages = _from_bswr_tsv(file_path)
    else:
        starts, durs, stages = _from_nsrr_tsv(file_path)
    return StartDurationStageFormat((starts, durs, stages))

def extract_hyp_from_txt(file_path, **kwargs):
    """
    Extracts hypnograms from txt formatted annotation files.

    Returns:
        A StartDurationStageFormat object
    """
    starts, durs, stages = [], [], []
    if os.path.basename(file_path).split('.')[-2] == 'stg':
        starts, durs, stages = _from_txt_Gamma(file_path)
    elif os.path.basename(file_path).split('.')[-2] == 'allscore':
        starts, durs, stages = _from_txt_Twin(file_path)
    return StartDurationStageFormat((starts, durs, stages))

def extract_hyp_from_xml(file_path, **kwargs):
    """
    Extracts hypnograms from NSRR XML formatted annotation files.

    Returns:
        A StartDurationStageFormat object
    """
    import xml.etree.ElementTree as ET
    starts, durs, stages = [], [], []
    # TODO - nsrr learn setting or external db
    if ET.parse(file_path).findall('SoftwareVersion') == []:
        starts, durs, stages = _from_xml_learn(file_path)
    elif ET.parse(file_path).findall('SoftwareVersion')[0].text == 'Compumedics':
        starts, durs, stages = _from_xml_Compumedics(file_path)
    elif ET.parse(file_path).findall('SoftwareVersion')[0].text == 'luna-v0.23':
        starts, durs, stages = _from_xml_Luna(file_path)
    return StartDurationStageFormat((starts, durs, stages))

def extract_from_start_dur_stage(file_path, **kwargs):
    """
    Loader for CSV-like files that store hypnogram information in the
    Start-Duration-Stage format.
    See utime.hypnogram.formats.StartDurationStageFormat

    Returns:
        A StartDurationStageFormat object
    """
    import pandas as pd
    df = pd.read_csv(file_path, header=None)
    return StartDurationStageFormat(zip(*df.to_numpy()))


_EXT_TO_LOADER = {
    "annot": extract_hyp_from_annot,
    "edf": extract_hyp_from_edf,
    "ids": extract_from_start_dur_stage,
    "sta": extract_hyp_from_sta,
    "tsv": extract_hyp_from_tsv,
    "txt": extract_hyp_from_txt,
    "xml": extract_hyp_from_xml
}

def extract_ids_from_hyp_file(file_path, period_length_sec=None, sample_rate=None):
    """
    Entry function for extracting start-duration-stage format data from variable input files

    Args:
        file_path: str path to hypnogram file
        period_length_sec: integer or None - only used for loading ndarray data. If None, ndarray must be
                           dense (not signal-dense)
        sample_rate: integer or None - - only used for loading ndarray data. If None, ndarray must be
                     dense (not signal-dense)

    Returns:
        A StartDurationStageFormat object
    """
    extension = os.path.splitext(file_path)[-1].lower()[1:]
    return _EXT_TO_LOADER[extension](file_path=file_path,
                                     period_length_sec=period_length_sec,
                                     sample_rate=sample_rate)


def extract_ann_data(file_path, period_length_sec, annotation_dict, sample_rate):
    """
    Load annotations from a file at 'file_path'

    Returns:
        A AnnType object, annotation dict
    """

    # TODO add def for each annotation type AnnType object
    ids_tuple = extract_ids_from_hyp_file(file_path, period_length_sec, sample_rate)
    return sparse_hypnogram_from_ids_format(
        ids_tuple=ids_tuple,
        period_length_sec=period_length_sec,
        ann_to_class=annotation_dict
    )