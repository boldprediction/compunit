from analysis.individual import SubjectAnalysis
from serializer.html import HTMLText


class Info(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):
        return HTMLText('subject-info', 'Subject: {name}'.format(name=subject.name))
