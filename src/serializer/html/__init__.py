from serializer import Serializable


class HTMLResult(Serializable):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def serialize(self):
        result = ""
        for content in self.contents:
            result += content.serialize()

        return '<div class="{clazz}">{content}</div>'.format(clazz=self.name, content=result)


class HTMLText(Serializable):

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def serialize(self):
        return '<div class="{clazz}">{content}</div>'.format(clazz=self.name, content=self.content)


class HTMLImage(Serializable):

    def __init__(self, name, src):
        self.name = name
        self.src = src

    def serialize(self):
        return '<img class="{clazz}" src="{src}">'.format(clazz=self.name, src=self.src)


class HTMLHref(Serializable):

    def __init__(self, name, href):
        self.name = name
        self.href = href

    def serialize(self):
        return '<a class="{clazz}" href="{href}"'.format(clazz=self.name, href=self.href)
