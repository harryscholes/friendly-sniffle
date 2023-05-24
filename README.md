# friendly-sniffle

## Setup

```
conda create -n friendly-sniffle python=3.11
conda activate friendly-sniffle
pip install -r requirements.txt
```

## Testing

```
pytest
```

## Running

- Obtain a Covalent API key and set it to `COVALENT_API_KEY` as an environment variable, optionally in a `.env` file.
- Run:

```
# Development
hypercorn app/main:app --reload

# Production
hypercorn app/main:app
```
