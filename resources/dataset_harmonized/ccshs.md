## Dataset: CCSHS

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/ccshs/polysomnography/edfs/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/ccshs/ --resample 128 --channels C3-A2 C4-A1 LOC-A2 ROC-A1 EMG1 EMG2 EMG3 --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/ccshs/polysomnography/annotations-events-nsrr/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/ccshs/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 1 group: 'trec' (study has 3 longitudinal visits, but only 'trec' is published currently)
- example nameing: 'ccshs-trec-1800005'
- harmonized by NSRR (.xml)