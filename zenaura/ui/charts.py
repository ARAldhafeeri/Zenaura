from zenaura.client.tags.builder import Builder
from zenaura.web.utils import document, to_js
def ChartThis(config, chart_id, *args, **kwargs):
  """
    Attaches a chart to canvas.

    Args: 
      config - ChartJS config https://www.chartjs.org/docs/latest/configuration/
      chart_id - unique id for canvas <canvas id=chart_id> to attach chartjs graph to.
    returns:
      Chart
  """
  from js import Chart, Object
  # clean up chart if chart exists 
  chart_exists = Chart.getChart(chart_id)
  if chart_exists:
    chart_exists.destroy()
  
  # use pyodide to transfrom python dict into js object
  obj = to_js(config, depth=-1,  
                  pyproxies=None,
      create_pyproxies=False,
      dict_converter=Object.fromEntries)
  
  # attach graph
  ctx = document.getElementById(chart_id).getContext('2d')
  Chart.new(ctx, obj)

  # return Chart for extendibility
  return Chart

def Canvas(id, attrs={}, childrens=[]):
  """
    canvas html tag for use with chartjs

    args: 
      id - unique chart id
      attrs - html attributes
      children - children within canvas tag if needed
  """
  return  Builder("canvas").with_attribute("id", id).build()