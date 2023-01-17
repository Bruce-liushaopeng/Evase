from backend.depanalyze.projectstructure import ProjectAnalysisStruct


def perform_analysis(
        folder: str,
        project_name: str = None,
        sql_injection: bool = False,
        forced_deadlock: bool = False,
        no_encryption: bool = False,
        dictionary: bool = False):

    if project_name is None:
        project_name = "UNKNOWN"

    prj_struct = None
    if any([sql_injection, forced_deadlock, no_encryption, dictionary]):
        prj_struct = ProjectAnalysisStruct(project_name, folder)

    else:
        return "No type of analysis was provided."

    if sql_injection:
        print("Check for SQL Injection.")

    if forced_deadlock:
        print("Check for forced deadlock.")

    if no_encryption:
        print("Check for no encryption.")

    if dictionary:
        print("Check for dictionary.")