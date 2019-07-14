class AnalysisResult:

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def render(self):
        result = ""
        for content in self.contents:
            result += content.render()

        return '<div class="{clazz}">{content}</div>'.format(clazz=self.name, content=result)


class AnalysisTextResult:

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def render(self):
        return '<div class="{clazz}">{content}</div>'.format(clazz=self.name, content=self.content)


class AnalysisImageResult:

    def __init__(self, name, src):
        self.name = name
        self.src = src

    def render(self):
        return '<img class="{clazz}" src="{src}">'.format(clazz=self.name, src=self.src)


class AnalysisHrefResult:

    def __init__(self, name, href):
        self.name = name
        self.href = href

    def render(self):
        return '<a class="{clazz}" href="{href}"'.format(clazz=self.name, href=self.href)
