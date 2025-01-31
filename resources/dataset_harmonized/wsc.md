## Dataset: WSC

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/wsc/polysomnography/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/wsc/ --resample 128 --channels F3_M1 F3_M2 F3_AVG F4_M1 F4_M2 F4_AVG Fz_M1 Fz_M2 Fz_AVG Cz_M1 Cz_M2 Cz_AVG C3_M1 C3_M2 C3_AVG C4_M1 C4_M2 C4_AVG Pz_M1 Pz_M2 Pz_AVG Pz_Cz O1_M1 O1_M2 O1_AVG O2_M1 O2_M2 O2_AVG E1 E2 chin cchin_l cchin_r rchin_l 
--rename_channels F3-M1 F3-M2 F3-AVG F4-M1 F4-M2 F4-AVG Fz-M1 Fz-M2 Fz-AVG Cz-M1 Cz-M2 Cz-AVG C3-M1 C3-M2 C3-AVG C4-M1 C4-M2 C4-AVG Pz-M1 Pz-M2 Pz-AVG Pz-Cz O1-M1 O1-M2 O1-AVG O2-M1 O2-M2 O2-AVG E1 E2 chin cchin_l cchin_r rchin_l --seed 123 --overwrite --del_substring
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/wsc/polysomnography/*stg.txt --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/wsc/ --dir_name " -nsrr.stg.txt" --fill_blanks "UNKNOWN" --seed 123 --overwrite
extract_hypno --file_regex [LOCAL_PATH]/nsrr/wsc/polysomnography/*allscore.txt --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/wsc/ --dir_name " -nsrr.allscore.txt" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 5 visits: 'visit 1', 'visit 2', 'visit 3', 'visit 4', 'visit 5'
- 1,123 recordings at Visit 1; 758 recordings at Visit 2; 566 recordings at Visit 3; 121 recordings at Visit 4; 2 recordings at Visit 5
- example nameing: wsc-visit1-10119, wsc-visit2-2987, wsc-visit5-79657
- nsrr.stg.txt or nsrr.allscore.txt format staging