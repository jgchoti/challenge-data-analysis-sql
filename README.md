# Data Analysis with SQL

Welcome to the Data Analysis with SQL challenge! This project is part of my earning journey with BeCode to shraping SQL skills and apply them to real-world data analysis scenarios.

## Overview

This repository contains a collection of SQL queries and analyses performed on a SQL database containing information about active companies in Belgium. The goal is to extract meaningful business insights that can help the company grow.
Note that these data come from [public open data](https://economie.fgov.be/en/themes/enterprises/crossroads-bank-enterprises/services-everyone/public-data-available-reuse/cbe-open-data)

## 🛠️ `main.py` – Database Preparation Script

This script creates and modifies tables in the SQLite database.

Features:

- Creates tables from raw CSV or cleaned data
- Alters tables to add new columns or calculated fields
- Prepares a structured database ready for analysis

💡 Run this file first to ensure the database is correctly set up.

## 📓 `analysis.ipynb` – Jupyter Notebook for Graphs

This notebook contains SQL queries and analyses to explore the database.
Includes:

- Line charts, bar charts, pie charts to show trends and distributions
- Grouping by sector, region, legal form, year, etc.
- Filtering for top categories and aggregating small groups into "Other"

🔍 Ideal for data exploration, presentation, or insights generation.
