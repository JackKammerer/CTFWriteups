# Use an official Python runtime as an image
FROM python:3.9

# Sets the working directory for following COPY and CMD instructions
WORKDIR /chal

# Install any needed packages specified in requirements.txt
COPY requirements.txt /chal/
RUN pip install -r requirements.txt

COPY bot.py /chal/
COPY flag.txt /chal/

CMD ["python3", "bot.py"]
