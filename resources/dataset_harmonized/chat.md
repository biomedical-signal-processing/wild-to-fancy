## Dataset: CHAT

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/chat/polysomnography/edfs/*/*.edf --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/chat/ --resample 128 --channels F3-M2 F4-M1 C3-M2 C4-M1 T3-M2 T4-M1 O1-M2 O2-M1 E1-M2 E2-M1 E1 E2 Cchin Lchin Rchin LCHIN-RCHIN 
--rename_channels F3-M2 F4-M1 C3-M2 C4-M1 T3-M2 T4-M1 O1-M2 O2-M1 E1-M2 E2-M1 E1 E2 Cchin Lchin Rchin Lchin-Rchin --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/chat/polysomnography/annotations-events-nsrr/*/*.xml --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/chat/ --dir_name " -nsrr.xml" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- 3 groups: 'baseline', 'followup', 'nonrandomized'
- example nameing: 'chat-baseline-300001', 'chat-followup-300001'
                   'chat-nonrandomized-300004'
- harmonized by NSRR (.xml)

