# Use the official Python image from the Docker Hub
FROM python:3.11.5

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt requirements.txt

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the project files to the container's working directory
COPY . .

# Run the script to initialize or set up the database connection
# RUN python src/connectdb_sqlite.py

# Expose the port your app runs on (if applicable)
EXPOSE 8501

# Command to run your application
CMD ["streamlit", "run", "src/home.py"]

