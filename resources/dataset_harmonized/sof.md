## Dataset: SOF

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/sof/polysomnography/edfs/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/sof/ --resample 128 --channels C3-A2 C4-A1 LOC-A2 ROC-A1 "L Chin" "R Chin" "EMG/L" "EMG/R" 
--rename_channels C3-A2 C4-A1 LOC-A2 ROC-A1 LChin RChin LChin RChin --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/sof/polysomnography/annotations-events-nsrr/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/sof/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 1 group: 'visit8'
- example nameing: 'sof-visit-8-07853'
- harmonized by NSRR (.xml)