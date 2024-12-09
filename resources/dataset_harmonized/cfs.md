## Dataset: CFS

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/cfs/polysomnography/edfs/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/cfs/ --resample 128 --channels C3-A2 C4-A1 LOC-A2 ROC-A1 EMG1 EMG2 EMG3 --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/cfs/polysomnography/annotations-events-nsrr/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/cfs/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes:
- 1 group: 'visit5'
- example nameing: 'cfs-visit5-802593-famID{ID_REDACTED}'
                   'cfs-visit5-802626-famID{ID_REDACTED}'
- harmonized by NSRR (.xml)