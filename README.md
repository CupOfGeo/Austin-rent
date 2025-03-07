# Austin Rent

This project will scrape the rents prices form buildings on Rainey St in Austin Tx. The goal of this project will be to product a nice data visualization for reddit.
This project is more of a devops project than a software project. Ideal I would have an org in a box with a real production best practices.

## The One Repo To Rule Them All (ORTRTA)

this is the common read me that will spread standards across multiple repos

Main Mermaid diagram

```mermaid
```

## Pre-Commit hooks

install deps
[TFlint](https://github.com/terraform-linters/tflint)
[Trivy](https://github.com/aquasecurity/trivy)

```bash
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin v0.58.1
```

## Github actions

We use github actions but bc we are running a (ORTRTA). You have to manually trigger it and specify the app name so we don't rebuild and deploy ever app on push to main.

Folder name dictates app name same as cloud run name

### Linter

to run locally use

```bash
docker run --platform linux/amd64 -e DEFAULT_BRANCH=main -e SHELL=/bin/bash \
  -e LOG_LEVEL=DEBUG \
  -e RUN_LOCAL=true \
  -v ~/Code/AustinRent:/tmp/lint \
  --rm \
  ghcr.io/super-linter/super-linter:latest
```

## Database

Postgres dbs
[naming conventions](https://gist.github.com/kyledcline/9b7e864b89c269beb2c34e55fb0903b0)

naming convention.
    - underscores for table_name
    - PK should be table_name_id

Connecting to CloudSQL
[gcp docs](https://cloud.google.com/sql/docs/mysql/connect-auth-proxy)
Note: if you are in a dev container use linux 64. Then move it to `mv cloud-sql-proxy ~/.local/bin/`

```bash
./cloud-sql-proxy --address 0.0.0.0 --port 5432 austin-rent:us-central1:austin-rent-db
```

## Secrets

So I have updated this a few times.
I have created the key with this command and set it as the gh secret.
`age-keygen -o secrets/austin-rent-key.txt`
Public key: age1phl53gymlk2rt5fwvdvyeds30w73slkgj8trs6c5nkdf43wzkd2s2mdfx0
`gh secret set AUSTIN_RENT_KEY < secrets/austin-rent-key.txt`

Ok so i just caved and did this for the flyway migration. Probably for the best to just use the gh secretes.
`gh secret set SCRAPER_APP_PASSWORD < secrets/.env`

## Creating a new secret

get the value from [secret manager](https://console.cloud.google.com/security/secret-manager/secret/manual-private-key/versions?project=austin-rent)
`echo 'export AR_PUBLIC_KEY=age1phl53gymlk2rt5fwvdvyeds30w73slkgj8trs6c5nkdf43wzkd2s2mdfx0' >> ~/.zshrc`

Now we can do
`echo "your-secret-value" | age -r $AR_PUBLIC_KEY | base64`

Then you can put them in the respective config yaml `/scraper/scraper/configs/dev.yaml`

```yaml
secrets:
  TEST: YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBTa1RkTEVZZWdEbnI1Rmgyb2RzdEc3L1hkWXozYWk5RkZmMlk5TUpFSWljCm9ldTJBN2xEYXlFaFdiNmJsUXR4eklxTllBV2JjTi9Yb2czTUxrRElnWmsKLS0tIDNYbWNvNnFUeDFrb2VZZ3FCcGsyOWNtZ25hQXMrWi91cGY5endYeGo2UlEK61yW+mYcM0my9NH6B2X3o2L3CfCNveVXm9PtV5V/0R7w2Ue2aWUrrEUL3SXEwSNIMAQ=
env_vars:
  ENVIRONMENT: DEV
```

They will be decrypted at the start of runtime see `/scraper/scraper/config/secret_manager.py`

Then see `/opentofu_repo/scraper-module/compute.tf` was granted access to read that secret.

First attempt was making gcp secrets with gcloud cli and then retrieving them with python. This got better when I used tofu to create the secrets. One draw back using it in python was circular imports from the settings so i have to still hard code the gcp project. worked fine when the only thing was the db password but now i want to add the db public ip. I don't wanna make a whole tofu thing for it. Now im going to use [age](https://github.com/FiloSottile/age) so we can encrypt values with public keys then decrypt them at runtime.

## Notes

Lets build something that scrapes rent prices on Rainey street and uploads them to a database.

My initial idea of the system.

- Well we gotta start with a list of urls somewhere. Maybe they live in a database
    [https://700river.com/floorplans/, https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524, ...]

- Well have a cron job that will basically just select everything from that database and publish messages to a scrape service

- well make requests to them for now http should be fine and we shouldn't worry about cloning the browser with playwright. This should be its own service that we send messages (url) to and it will save the response to a bucket and pass that id on as a message to

- Extraction service this will given a page and a complex page extract the relevant fields we want from the scraped response. Should be relatively generic so that we can just create new configs per complex (*thinking maybe should do by address*). then save the extraction to the database. if the extraction fails we should save a failed. well have the original scraped response saved to the bucket so we could reprocess it if its a valid page.

Simple One service to rule them all.

- List is hard coded into they code
- We also do parsing in the code
- save it to the db from here

<https://github.com/apify/crawlee-python>
