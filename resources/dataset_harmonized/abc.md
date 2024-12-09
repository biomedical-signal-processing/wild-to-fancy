## Dataset: ABC

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/abc/polysomnography/edfs/*/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/abc/ --resample 128 --channels F3-M2 F4-M1 C3-M2 C4-M1 O1-M2 O2-M1 E1-M2 E2-M1 Chin1 Chin2 Chin3 --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/abc/polysomnography/annotations-events-nsrr/*/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/abc/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 3 visits: 'baseline', 'month09', 'month18'
- example nameing: abc-baseline-900001, abc-month18-900001, abc-month09-900001
- harmonized by NSRR (.xml)