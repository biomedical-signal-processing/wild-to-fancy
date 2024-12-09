## Dataset: MESA

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/mesa/polysomnography/edfs/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mesa/ --resample 128 --channels EEG1 EEG2 EEG3 EOG-L EOG-R EMG 
--rename Fz-Cz Cz-Oz C4-M1 E1-FPz E2-FPz EMG --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/mesa/polysomnography/annotations-events-nsrr/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mesa/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 1 group: 'sleep'
- example nameing: 'mesa-sleep-5805'
- harmonized by NSRR (.xml)