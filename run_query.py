import sqlite3


conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

with open('query.sql', 'r') as f:
    query = f.read()
    cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
{
  "cells": [],
  "metadata": {
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}