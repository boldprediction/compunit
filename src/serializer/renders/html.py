from serializer.renders import Render
from serializer.html import HTMLResult, HTMLText


class HTMLRender(Render):

    def render(self, contrast, group_results, individual_results):
        # prepare
        # contrast info
        c1_names = str(contrast.condition1.names)
        c2_names = str(contrast.condition2.names)
        contrast_title = 'Contrast: {c1} - {c2}'.format(c1=c1_names, c2=c2_names)
        contrast_info = HTMLText('contrast-info', contrast_title)
        # group info
        group = HTMLResult('group', group_results)
        # individuals
        individuals = HTMLResult('individuals', individual_results)

        return HTMLResult('contrast', [contrast_info, group, individuals])
