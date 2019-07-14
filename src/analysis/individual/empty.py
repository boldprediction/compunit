from analysis.individual import SubjectAnalysis
from analysis.result import AnalysisTextResult


class EmptyAnalysis(SubjectAnalysis):

    def __call__(self, exp_name, subject, contrast, contrast_data):
        return AnalysisTextResult('empty-analysis analysis', 'completed')
