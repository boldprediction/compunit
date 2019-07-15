class GroupAnalysis:
    """
    This class represents an analysis for a group of subjects and contrast_results.
    GroupAnalysis has a special flow mechanism.

    Group Analysis Flow

    if a GroupAnalysis returns a dictionary, then the next GroupAnalysis object in the
    analyses chain will receive what the current analysis returned as keyword parameters.

    if a GroupAnalysis returns a Serializable object, then this Serializable object will be
    collected as a part of result. Keyword parameters for the next GroupAnalysis object won't
    change.
    """
    def __call__(self, exp_name, subjects, contrast, contrast_results, **kwargs):
        pass
