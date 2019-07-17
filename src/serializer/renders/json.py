from serializer.renders import Render
from serializer.json import JSONResult


class JSONRender(Render):

    def render(self, contrast, group_results, individual_results):

        c1_names = str(contrast.condition1.names)
        c2_names = str(contrast.condition2.names)
        contrast_title = 'Contrast: {c1} - {c2}'.format(c1=c1_names, c2=c2_names)
        contrast_info = {'contrast_info': contrast_title}

        return JSONResult([contrast_info, group_results, individual_results]).serialize()
