# bs-crawler

Project skeleton generated by Crawlee (Beautifulsoup template).

## Usage

To get started, ensure you have [Poetry](https://python-poetry.org/), a package and dependency management system, installed on your machine. You can install it with the following command:

```sh
pip install poetry
```

Next, install the project dependencies:

```sh
poetry install
```

Finally, launch the crawler with:

```sh
poetry run python -m bs-crawler
```

This service will get scrape_requests from the `scrape-requests-subscription`. it will scrape the page and save the response to the `scraper-responses` bucket. This triggers a pubsub notification to the `scrape-responses-topic`. 



message sent to pubsub 
```json
{
  "kind": "storage#object",
  "id": "scraper-responses/01938823-0842-84bd-9d99-271570ab6365.json/1733155818279998",
  "selfLink": "https://www.googleapis.com/storage/v1/b/scraper-responses/o/01938823-0842-84bd-9d99-271570ab6365.json",
  "name": "01938823-0842-84bd-9d99-271570ab6365.json",
  "bucket": "scraper-responses",
  "generation": "1733155818279998",
  "metageneration": "1",
  "contentType": "text/plain",
  "timeCreated": "2024-12-02T16:10:18.287Z",
  "updated": "2024-12-02T16:10:18.287Z",
  "storageClass": "STANDARD",
  "timeStorageClassUpdated": "2024-12-02T16:10:18.287Z",
  "size": "629357",
  "md5Hash": "AN6sI8olmJOvsbD6l6ASyw==",
  "mediaLink": "https://storage.googleapis.com/download/storage/v1/b/scraper-responses/o/01938823-0842-84bd-9d99-271570ab6365.json?generation=1733155818279998&alt=media",
  "metadata": {
    "building_id": "12345"
  },
  "crc32c": "+ibZXg==",
  "etag": "CL6ojse8iYoDEAE="
}
```


Buildings on Rainey 
JSON
	- 700: https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524
	- Skyhouse: https://sightmap.com/app/api/v1/60p7q39nw7n/sightmaps/397
	- Camden: POST request 

```bash
https://www.camdenliving.com/_next/data/4kXFu0gMaS-hzENoMDlgs/apartments/austin-tx/camden-rainey-street/available-apartments.json?citySlug=austin-tx&communitySlug=camden-rainey-street
	- Quincy curl 'https://quincyatx.com/floorplans/' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.6' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'cookie: JonahLead=eyJyZWZlcnJlciI6InNlYXJjaC5icmF2ZS5jb20iLCJyZWZlcnJlcl91cmxfcXVlcnlzdHJpbmciOm51bGwsImN1cnJlbnRfdXJsX3F1ZXJ5c3RyaW5nIjoiIiwicHJvcGVydHlfaWRfaW5zdGFsbGVkIjp0cnVlfQ%3D%3D; PHPSESSID=41519e868bc35ec6838af82ccf810755' \
  -H 'origin: https://quincyatx.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://quincyatx.com/floorplans/' \
  -H 'sec-ch-ua: "Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw 'action=available-units&building=1'
```

HTML
	- 43 rainey windsor https://www.windsorcommunities.com/properties/windsor-on-the-lake/floorplans/

Zillow
48 east - https://www.zillow.com/b/48-east-ave-austin-tx-9LRMhF/
54 rainey Milago - https://www.zillow.com/b/54-rainey-st-austin-tx-5Xqvj9/
70 rainey