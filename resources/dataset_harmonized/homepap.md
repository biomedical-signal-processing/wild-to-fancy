## Dataset: HOMEPAP

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/homepap/polysomnography/edfs/lab/*/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/homepap/ --resample 128 --channels F4-M1 C4-M1 O2-M1 C3-M2 F3-M2 O1-M2 F4 C4 O2 C3 F3 O1 E1 E1-M2 E_1-M2 L-EOG E2 E2-M1 E_2-M1 R-EOG E1-E2 chin Cchin Lchin Rchin Rchon LCHIN-CCHIN 
--rename_channels F4-M1 C4-M1 O2-M1 C3-M2 F3-M2 O1-M2 F4 C4 O2 C3 F3 O1 E1 E1-M2 E1-M2 LOC E2 E2-M1 E2-M1 ROC E1-E2 Cchin Cchin Lchin Rchin Rchin Lchin-Cchin --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/homepap/polysomnography/annotations-events-nsrr/lab/*/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/homepap/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- (a) laboratory-based and (b) home-based
- 2 lab-based group: 'full', 'split'
- example nameing: 'homepap-lab-full-1600039',
                   'homepap-lab-split-1600150'
- harmonized by NSRR (.xml)