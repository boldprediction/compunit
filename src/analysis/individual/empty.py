from analysis.individual import SubjectAnalysis
from serializer.html import HTMLText


class EmptyAnalysis(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):
        return HTMLText('empty-analysis analysis', 'completed')
