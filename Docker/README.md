# Running OpenODS in Docker

To deploy OpenODS in Docker, follow the below instructions:

## Running on a local machine

To build and deploy on a local machine running Docker, from this directory - first, set up a directory to hold the postgres data:

```bash
mkdir /docker-data/openods-postgres-data
chown -R 1000:1000 /docker-data/openods-postgres-data
```

Note: If you have user namespacing set up in your docker daemon (a good idea for live servers), then you will need to set the permissions accordingly. For example, if your /etc/subuid and /etc/subgid files contains this line:

```bash
dockremap:165536:65536
```

Then you will need to set the owner of the data directory to be 1000+165536 (166536):

```bash
chown -R 166535:165536 /docker-data/openods-postgres-data
```

Currently, the data importer has not been set up for use in Docker, so you will need to download a dump of the postgres data:

```bash
cd ~
wget https://s3.amazonaws.com/openods-assets/database_backups/openods009_3.dump
```

Now, you can start a a postgres container, and load the data into it:

```bash
USER=myuser PASSWORD=12345 ./deploy-postgres.sh
USER=myuser PASSWORD=12345 ./import-data.sh ~/openods009_3.dump
```

And then start the API container:

```bash
./build-openods.sh
USER=myuser PASSWORD=12345 ./deploy-openods.sh
```

Now test it by visiting http://localhost:8083/

Enjoy!

