# XXL availability scraper

This scraper performs one check per run. It stores the availability status for
each product in `data/elements.json` and emails when the status changes from
`Ikke tilgjengelig online`.

Before running it, replace the example URL in `input/searches.yaml` with the
XXL product URL. Put the sender password in `.email_pwd`, then run:

```sh
pipenv install
pipenv run python xxl-scraper.py
```

The scraper imports the shared utilities from `../python-tools`, matching the
existing scraper projects in this workspace.