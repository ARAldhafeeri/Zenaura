# Intro 

Zenaura/UI Chart is built on top of Chart.js, enabling Python developers to leverage Python's superior data manipulation capabilities and display data using Chart.js. With simple easy to learn APIS.

Including a chart is of three steps:
1. Create chart.js configuration https://www.chartjs.org/docs/latest/configuration/
2. use `ChartThis` api and pass chart unique id.
3. pass chart unique id to the chart Canvas. 

For more complex usage feel free to review chartJS documentation, pydide:
1. chartjs: https://www.chartjs.org/
2. pyodide : https://pyodide.org/en/stable/

# Installation 

prerequisits:
    - Python 3.12 or above.
    - zenaura v0.13.0

##  Steps to use

1. Add chartjs to `build.py` to be able to use chartjs within zenaura component
```
from zenaura.server import ZenauraServer
from public.main import my_app_layout

ZenauraServer.hydrate_app_layout(my_app_layout, scripts=[
        # your scripts, style sheets.
        """    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>"""

])
```

2. Creating a chart is of three steps 

```
from zenaura.client.mutator import mutator
from zenaura.ui.charts import ChartThis, Canvas
from zenaura.client.component import Component

# Data for the chart
labels = ["January", "February", "March", "April", "May", "June", "July"]
data = {
    "labels": labels,
    "datasets": [{
        "label": "My First Dataset",
        "backgroundColor": "rgba(255, 99, 132, 0.2)",
        "borderColor": "rgb(255, 99, 132)",
        "data": [65, 59, 80, 81, 56, 55, 40],
    }]
}

# Configuration options
config = {
    "type": "bar",
    "data": data,
    "options": {}
}

class Chart(Component):
  def __init__(self):
    self.chart_name = "barchart"

  @mutator
  async def attached(self):
    ChartThis(config, self.chart_name)

    
  def render(self):
    return  Canvas(self.chart_name)


```

Now you can use this component within a page, you can as well create presentational component and use it within larger component. 