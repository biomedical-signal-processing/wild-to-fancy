## Dataset: MNC

#### Extract commands (one command for each sub-cohort)
```
extract --file_regex [LOCAL_PATH]/nsrr/mnc/cnc/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mnc_cnc/ --resample 128 --channels C3-M2 C3 C4-M1 C4 Cz F3-M2 F3 F4-M1 F4 O1-M2 O1 O2-M1 O2 E1-M2 E1 E2-M1 E2 cchin cchin_l chin --seed 123 --overwrite --del_nsrr_names
extract --file_regex [LOCAL_PATH]/nsrr/mnc/dhc/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mnc_dhc/ --resample 128 --channels C3-M2 C3 C4-M1 C4 Cz F3-M2 F3 F4-M1 F4 O1-M2 O1 O2-M1 O2 E1-M2 E1 E2-M1 E2 cchin cchin_l chin --seed 123 --overwrite --del_nsrr_names
extract --file_regex [LOCAL_PATH]/nsrr/mnc/ssc/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mnc_ssc/ --resample 128 --channels C3-M2 C3 C4-M1 C4 Cz F3-M2 F3 F4-M1 F4 O1-M2 O1 O2-M1 O2 E1-M2 E1 E2-M1 E2 cchin cchin_l chin --seed 123 --overwrite --del_nsrr_names
```

#### Extract hypno commands (one command for each sub-cohort)
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/mnc/cnc/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mnc_cnc/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
extract_hypno --file_regex [LOCAL_PATH]/nsrr/mnc/dhc/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mnc_dhc/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
extract_hypno --file_regex [LOCAL_PATH]/nsrr/mnc/ssc/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/mnc_ssc/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 7 cohorts: (3 with annotations) 'cnc', 'dhc', 'ssc' - (4 without annotations) 'fhc', 'ihc', 'is-rc', 'khc'
- example nameing: chc001-nsrr, N0020-nsrr, Sub01-nsrr, ssc_1558_1-nsrr
- harmonized by NSRR (.edf, .eannot, .xml)