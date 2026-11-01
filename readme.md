
## 1. Create venv
```
python -m venv cs_statistics_venv
```

## 2. Activate venv

```
source cs_statistics_venv/bin/activate
```

```
cs_statistics_venv\Scripts\Activate.ps1
```

```
cs_statistics_venv\Scripts\activate.bat
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