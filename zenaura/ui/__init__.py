from .tags import (
    # main root and meta data
    html, main, body, base, head, link, meta, style, title,
    
    # Section root elements
    address, article, aside, footer, header, header, h1, h2, h3, h4, h5, h6, hgroup, nav, section, search,
    
    # Text content elements
    blockquote, dd, div, dl, dt, figcaption, figure, hr, li, menu, ol, p, pre, ul, img,
    
    # Inline text semantic elements
    a, abbr, b, bdi, bdo, br, cite, code, data, dfn, em, i, kbd, mark, q, rp, rt, ruby, s, samp, small, span, strong, sub, sup, time, u, var,
    
    # Forms
    form, input_, label, select, textarea, option, fieldset, datalist, meter, optgroup, output, progress,
    # embedded content
    
    
    # Scripting elements
    script,
    
    # Media elements
    audio, video, source, img, source, track, video, 
    
    # Table elements
    caption, col, colgroup, table, tbody, td, tfoot, th, thead, tr,

    # embedded content 
    embed, fencedframe, iframe, object_, picture, portal, 

    # svg  and math 
    svg, math, circle, ellipse, line, polyline, polygon, 
    path, rect,

    # Miscellaneous content 
    noscript, del_, ins 
)


from .badge import Badge
from .button import Button
from .breadcrumbs import BreadCrumbs
from .card import Card
from .charts import Canvas, ChartThis
from .common import (
  Image,
  Header2,
  Header1,
  Section,
  HR,
  OL,
  LI,
  A,
  Dialog,
  Paragraph,
  Div,
  Loader,
  NavItemText,
  NavItemTextNameFactory,
  Link,
  NavItemIcon,
  SvgPath,
  Svg,
  Span
)