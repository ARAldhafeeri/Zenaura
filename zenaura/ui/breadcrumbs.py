from .common import Span, LI, A, OL
from zenaura.client.tags.builder import Builder


def BreadCrumbs(
    breadcrumbs, 
    seprator=">", 
    span_class="", 
    a_tag_class="opacity-60", 
    li_class="flex cursor-pointer items-center font-sans text-sm font-normal leading-normal antialiased transition-colors duration-300 text-light-gray1 hover:text-light-green dark:text-dark-page1 dark:hover:text-dark-gray2 ", 
    ol_class="flex w-full flex-wrap items-center rounded-md py-2 px-4", 
    sep_class="pointer-events-none mx-2 select-none font-sans text-sm font-normal leading-normal antialiased"
    ) -> "BreadCrumbs":
  """
    Display the path to the current resources as hierarchy of links

    args : 
      breadcrumbs - list of tuples as [("title", "handler"), ...] displayed in order
        handler url to navigate to.
        title is the title of breadcrumb that will be displayed.
      seprator - custom seprator between breadcrumbs default is text >
      span_class - span element classes
      a_tag_class - breadcrumb a tag css calsses
      li_class - breadcrumb li tag css classes
      ol_class - bread crumb ol tag css classes
      sep_class - breadcrumb seprator css classes
  """
  crumbs = []
  sep = Span(sep_class, seprator)
  n = len(breadcrumbs)
  for i in range(n):
    title, handler  = breadcrumbs[i]
    crumb = LI(
      A(
        Span(span_class, title),
        {"class": a_tag_class, "href": handler},
      ),
      {"class": li_class}
    )
    crumbs.append(crumb)
    if i != n - 1:
      crumbs.append(sep)
  return OL(crumbs, {"class" : ol_class})
