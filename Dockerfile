# Source Image
FROM python:3.7
# Author
MAINTAINER Leon "leontian1024@gmail.com"
# Set working director
WORKDIR /var/app/microFaultInjection
# Add source code from os into container
Add . /var/app/microFaultInjection
# Import packages
RUN pip install Flask
RUN pip install Flask-wtf
RUN pip install flask-bootstrap
# Update Source list
RUN rm -rf /etc/apt/sources.list
Add /etc/apt/sources.list /etc/apt
# Get Linux Commands
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated stress
RUN apt-get install -y --allow-unauthenticated iperf3
# Expose port
EXPOSE 5000
# Run command
ENTRYPOINT ["python","./webServer.py"]