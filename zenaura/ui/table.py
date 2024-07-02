from .common import *


def Table(data, columns, attrs={}, class_names="min-w-full bg-white shadow-md rounded-xl", td_class_names="py-3 px-4 text-left", th_class_names="py-3 px-4", tr_class_names="border-b border-light-gray dark:border-dark-page1"):
	"""
	Creates a table component with given data, columns.
	args:
			data - list of dictionaries of data e.g. [{"key" : 1, "name": "Mike"}]
			columns - list of dictionaries of column names [{"title": "Name", "index": "name"}]
					note index for each column is where data is indexed and displayed, for example
							when index is "name" , for every dictionary in data "name" is fetched and displayed
			class_names - default class name
			attrs table tag attributes dictionary
	"""
	names = [Builder("th").with_class(th_class_names).with_text(col["title"]).build() for col in columns]
	indexes = [col["index"] for col in columns]
	rows = []
	for i in range(len(data)):
			row_items = [Builder("td").with_class(td_class_names).with_text(str(data[i][index])).build() for index in indexes]
			rows.append(Builder("tr").with_class(tr_class_names).with_children(
					*row_items
			).build())
	
	return    Builder("table").with_attributes(**attrs).with_attribute("class", class_names).with_children(
			Builder("thead").with_child(
					Builder("tr").with_class(tr_class_names).with_children(
					*names
			).build()
			).build(),
			Builder("tbody").with_children(
					*rows
			).build()
	).build()