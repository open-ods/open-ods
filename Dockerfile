FROM ubuntu:16.04

ENV DATABASE_URL postgresql://openods:openods@openods-postgres:5432/openods
ENV CACHE_TIMEOUT 30
ENV APP_HOSTNAME localhost:8080/api
ENV API_PATH /api
ENV LIVE_DEPLOYMENT FALSE
ENV INSTANCE_NAME Development
ENV FT_SUPPRESSPRIMARYROLESEARCHLINK ""

RUN apt-get update && apt-get install -y python3 python3-pip  python3-all-dev postgresql-server-dev-all memcached python-pylibmc libmemcached-dev libxml2 libxml2-dev libxslt-dev

# Set up a user for the code to run as
RUN groupadd -r openods -g 1000 && \
    useradd -u 1000 -r -g openods openods

# Copy code into container
COPY requirements.txt /openods/
COPY openods /openods/openods/

# Install python modules
RUN pip3 install --upgrade pip
RUN pip3 install -r /openods/requirements.txt
RUN pip3 install gunicorn

# Give our user permissions for the code directory
RUN chown -R openods:openods /openods

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 8080/tcp

# We want this container to run without root priviledges
USER openods

ENTRYPOINT ["/entrypoint.sh"]

