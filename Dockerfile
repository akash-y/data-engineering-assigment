FROM python:3.8.1-buster
COPY . /src

#Install the Microsoft ODBC driver for MacOS
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 

RUN apt-get update
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN apt-get install mssql-tools unixodbc-dev -y

RUN apt-get update && apt-get install -my wget gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Install the Microsoft ODBC driver for SQL Server (Linux)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/msprod.list


#Download the desired package(s)
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.2-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.apk


#(Optional) Verify signature, if 'gpg' is missing install it using 'apk add gnupg':
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.2-1_amd64.sig
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.sig

#Install the package(s)
RUN sudo apk add --allow-untrusted msodbcsql17_17.5.2.2-1_amd64.apk
RUN sudo apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk

RUN curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import - \
gpg --verify msodbcsql17_17.5.2.2-1_amd64.sig msodbcsql17_17.5.2.2-1_amd64.apk \
gpg --verify mssql-tools_17.5.2.1-1_amd64.sig mssql-tools_17.5.2.1-1_amd64.apk


#Install the package(s)
RUN sudo apk add --allow-untrusted msodbcsql17_17.5.2.2-1_amd64.apk
RUN sudo apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk


#Runnig main files 
RUN pip install -r /src/requirements.txt
CMD ["python", "/src/main.py"] 

