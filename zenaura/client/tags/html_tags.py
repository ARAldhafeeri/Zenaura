from .builder import TagBuilder

class HTMLTags:
    """
        html tags factory
    """
    def __init__(self):
        """
            Initializes the HTMLTags object with various tag builders for HTML elements.
        """
        self.html =  TagBuilder("html")
        self.head = TagBuilder("head")
        self.body = TagBuilder("body")

        # Core structural tags
        self.a = TagBuilder("a")
        self.div = TagBuilder("div")
        self.p = TagBuilder("p")
        self.img = TagBuilder("img")
        self.span = TagBuilder("span")
        self.h1 = TagBuilder("h1") 
        self.h2 = TagBuilder("h2")
        self.h3 = TagBuilder("h3")
        self.h4 = TagBuilder("h4")
        self.h5 = TagBuilder("h5")
        self.h6 = TagBuilder("h6")

        # Text formatting tags
        self.abbr = TagBuilder("abbr")
        self.acronym = TagBuilder("acronym")  
        self.address = TagBuilder("address")
        self.b = TagBuilder("b")
        self.bdi = TagBuilder("bdi")
        self.bdo = TagBuilder("bdo")
        self.blockquote = TagBuilder("blockquote")
        self.cite = TagBuilder("cite")
        self.code = TagBuilder("code")
        self.del_ = TagBuilder("del") 
        self.dfn = TagBuilder("dfn")
        self.em = TagBuilder("em")
        self.i = TagBuilder("i")
        self.ins = TagBuilder("ins")
        self.kbd = TagBuilder("kbd")
        self.mark = TagBuilder("mark")
        self.pre = TagBuilder("pre")
        self.q = TagBuilder("q")
        self.rp = TagBuilder("rp")
        self.rt = TagBuilder("rt")
        self.ruby = TagBuilder("ruby")
        self.s = TagBuilder("s")
        self.samp = TagBuilder("samp")
        self.small = TagBuilder("small")
        self.strong = TagBuilder("strong")
        self.sub = TagBuilder("sub")
        self.sup = TagBuilder("sup")
        self.time = TagBuilder("time")
        self.u = TagBuilder("u")
        self.var = TagBuilder("var")

        # List tags
        self.ul = TagBuilder("ul")
        self.ol = TagBuilder("ol")
        self.li = TagBuilder("li")
        self.dl = TagBuilder("dl")
        self.dt = TagBuilder("dt")
        self.dd = TagBuilder("dd")

        # Form tags
        self.form = TagBuilder("form")
        self.input = TagBuilder("input")
        self.textarea = TagBuilder("textarea")
        self.button = TagBuilder("button")
        self.label = TagBuilder("label")
        self.select = TagBuilder("select")
        self.optgroup = TagBuilder("optgroup")
        self.option = TagBuilder("option")
        self.fieldset = TagBuilder("fieldset")
        self.legend = TagBuilder("legend")

        # Other common tags
        self.table = TagBuilder("table")
        self.thead = TagBuilder("thead")
        self.tbody = TagBuilder("tbody")
        self.tfoot = TagBuilder("tfoot")
        self.tr = TagBuilder("tr")
        self.th = TagBuilder("th")
        self.td = TagBuilder("td")
        self.caption = TagBuilder("caption")
        self.colgroup = TagBuilder("colgroup")
        self.col = TagBuilder("col")

        # Media tags
        self.audio = TagBuilder("audio")
        self.video = TagBuilder("video")
        self.source = TagBuilder("source")
        self.track = TagBuilder("track")
        self.embed = TagBuilder("embed")
        self.object = TagBuilder("object")
        self.param = TagBuilder("param")
        self.picture = TagBuilder("picture")

        # Semantic/specialized tags
        self.section = TagBuilder("section")
        self.article = TagBuilder("article")
        self.aside = TagBuilder("aside")
        self.header = TagBuilder("header")
        self.footer = TagBuilder("footer")
        self.nav = TagBuilder("nav")
        self.figure = TagBuilder("figure")
        self.figcaption = TagBuilder("figcaption")
        self.main = TagBuilder("main")
        self.details = TagBuilder("details")
        self.summary = TagBuilder("summary")
        self.dialog = TagBuilder("dialog")

        # Deprecated tags (avoid using)
        self.basefont = TagBuilder("basefont") 
        self.big = TagBuilder("big")
        self.center = TagBuilder("center")
        self.font = TagBuilder("font")
        self.strike = TagBuilder("strike")
        self.tt = TagBuilder("tt")