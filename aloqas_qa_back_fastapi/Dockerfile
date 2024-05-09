FROM python:3.10

# Copy the current directory contents into the container at .
COPY . .

# Set the working directory to /
WORKDIR /

# Install requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN mkdir ./.cache
RUN touch user
RUN chmod -R 777 ./.cache

# Start the FastAPI app on port 7860, the default port expected by Spaces
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
