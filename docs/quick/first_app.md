# Creating your first zenaura app

In this example we will go over creating your first zenaura application, go over basic concepts as well. 

Once you installed the library, the library, it comes with simple CLI tool.

#### CLI Commands:
    - init: Will create simple zenaura application
    - build : Will build the application
    - run : Will run the development server 


First let's initials a basic zenaura application:
```bash
zenaura init 
```
This command will auto generate basic zenaura application with the needed files auto generated for you, so you can get up to speed with the library.

### Auto generated files from init command:
- build.py : used for building zenaura application.
- index.py : simple zenaura server.
- public/components.py: single zenaura component.
- public/presentational.py: few zenaura presentational components created using builder interface.
- public/main.py : main file where we import components, create pages and  configure the client router. 
- public/routes.py : where your client side routes lives.
- public/main.css : the main css file.
- public/config.json: pyscript pydide configuration. 

### Building zenaura 

```bash
zenaura build
```
This command will build index.html.


### Running zenaura
```bash
zenaura run
```

This command will run the development server. Now open browser tab and go to localhost:5000. You will see the following Rendered HTML : 

<center>![](logo.png)
<div data-zenaura="938070c700" class=""><h1 data-zenaura="938070c70011">The Python Library For !</h1><h1 data-zenaura="938070c70012">Building Modern Web User Interface</h1></div>
</center>

Now if we opened components.py, and changed the header text:
``` py
from zenaura.client.component import Component
from public.presentational import * 


class ZenauraStarter(Component):
    def render(self):
        return Div("zenaura", [
           Div("", [
            Image("./public/logo.png", "zenaura", "255", "255", "starterLogo"),
            Header1("The Python Library For, Hello world !"), # note here we changed the content
            Header1("Building Modern Web User Interface")
           ])
        ])

```

The development server have hot reloading feature built-in , it will trigger reloading of the page and we will see the changes live. And changes will be applied.

Rendered HTML : 

<center>![](logo.png)
<div data-zenaura="938070c700" class=""><h1 data-zenaura="938070c70011">The Python Library For, Hello world !</h1><h1 data-zenaura="938070c70012">Building Modern Web User Interface</h1></div>
</center>


## Adding new component to the page

Now we will add new component to the page, this component will be simply a header:

in public/components.py: 

``` py
from zenaura.client.component import Component
from public.presentational import * 


class ZenauraStarter(Component):
    def render(self):
        return Div("zenaura", [
           Div("", [
            Image("./public/logo.png", "zenaura", "255", "255", "starterLogo"),
            Header1("The Python Library For, Hello world !"), # note here we changed the content
            Header1("Building Modern Web User Interface")
           ])
        ])

class ZenauraStarter2(Component):
    def render(self):
        return  Header1("Simple Header !")

```
In public/main.py

``` py
from zenaura.client.app import Route, App
from zenaura.client.page import Page
from public.routes import ClientRoutes
from public.components import ZenauraStarter, ZenauraStarter2 # add the new component
import asyncio


starter = ZenauraStarter()

starter2 = ZenauraStarter2() # create instance of the component
# App and routing
router = App()
home_page = Page([starter, starter2]) # add component to the page

router.add_route(Route(
    title="Developer-Focused | Zenaura",
    path=ClientRoutes.home.value,
    page=home_page
))

# Run the application
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(router.handle_location())



```
Rendered HTML : 

<center>![](logo.png)
<div data-zenaura="938070c700" class=""><h1 data-zenaura="938070c70011">The Python Library For, Hello world !</h1><h1 data-zenaura="938070c70012">Building Modern Web User Interface</h1></div>
</center>
<h1>Simple Header !</h1>



## Adding State to the component 
Now we will add state to the component, the state will be simple keyword rendered within the h1 tag.

```
from zenaura.client.component import Component
from public.presentational import * 


class ZenauraStarter(Component):
    def __init__(self, state):
        self.state = state
    def render(self):
        return  Header1(f"{state}")
```

Note if we took a look at public/presentational.py, we will notice a text node
```py
def Header1(text):
    return Builder('h1').with_text(text).build()
```
with_text, or Node(text=text), is very important this is how you should render user text, the compiler will santize and render the text, to prevent known security issues.

Note this is very simple guide to help you start with zenaura library, in The Basics guide we will go over each building block in zenaura library and explain it, in rich details.
