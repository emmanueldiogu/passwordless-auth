FROM python:3.10

# Any python command would be written into this folder
ENV PYTHONUNBUFFERED=1

# Working directory called app
WORKDIR /app

# Install pipenv
RUN pip install --upgrade pip 
RUN pip install pipenv

# Copy and Install application dependencies
COPY Pipfile Pipfile.lock /app/

# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments. 
RUN pipenv install --system --dev

# Copy the application files into the image
COPY . /app/