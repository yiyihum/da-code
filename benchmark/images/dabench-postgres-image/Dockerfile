FROM python:3.9

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    postgresql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip install --upgrade pip

RUN pip install google-cloud-bigquery db-dtypes pandas matplotlib scikit-learn seaborn numpy scipy statsmodels xgboost plotly tabulate snowflake-connector-python duckdb

COPY init.sh .

RUN chmod +x init.sh && ./init.sh

WORKDIR /workspace

# Set the default command to run when starting the container
CMD ["/bin/bash"]
