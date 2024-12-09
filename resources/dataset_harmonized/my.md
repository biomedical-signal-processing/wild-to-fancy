## Dataset: EXT

#### Extract command
```
extract --file_regex [LOCAL_PATH]/tutorial/edfs/*.edf --out_dir [LOCAL_PATH]/tutorial/external/ --resample 128 --select_types EEG EOG MASTOID --auto_reference_types None --use_my_files --seed 123 --overwrite
```

#### Extract hypno command
```
extract_hypno --file_regex [LOCAL_PATH]/tutorial/edfs/*.xml --out_dir [LOCAL_PATH]/tutorial/my/ --dir_name " .xml" --fill_blanks "UNKNOWN" --use_my_files --seed 123 --overwrite
```