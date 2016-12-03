FROM postgres:9.6

COPY data.sql /data/data.sql
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV DB openods
ENV DB_USER openods
ENV DB_PASSWORD openods
ENV DROP_EXISTING true

# Entrypoint script to run the data load
ENTRYPOINT ["/entrypoint.sh"]

