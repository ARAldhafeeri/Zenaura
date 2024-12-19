import unittest
import unittest

from zenaura.ui.tags import (
    # main root and meta data
    main, base, head, link, meta, style, title, html,
    
    # Section root elements
    body, address, article, aside, footer, header, h1, h2, h3, h4, h5, h6, hgroup, nav, section, search,
    
    # Text content elements
    blockquote, dd, div, dl, dt, figcaption, figure, hr, li, menu, ol, p, pre, ul, img,
    
    # Inline text semantic elements
    a, abbr, b, bdi, bdo, br, cite, code, data, dfn, em, i, kbd, mark, q, rp, rt, ruby, s, samp, small, span, strong, sub, sup, time, u, var,
    
    # Forms
    form, input, label, select, textarea, option, 

    # embedded content
    
    
    # Scripting elements
    script,
    
    # Media elements
    audio, video, source, 
    
    # Table elements
    caption, col, colgroup, table, tbody, td, tfoot, th, thead, tr
)


from zenaura.client.compiler import Compiler
from zenaura.client.tags import Node
compiler = Compiler() 
txt_node = lambda txt:  Node(text=txt)
class TagTests(unittest.TestCase):
  # main, html and  root and meta data
  def test_html(self):
    elm = html(lang="main-content")
    result = compiler.compile(elm)
    self.assertEqual(result, '<html lang="main-content"></html>')

  def test_main(self):
      elm = main(txt_node("Main content here"), id="main-content", class_="container")
      result = compiler.compile(elm)
      self.assertEqual(result, '<main id="main-content" class="container">Main content here</main>')

  def test_base(self):
      elm = base(href="https://example.com")
      result = compiler.compile(elm)
      self.assertEqual(result, '<base href="https://example.com" />')

  def test_head(self):
      elm = head(meta(name_="viewport", content="width=device-width"))
      result = compiler.compile(elm)
      self.assertEqual(result, '<head><meta name="viewport" content="width=device-width" /></head>')

  def test_link(self):
      elm = link(rel="stylesheet", href="style.css")
      result = compiler.compile(elm)
      self.assertEqual(result, '<link rel="stylesheet" href="style.css" />')

  def test_meta(self):
      elm = meta(name_="description", content="Test description")
      result = compiler.compile(elm)
      self.assertEqual(result, '<meta name="description" content="Test description" />')

  def test_style(self):
      elm = style(type="text/css", text="body {background-color: #fff;}")
      result = compiler.compile(elm)
      self.assertEqual(result, '<style type="text/css">body {background-color: #fff;}</style>')

  def test_title(self):
      elm = title(text="Test Page Title")
      result = compiler.compile(elm)
      self.assertEqual(result, '<title>Test Page Title</title>')


  def test_body(self):
      elm = body(txt_node("This is the body content."), id="main-body")
      result = compiler.compile(elm)
      self.assertEqual(result, '<body id="main-body">This is the body content.</body>')

  def test_address(self):
      elm = address("123 Test Street, Test City, TX 12345")
      result = compiler.compile(elm)
      self.assertEqual(result, '<address>123 Test Street, Test City, TX 12345</address>')

  def test_article(self):
      elm = article(txt_node("This is an article."), class_="post")
      result = compiler.compile(elm)
      self.assertEqual(result, '<article class="post">This is an article.</article>')

  def test_aside(self):
      elm = aside(txt_node("This is an aside content."), class_="sidebar")
      result = compiler.compile(elm)
      self.assertEqual(result, '<aside class="sidebar">This is an aside content.</aside>')

  def test_footer(self):
      elm = footer(txt_node("This is the footer."))
      result = compiler.compile(elm)
      self.assertEqual(result, '<footer>This is the footer.</footer>')

  def test_body(self):
      elm = body("This is the body content.", id="main-body")
      result = compiler.compile(elm)
      self.assertEqual(result, '<body id="main-body">This is the body content.</body>')

  def test_address(self):
      elm = address("123 Test Street, Test City, TX 12345")
      result = compiler.compile(elm)
      self.assertEqual(result, '<address>123 Test Street, Test City, TX 12345</address>')

  def test_article(self):
      elm = article("This is an article.", class_="post")
      result = compiler.compile(elm)
      self.assertEqual(result, '<article class="post">This is an article.</article>')

  def test_aside(self):
      elm = aside("This is an aside content.", class_="sidebar")
      result = compiler.compile(elm)
      self.assertEqual(result, '<aside class="sidebar">This is an aside content.</aside>')

  def test_footer(self):
      elm = footer("This is the footer.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<footer>This is the footer.</footer>')

  def test_header(self):
      elm = header("This is the header.", class_="header-main")
      result = compiler.compile(elm)
      self.assertEqual(result, '<header class="header-main">This is the header.</header>')

  def test_h1(self):
      elm = h1("Heading 1")
      result = compiler.compile(elm)
      self.assertEqual(result, '<h1>Heading 1</h1>')

  def test_h2(self):
      elm = h2("Heading 2")
      result = compiler.compile(elm)
      self.assertEqual(result, '<h2>Heading 2</h2>')

  def test_h3(self):
      elm = h3("Heading 3")
      result = compiler.compile(elm)
      self.assertEqual(result, '<h3>Heading 3</h3>')

  def test_h4(self):
      elm = h4("Heading 4")
      result = compiler.compile(elm)
      self.assertEqual(result, '<h4>Heading 4</h4>')

  def test_h5(self):
      elm = h5("Heading 5")
      result = compiler.compile(elm)
      self.assertEqual(result, '<h5>Heading 5</h5>')

  def test_h6(self):
      elm = h6("Heading 6")
      result = compiler.compile(elm)
      self.assertEqual(result, '<h6>Heading 6</h6>')

  def test_hgroup(self):
      elm = hgroup(h1("Main Heading"), h2("Subheading"))
      result = compiler.compile(elm)
      self.assertEqual(result, '<hgroup><h1>Main Heading</h1><h2>Subheading</h2></hgroup>')

  def test_nav(self):
      elm = nav("Navigation Links", id="main-nav")
      result = compiler.compile(elm)
      self.assertEqual(result, '<nav id="main-nav">Navigation Links</nav>')

  def test_section(self):
      elm = section("This is a section.", id="main-section")
      result = compiler.compile(elm)
      self.assertEqual(result, '<section id="main-section">This is a section.</section>')

  def test_search(self):
      elm = search("Search Bar", role="search")
      result = compiler.compile(elm)
      self.assertEqual(result, '<search role="search">Search Bar</search>')

  def test_blockquote(self):
      elm = blockquote("This is a blockquote.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<blockquote>This is a blockquote.</blockquote>')

  def test_dd(self):
      elm = dd("Definition description.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<dd>Definition description.</dd>')

  def test_div(self):
      elm = div("This is a div element.", id="main-div")
      result = compiler.compile(elm)
      self.assertEqual(result, '<div id="main-div">This is a div element.</div>')

  def test_dl(self):
      elm = dl(
          dt("Term 1"),
          dd("Definition for Term 1"),
          dt("Term 2"),
          dd("Definition for Term 2")
      )
      result = compiler.compile(elm)
      self.assertEqual(result, '<dl><dt>Term 1</dt><dd>Definition for Term 1</dd><dt>Term 2</dt><dd>Definition for Term 2</dd></dl>')

  def test_dt(self):
      elm = dt("Definition Term")
      result = compiler.compile(elm)
      self.assertEqual(result, '<dt>Definition Term</dt>')

  def test_figcaption(self):
      elm = figcaption("This is a caption.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<figcaption>This is a caption.</figcaption>')

  def test_figure(self):
      elm = figure(
          img(src="image.jpg", alt="Test Image"),
          figcaption("This is a caption for the image.")
      )
      result = compiler.compile(elm)
      self.assertEqual(result, '<figure><img src="image.jpg" alt="Test Image" /><figcaption>This is a caption for the image.</figcaption></figure>')

  def test_hr(self):
      elm = hr()
      result = compiler.compile(elm)
      self.assertEqual(result, '<hr />')

  def test_li(self):
      elm = li("List item content.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<li>List item content.</li>')

  def test_menu(self):
      elm = menu(
          li("Menu item 1"),
          li("Menu item 2"),
          li("Menu item 3")
      )
      result = compiler.compile(elm)
      self.assertEqual(result, '<menu><li>Menu item 1</li><li>Menu item 2</li><li>Menu item 3</li></menu>')

  def test_ol(self):
      elm = ol(
          li("Ordered item 1"),
          li("Ordered item 2"),
          li("Ordered item 3")
      )
      result = compiler.compile(elm)
      self.assertEqual(result, '<ol><li>Ordered item 1</li><li>Ordered item 2</li><li>Ordered item 3</li></ol>')

  def test_p(self):
      elm = p("This is a paragraph.", class_="text-body")
      result = compiler.compile(elm)
      self.assertEqual(result, '<p class="text-body">This is a paragraph.</p>')

  def test_pre(self):
      elm = pre("Preformatted text block.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<pre>Preformatted text block.</pre>')

  def test_ul(self):
      elm = ul(
          li("Unordered item 1"),
          li("Unordered item 2"),
          li("Unordered item 3")
      )
      result = compiler.compile(elm)
      self.assertEqual(result, '<ul><li>Unordered item 1</li><li>Unordered item 2</li><li>Unordered item 3</li></ul>')
   
  def test_a(self):
      elm = a("Click here", href="https://example.com")
      result = compiler.compile(elm)
      self.assertEqual(result, '<a href="https://example.com">Click here</a>')

  def test_abbr(self):
      elm = abbr("HTML", title="HyperText Markup Language")
      result = compiler.compile(elm)
      self.assertEqual(result, '<abbr title="HyperText Markup Language">HTML</abbr>')

  def test_b(self):
      elm = b("Bold text")
      result = compiler.compile(elm)
      self.assertEqual(result, '<b>Bold text</b>')

  def test_bdi(self):
      elm = bdi("This is BDI content.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<bdi>This is BDI content.</bdi>')

  def test_bdo(self):
      elm = bdo("This is BDO content.", dir="rtl")
      result = compiler.compile(elm)
      self.assertEqual(result, '<bdo dir="rtl">This is BDO content.</bdo>')

  def test_br(self):
      elm = br()
      result = compiler.compile(elm)
      self.assertEqual(result, '<br />')

  def test_cite(self):
      elm = cite("This is a citation.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<cite>This is a citation.</cite>')

  def test_code(self):
      elm = code(txt_node("""print('Hello, World!')"""))
      result = compiler.compile(elm)
      self.assertEqual(result, '<code>print(\'Hello, World!\')</code>')

  def test_data(self):
      elm = data("12345", value="67890")
      result = compiler.compile(elm)
      self.assertEqual(result, '<data value="67890">12345</data>')

  def test_dfn(self):
      elm = dfn("This is a definition term.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<dfn>This is a definition term.</dfn>')

  def test_em(self):
      elm = em("This is emphasized text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<em>This is emphasized text.</em>')

  def test_i(self):
      elm = i("This is italic text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<i>This is italic text.</i>')

  def test_kbd(self):
      elm = kbd("Ctrl+C")
      result = compiler.compile(elm)
      self.assertEqual(result, '<kbd>Ctrl+C</kbd>')

  def test_mark(self):
      elm = mark("This text is highlighted.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<mark>This text is highlighted.</mark>')

  def test_q(self):
      elm = q("This is a quotation.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<q>This is a quotation.</q>')

  def test_rp(self):
      elm = rp("This is ruby parenthesis.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<rp>This is ruby parenthesis.</rp>')

  def test_rt(self):
      elm = rt("This is ruby text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<rt>This is ruby text.</rt>')

  def test_ruby(self):
      elm = ruby("漢", rt("kanji"))
      result = compiler.compile(elm)
      self.assertEqual(result, '<ruby>漢<rt>kanji</rt></ruby>')

  def test_s(self):
      elm = s("Strikethrough text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<s>Strikethrough text.</s>')

  def test_samp(self):
      elm = samp("Sample text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<samp>Sample text.</samp>')

  def test_small(self):
      elm = small("This is small text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<small>This is small text.</small>')

  def test_span(self):
      elm = span("This is a span element.", class_="highlight")
      result = compiler.compile(elm)
      self.assertEqual(result, '<span class="highlight">This is a span element.</span>')

  def test_strong(self):
      elm = strong("This is strong text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<strong>This is strong text.</strong>')

  def test_sub(self):
      elm = sub("Subscript text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<sub>Subscript text.</sub>')

  def test_sup(self):
      elm = sup("Superscript text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<sup>Superscript text.</sup>')

  def test_time(self):
      elm = time("2:30 PM", datetime="14:30")
      result = compiler.compile(elm)
      self.assertEqual(result, '<time datetime="14:30">2:30 PM</time>')

  def test_u(self):
      elm = u("Underlined text.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<u>Underlined text.</u>')

  def test_var(self):
      elm = var("Variable name")
      result = compiler.compile(elm)
      self.assertEqual(result, '<var>Variable name</var>')

  def test_form(self):
      elm = form(input(type_="text"), action="/submit", method="post")
      result = compiler.compile(elm)
      self.assertEqual(result, '<form action="/submit" method="post"><input type="text" /></form>')

  def test_input(self):
      elm = input(type="text", value="Input Value")
      result = compiler.compile(elm)
      self.assertEqual(result, '<input type="text" value="Input Value" />')

  def test_label(self):
      elm = label("Name", for_="name")
      result = compiler.compile(elm)
      self.assertEqual(result, '<label for="name">Name</label>')

  def test_select(self):
      elm = select(option("Option 1"), name_="dropdown")
      result = compiler.compile(elm)
      self.assertEqual(result, '<select name="dropdown"><option>Option 1</option></select>')

  def test_textarea(self):
      elm = textarea("This is a textarea.", name_="description")
      result = compiler.compile(elm)
      self.assertEqual(result, '<textarea name="description">This is a textarea.</textarea>')

  def test_script(self):
      elm = script("console.log('Hello, World!');")
      result = compiler.compile(elm)
      self.assertEqual(result, '<script>console.log(\'Hello, World!\');</script>')

  def test_audio(self):
      elm = audio(source(src="audio.mp3", type_="audio/mpeg"), controls=True)
      result = compiler.compile(elm)
      self.assertEqual(result, '<audio controls="true"><source src="audio.mp3" type="audio/mpeg" /></audio>')

  def test_video(self):
      elm = video(source(src="video.mp4", type_="video/mp4"), controls=True)
      result = compiler.compile(elm)
      self.assertEqual(result, '<video controls="true"><source src="video.mp4" type="video/mp4" /></video>')

  def test_caption(self):
      elm = caption("This is a table caption.")
      result = compiler.compile(elm)
      self.assertEqual(result, '<caption>This is a table caption.</caption>')

  def test_col(self):
      elm = col(span="2")
      result = compiler.compile(elm)
      self.assertEqual(result, '<col span="2" />')

if __name__ == "__main__":
    unittest.main()
