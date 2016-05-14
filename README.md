## Pyblog
Pyblog is a asynchronous web framework that base on aiohttp

## Get Started
```python
from pyblog.httptools import Route
from pyblog.application import Application

@Route.get("/")
def index_handler(app):
	app.render("index.html")
	
app=Application()
app.run()
```
## Updating.....
