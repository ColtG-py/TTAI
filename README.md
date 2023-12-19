## Replace
1. gen_data.py, L3 API key with your own.
2. datasets/ttr-obj-detect-2/data.yml L20 - 22 with path to train, test, and valid.

## Run Order
`pip install -r requirements.txt`

`python gen_data.py`

`python train.py`

`python run.py`
