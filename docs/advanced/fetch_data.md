# Fetching Data and Integrating APIs with Zenaura

Zenaura simplifies the process of fetching data from APIs and integrating it into your Python-based web applications.

## Key Concepts

1. **Async/Await:** Zenaura embraces asynchronous programming for efficient data fetching. `async def` functions allow your application to perform other tasks while waiting for API responses.

2. **`mutator`:** The `mutator` decorator is used to mark functions that modify component state. This ensures the component automatically re-renders to reflect the updated data.

**Example Client-Side Component (`DataFetcher`)**

### Create zenaura application

```
zenaura init
```

### Add requests to config.json

```
# stays same
    "packages": [
      "zenaura==0.9.94",
      "requests"
    ],
# stays same
```

### Presentational components

```Python
from zenaura.ui import div, img, h1, p

def Div(class_name, children):
    return div(*children, class_=class_name)

def Image(src, alt, width, height, classname=""):
    return img(
        src=src,
        alt=alt,
        width=width,
        height=height,
        class_=classname
    )

def Header1(text):
    return h1(text)

def Paragraph(text):
    return p(text)

def Spinner(text):
    return Div("spinner-container", [
        Header1(text),
    ])

def LoadingComponent():
    """Displays a loading indicator while data is being fetched."""
    return Div("loading", [
        Spinner("spinner"),  # Replace 'Spinner' with your actual spinner component
        Paragraph("Loading data...")
    ])

def ErrorComponent(error):
    """Displays an error message when data fetching fails."""
    return Div("error", [
        Image("./public/error.png", "error", "45", "45"),
        Header1("Error Fetching Data"),
        Paragraph(error)
    ])
```

### main component

```python
from zenaura.client.component import Component
from zenaura.client.mutator import mutator
from public.presentational import *
import requests
def DataDisplayComponent(data):
    return Div("data-dict", [
            Div("item", [Paragraph(key), Paragraph(str(value))])
            for key, value in data.items()
        ])

class DataFetcher(Component):
    def __init__(self):
        super().__init__()
        self.state = {"data": None, "error": None}  # Initial state

    async def fetch_data(self):
        try:
            api_url = 'https://randomuser.me/api/'  # Your API endpoint
            response = requests.get(api_url)
            if response.ok:
                self.state["data"] = response.json()
            else:
                self.state["error"] = "API request failed"
        except Exception as e:
            self.state["error"] = str(e)

    @mutator
    async def attached(self):
        await self.fetch_data()
        print(self.state["data"])


    def render(self):
        if self.state["error"]:
            return ErrorComponent(error=self.state["error"])
        elif self.state["data"]:
            return DataDisplayComponent(data=self.state["data"])
        else:
            return LoadingComponent()
```

### Build and run zenaura app

```Bash
zenaura build
zenaura run
```

now if we went to http://localhost:5000, and open the console we will see this

```JSON
{
  "results": [
    {
      "gender": "male",
      "name": {
        "title": "Mr",
        "first": "Charles",
        "last": "Clark"
      },
      "location": {
        "street": {
          "number": 5328,
          "name": "Vimy St"
        },
        "city": "Grand Falls",
        "state": "Nunavut",
        "country": "Canada",
        "postcode": "Z1S 2U2",
        "coordinates": {
          "latitude": "-69.8976",
          "longitude": "-134.5780"
        },
        "timezone": {
          "offset": "-6:00",
          "description": "Central Time (US & Canada), Mexico City"
        }
      },
      "email": "charles.clark@example.com",
      "login": {
        "uuid": "3338f687-3461-4a72-88e9-33eb19c9077d",
        "username": "tinymeercat320",
        "password": "kang",
        "salt": "mrAgPCkY",
        "md5": "1e1006b14c2e083026c86c129be8c0b8",
        "sha1": "e29949ab4b75c8fa07b79312098e28edb7e10e27",
        "sha256": "e3f3e1ffcf4e73ece750f437f70ac840a941b154e002a5d7327ee84111f59230"
      },
      "dob": {
        "date": "1957-01-26T13:12:12.937Z",
        "age": 67
      },
      "registered": {
        "date": "2020-10-19T19:29:09.124Z",
        "age": 3
      },
      "phone": "C57 P04-4851",
      "cell": "R98 P02-7749",
      "id": {
        "name": "SIN",
        "value": "389514100"
      },
      "picture": {
        "large": "https://randomuser.me/api/portraits/men/70.jpg",
        "medium": "https://randomuser.me/api/portraits/med/men/70.jpg",
        "thumbnail": "https://randomuser.me/api/portraits/thumb/men/70.jpg"
      },
      "nat": "CA"
    }
  ],
  "info": {
    "seed": "61b28009e82e3240",
    "results": 1,
    "page": 1,
    "version": "1.4"
  }
}

```

## Explanation

- **State:** The `state` dictionary holds the fetched data (`data`) and any potential error messages (`error`).
- **`fetch_data`:** This `async` function handles the API request using `requests`.
- **`data` & `error`:** update the state based on the API response or error.
- **`attached`:** Automatically fetches data when the component is added to the DOM, and re-render the component with the data.

In all, this component will set data to data state, error to error if error exists, it uses python requests library to fetch requests, and on success renders an error or data.

## Key Improvements

- Clearer structure and separation of concerns.
- Error handling mechanism.
- Flexibility to use different state management approaches.
