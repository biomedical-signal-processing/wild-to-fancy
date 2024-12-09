## Dataset: SHHS

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/shhs/polysomnography/edfs/shhs*/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/shhs/ --resample 128 --channels "EEG" "EEG(sec)" "EEG_SEC" "EEG_2" "EEG2" "EOG(L)" "EOG(R)" "EMG" 
--rename_channels "C4-A1" "C3-A2" "C3-A2" "C3-A2" "C3-A2" "EOG(L)-PG1" "EOG(R)-PG1" "EMG" --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/shhs/polysomnography/annotations-events-nsrr/shhs*/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/shhs/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 2 visits: 'shhs1', 'shhs2'
- example nameing: 'shhs1-205238', 'shhs2-205238'
- harmonized by NSRR (.xml)