import io
from zenaura.client.page import Page 
from zenaura.client.hydrator import HydratorCompilerAdapter
from zenaura.client.app import App 

compiler_adapter = HydratorCompilerAdapter()

# create pyscript pydido template 
def template(content, meta_description=None, title=None, icon=None, pydide="https://pyscript.net/releases/2024.1.1/core.js", scripts=None):
    if scripts:
      s = io.StringIO()
      for script in scripts:
          s.write(script)
          s.write("\n")
      scripts = s 
        
    return f"""

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="{icon}" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="title" content="{title}" />
    <meta http-equiv="refresh"  />
    <meta
      name="description"
      content="{meta_description}"
    />
    <script type="module" src="{pydide}"></script>
    {scripts if scripts else ""}
 
	<script type="py" src="./public/main.py" config="./public/config.json"></script>

    <link  rel="stylesheet" href="./public/main.css">

    <title>{title}</title>
    
  </head>
  <body>
    <div id="root">
        {content}
    </div>
  
  </body>

</html>
"""
class ZenauraServer:

    @staticmethod
    def hydrate_page(page : Page, title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js"):
        """
          hyderate zenaura page for server side rendering, 
          params :
           page - zenaura page.
           title - html meta tag for title text
           meta_description : html meta description for website
           icon: favorite.ico
           pydide : is pydide build script url.
        """
        return template(compiler_adapter.hyd_comp_compile_page(page),meta_description, title, icon, pydide)
    
    @staticmethod
    def hydrate_app(app :App, title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js", scripts=None):
      """
          render pages on app run, set page with path / to visible, rest to hidden
          then compile index.html on server run. 
          params :
          app - zenaura app.
          title - html meta tag for title text
          meta_description : html meta description for website
          icon: favorite.ico
          pydide : is pydide build script url.
      """
      pages = io.StringIO()

      # render pages 
      for path, route in app.routes.items():
          page, _, _ , ssr = route 
          if ssr: # ignore SSR pages
              continue 
          if path == "/" : # set / route to visible 
              page_div = lambda comps : f'<div data-zenaura="{page.id}">{comps}</div>'
              pages.write(page_div(compiler_adapter.hyd_comp_compile_page(page)))
              continue
          # pages other than / are set to hidden
          page_div = lambda comps : f'<div hidden data-zenaura="{page.id}">{comps}</div>'
          pages.write(page_div(compiler_adapter.hyd_comp_compile_page(page)))
      

      pages = pages.getvalue() 

      # overwrite in public dir
      with open("./public/index.html", "w") as file:
          print(file)
          file.write(template(pages,meta_description, title, icon, pydide, scripts))

        
