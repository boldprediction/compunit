from analysis.individual import SubjectAnalysis
from analysis.result import AnalysisTextResult


class Info(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):
        return AnalysisTextResult('subject-info', 'Subject: {name}'.format(name=subject.name))
