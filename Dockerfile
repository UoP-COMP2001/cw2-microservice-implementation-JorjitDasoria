
FROM python:3.9-bullseye

# Install Microsoft SQL Server requirements
ENV ACCEPT_EULA=Y
RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc unixodbc-dev odbcinst

# Add SQL Server ODBC Driver 17 for Debian
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Set working directory
WORKDIR /app

# Copy all files to /app directory
COPY . .

# Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Clean up to reduce image size
RUN apt-get -y clean

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
