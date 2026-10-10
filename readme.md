
## 1. Create venv
```
python -m venv cs_statistics
```

## 2. Activate venv

```
source cs_statistics/bin/activate
```

```
cs_statistics\Scripts\Activate.ps1
```

```
cs_statistics\Scripts\activate.bat
```

## 3. Install requirements

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Download data

```
python src/scripts/get_raw_data.py
```