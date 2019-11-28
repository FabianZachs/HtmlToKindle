FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -y xvfb libfontconfig wkhtmltopdf
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "toKindle.py"]
