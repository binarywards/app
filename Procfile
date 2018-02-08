release: python create_config.py
web: gunicorn --worker-class eventlet -w 1 binarywards:app --log-file=logs/gunicorn.log