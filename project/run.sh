echo "Make sure you've set the correct DB URL in .env and alembic.ini"
alembic upgrade head
python3 app/main.py
# alembic revision -m "Message"
