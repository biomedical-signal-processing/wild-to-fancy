# Dataset: APPLES

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/apples/polysomnography/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/apples/ --resample 128 --channels C3_M2 C4_M1 O1_M2 O2_M1 E1 E2 EMG EEG_C3_A2 EEG_C4_A1 EEG_O1_A2 EEG_O2_A1 EOG_Left EOG_Right EMG_Chin 
--rename_channels C3-M2 C4-M1 O1-M2 O2-M1 LOC ROC EMG C3-M2 C4-M1 O1-M2 O2-M1 LOC ROC EMG --seed 123 -overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/apples/polysomnography/*.annot --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/apples/ --dir_name " .annot" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- subjects with PSG data from the diagnostic visit (DX)
- 7 but no more than 9 hours in bed
- example nameing: apples-130001
- harmonized by NSRR (.edf and .annot)