## Dataset: MSP

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/msp/polysomnography/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/msp/ --resample 128 --channels C3_M2 C4_M1 F3_M2 F4_M1 O1_M2 O2_M1 LOC ROC EMG1 EMG2
--rename_channels C3-M2 C4-M1 F3-M2 F4-M1 O1-M2 O2-M1 LOC ROC EMG1 EMG2 --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/abc/polysomnography/*.annot --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/msp/ --dir_name " .annot" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes:
- example nameing: msp-S003
- harmonized by NSRR (.edf and .annot)