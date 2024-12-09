<## Dataset: MROS

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/mros/polysomnography/edfs/visit*/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mros/ --resample 128 --channels C3-M2 C4-M1 E1-M2 E2-M1 E1 E2 LChin RChin "L Chin" "R Chin" "L_CHIN-R_CHIN" 
--rename_channels C3-M2 C4-M1 E1-M2 E2-M1 E1 E2 LChin RChin LChin RChin LChin-RChin --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/mros/polysomnography/annotations-events-nsrr/visit*/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mros/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes:
- 2 visits: 'visit1', 'visit2'
- example nameing: mros-visit1-aa5665, mros-visit2-aa5665
- harmonized by NSRR (.xml)