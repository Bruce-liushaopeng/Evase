from backend.analysisperformer import AnalysisPerformer
from backend.depanalyze.projectstructure import ProjectAnalysisStruct
from pprint import pprint


def perform_analysis(
        folder: str,
        output_folder: str,
        project_name: str = None,
        sql_injection: bool = False,
        forced_deadlock: bool = False,
        no_encryption: bool = False,
        password_guessing: bool = False, ):
    if project_name is None:
        project_name = "UNKNOWN"

    analysis_performer = AnalysisPerformer(project_name=project_name, project_root=folder, sql_injection=sql_injection,
                                           forced_deadlock=forced_deadlock, no_encryption=no_encryption,
                                           password_guessing=password_guessing)

    analysis_performer.perform_analysis()
    pprint(analysis_performer.get_results())
    analysis_performer.results_to_JSON(output_folder)
