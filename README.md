# Jobs board web scrapping

Main goal is to scrap multiple job boards and looks for desired key worlds.
Selenium (with Firefox geckodriver) is used as a web browser engine.
Celery workers and celery beat is used to fire the web engine.
RabbitMQ is used as message broker for Celery.


To start the project:
```
docker-compose up -d app-backend
```

All required migrations should be applied, some init data loaded. `https://indeed.com` has been used 
as an example job board.

## DB Models 
Job Offers - found job offers.
Providers - job board from which data should be scrapped from.
Scrapping process:
- key words - words that should be imputed into board search bar
- selectors - CSS selectors that should be used in the scrapping process to look for desired elements
- scrapping steps - steps for a given scrapping process. Steps define actions that Web Engnine should perform. It's possible to customize each step so it works for different job boards
- scrapping process - process defined for a given provider (job board), consists of a scrapping steps
