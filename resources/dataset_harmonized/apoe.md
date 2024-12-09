# Dataset: APOE

#### Extract command
```
extract --file_regex [LOCAL_PATH]/nsrr/apoe/original/PSG/*.EDF --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/apoe/ --resample 128 
--channels "C3/A2" "C4/A1" "O1/A2" "O2/A1" "LOC/A2" "ROC/A1" C3_A1 C3_A2 C3_O1 C4_A1 C4_A2 F1_A2 F2_C4 F2_T4 FP1_C3 Fp1_C3 FP2_C4 Fp2_C4 Fz_A1 Fz_A2 01_A2 O1_A2 O2_A1 T3_O1 T4_O2 LOC_A2 L_EOG R_EOG ROC_A1 LOC ROC Chin_EMG Chin2_EMG Chin_L Chin_R Chin_Ctr C3-A1 C3-A2 C3-O1 C4-A1 C4-A2 F1-A2 F2-C4 F2-T4 FP1-C3 Fp1-C3 FP2-C4 Fp2-C4 Fz-A1 Fz-A2 01-A2 O1-A2 O2-A1 T3-O1 T4-O2 LOC-A2 L-EOG R-EOG ROC-A1 Chin-EMG Chin2-EMG Chin-L Chin-R Chin-Ctr
--rename_channels C3-A2 C4-A1 O1-A2 O2-A1 LOC-A2 ROC-A1 C3-A1 C3-A2 C3-O1 C4-A1 C4-A2 F1-A2 F2-C4 F2-T4 FP1-C3 FP1-C3 FP2-C4 FP2-C4 Fz-A1 Fz-A2 O1-A2 O1-A2 O2-A1 T3-O1 T4-O2 LOC-A2 LOC ROC ROC-A1 LOC ROC Chin_EMG Chin2_EMG Chin_L Chin_R Chin_Ctr C3-A1 C3-A2 C3-O1 C4-A1 C4-A2 F1-A2 F2-C4 F2-T4 FP1-C3 FP1-C3 FP2-C4 FP2-C4 Fz-A1 Fz-A2 O1-A2 O1-A2 O2-A1 T3-O1 T4-O2 LOC-A2 LOC ROC ROC-A1 Chin-EMG Chin2-EMG Chin-L Chin-R Chin-Ctr --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/nsrr/apoe/original/PSG/*.STA --out_dir /MEDITECH/BSP/data/processed/PSG/wtf/apoe/ --dir_name " .STA" --fill_blanks "UNKNOWN" --seed 123 --overwrite
```

Notes: 
- scored sleep annotation files (.STA) are available for all subjects
- Not clear if O1_x and O2_x are occipital channels
- example nameing: APOE_0001