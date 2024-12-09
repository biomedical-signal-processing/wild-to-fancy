## Dataset: PHYS

#### Extract command
```
ut extract --file_regex '[LOCAL_PATH]/phys/tr*/*.mat' --out_dir [LOCAL_PATH]/processed/phys/ --resample 128 --channels F3-M2 F4-M1 C3-M2 C4-M1 O1-M2 O2-M1 E1-M2
```

#### Extract hypno command
```
ut extract_hypno --file_regex '[LOCAL_PATH]/phys/tr*/*HYP.ids' --out_dir '[LOCAL_PATH]/processed/phys/'
```

Notes:
- No subject relations specified
- example nameing: 'tr13-0566'
- match regex: None