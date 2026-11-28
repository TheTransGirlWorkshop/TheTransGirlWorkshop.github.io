# TheTransGirlWorkshop.github.io

Official website for The Trans Girl Workshop — games, Discord bots, mods, tools and experimental projects.

This repository is the public static website only. Private project source code is kept elsewhere.

## Publishing catalogue changes

Edit `.github/site/catalogue.json` for product names, descriptions, prices, status and listings. Run `python .github/site/render.py` from the repository checkout, then review and commit the generated pages and feeds with the change. Product article layouts and longer supporting copy live in `.github/site/articles.json`. The Launcher feed keeps the client’s existing operational fields, including the legacy release and playtest flags, and publishes the catalogue display status separately.
