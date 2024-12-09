## Dataset: SEDF-SC

#### Extract command
```
ut extract --file_regex '[LOCAL_PATH]/sleep-edf-extended/SC*/*PSG.edf' --out_dir '[LOCAL_PATH]/processed/sedf-sc/' --resample 128 --channels 'EEG Fpz-Cz' 'EEG Pz-Oz' 'EOG horizontal' --rename Fpz-Cz Pz-Oz EOG
```

#### Extract hypno command
```
ut extract_hypno --file_regex '[LOCAL_PATH]/sleep-edf-extended/SC*/*Hypnogram.edf' --out_dir '[LOCAL_PATH]/processed/sedf-sc/'
```

Notes: 
- Two sleep studies made on each subject (The first nights of subjects 36 and 52, and the second night of subject 13, were lost due to a failing cassette or laserdisk.)
- 2 groups, Files are named in the form SC4ssNEO-PSG.edf where 'ss' is the subject number, and 'N' is the night.
- example nameing: 'SC4801G0-PSG', 'SC4802G0-PSG' 
- match regex: 'SC4(\d{2}).*'