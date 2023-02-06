from evase.structures.analysisperformer import AnalysisPerformer


def perform_analysis(
        folder: str,
        output_folder: str,
        project_name: str = None):
    if project_name is None:
        project_name = "UNKNOWN"

    analysis_performer = AnalysisPerformer(project_name=project_name, project_root=folder)

    analysis_performer.perform_analysis()
    results = analysis_performer.get_results()
    analysis_performer.results_to_JSON(folder)
    return results
