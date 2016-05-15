## Pyblog
Pyblog is a asynchronous web framework that base on aiohttp

## Get Started
```python
from pyblog import Route
from pyblog import Application

@Route.get("/")
def index_handler(app):
	app.render("index.html")
	
app=Application()
app.run()
```
## Updating.....
