## Dataset: NCHSDB

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/nchsdb/sleepdata/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/nchsdb/ --resample 128 
--channels FP1 FP2 FZ CZ PZ OZ FPZ P3-M2 P4-M1 F3-M2 F4-M1 C3-M2 C4-M1 T3-M2 T4-M1 O1-M2 O2-M1 E1-M2 E2-M1 E1 E2 'EEG F4-M1' 'EEG F3-M2' 'EEG C4-M1' 'EEG C3-M2' 'EEG O2-M1' 'EEG O1-M2' EOG_LOC-M2 EOG_ROC-M1 EMG_CHIN1-CHIN2 EEG_F4-EEG_M1 EEG_F4-M2 EEG_F3-EEG_M2 EEG_C4-EEG_M1 EEG_C4-M2 EEG_C3-EEG_M2 EEG_O2-EEG_M1 EEG_O1-EEG_M2 EOG_LOC-EEG_M2 EOG_ROC-EEG_M1 EMG_CHIN1-EMG_CHIN2 CHIN1 CHIN2 CHIN3 EEG_CHIN1 EEG_CHIN2 EEG_CHIN3 EMG_CHIN1-CHIN3 EEG_CHIN1-CHIN3 EEG_CHIN1-CHIN2 EEG_CHIN3-CHIN2 EEG_ROC-M1 EEG_ROC-M2 EEG_LOC-M1 EEG_LOC-M2 EEG_E1 EEG_E2
 --rename_channels FP1 FP2 FZ CZ PZ OZ FPZ P3-M2 P4-M1 F3-M2 F4-M1 C3-M2 C4-M1 T3-M2 T4-M1 O1-M2 O2-M1 E1-M2 E2-M1 E1 E2 F4-M1 F3-M2 C4-M1 C3-M2 O2-M1 O1-M2 E1-M2 E2-M1 CHIN1-CHIN2 F4-M1 F4-M2 F3-M2 C4-M1 C4-M2 C3-M2 O2-M1 O1-M2 E1-M2 E2-M1 CHIN1-CHIN2 CHIN1 CHIN2 CHIN3 CHIN1 CHIN2 CHIN3 CHIN1-CHIN3 CHIN1-CHIN3 CHIN1-CHIN2 CHIN3-CHIN2 E2-M1 E2-M2 E1-M1 E1-M2 E1 E2 --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/nchsdb/sleepdata/*.tsv --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/nchsdb/ --dir_name " .tsv" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 1 group
- example nameing: (STUDY_PAT_ID)_(SLEEP_STUDY_ID) 
                   '10000_17728'
- harmonized by ?NSRR? (.edf, .annot, .tsv)