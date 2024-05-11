from zenaura.client.dom import zenaura_dom


def mutator(func):
    def wrapper_func(self, *args, **kwargs):
        func(self, *args, **kwargs)
        zenaura_dom.render(self)
    return wrapper_func