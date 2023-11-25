# CSCI596-Final-Project

This is the repository for the final project of CSCI596 Scientific Computing & Visualization at USC. The project is mainly about parallelizing the Locality Sensitive Hashing (LSH) algorithm.

## Development Plan

- Find the documents data.✅
- Generate document signature based on k-shingle.✅
- Reduce the dimensionality of signature with MinHash.
- Divide signatures in bands and hash to buckets respectively.
- Process candidate pairs (not sure).



## Preparation


Data source: [Text Documents classification](https://www.kaggle.com/datasets/jensenbaxter/10dataset-text-document-classification)



## Execution

1. Run this command to process data into json file.
```
python load_files.py
```

2. process the text into k-shingles with n processes.
```
mpiexec -n 4 python get_doc_features.py
```



## Analysis

Time vs. number of processes when computing signatures based on k-shingles.
| #process | Time (s) |
|-----|-----|
| 2 | 39.605998516082764 |
| 4 | 27.87109351158142 |
| 8 | 23.712995052337646 |
| 16 | 24.603995323181152 |