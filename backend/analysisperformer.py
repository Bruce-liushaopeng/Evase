from backend.depanalyze.projectstructure import ProjectAnalysisStruct
from backend.sql_injection.injectionvisitor import InjectionNodeVisitor

from abc import ABC, abstractmethod
import json
import os


class BehaviourAnalyzer(ABC):

    def __init__(
            self,
            project_struct: ProjectAnalysisStruct = None,
            executor=None
    ):
        self.project_struct = project_struct
        self.analysis_results = {}
        self.executor = executor

    def get_project_struct(self):
        return self.project_struct

    def get_analysis_results(self):
        return self.analysis_results

    def set_project_struct(self, project_struct: ProjectAnalysisStruct):
        self.project_struct = project_struct

    def set_executor(self, executor):
        self.executor = executor

    @abstractmethod
    def do_analysis(self):
        if self.project_struct is None:
            raise ValueError("Project structure needs to be set before performing analysis.")
        if self.executor is None:
            raise ValueError("An executor function needs to be set before performing analysis.")
        pass


class SQLInjectionBehaviourAnalyzer(BehaviourAnalyzer):

    def __init__(self, project_struct: ProjectAnalysisStruct = None):
        super().__init__(project_struct)

    def do_analysis(self):
        for m_name, m_struct in self.project_struct.get_module_structure().items():
            m_results = dict(found_any=False)
            visitor = InjectionNodeVisitor(self.project_struct, m_name)
            visitor.visit(m_struct.get_ast())
            results = visitor.get_vulnerable_funcs()
            print(results)
            m_results['results'] = results
            self.analysis_results[m_name] = m_results

        return self.analysis_results


class AnalysisPerformer:

    def __init__(
            self,
            project_name: str = None,
            project_root: str = None,
            sql_injection: bool = False,
            forced_deadlock: bool = False,
            no_encryption: bool = False,
            password_guessing: bool = False):

        self.project_name = project_name
        self.project_root = project_root
        self.sql_injection_detector = None
        self.forced_deadlock_detector = None
        self.no_encryption_detector = None
        self.password_guessing_detector = None
        self.analysis_results = {}

        if sql_injection:
            self.sql_injection_detector = SQLInjectionBehaviourAnalyzer()
            self.analysis_results['sql_injection'] = None

    def perform_analysis(self):

        prj_struct = None
        if any([self.sql_injection_detector, self.forced_deadlock_detector, self.no_encryption_detector,
                self.password_guessing_detector]):
            print(self.project_root)
            prj_struct = ProjectAnalysisStruct(self.project_name, self.project_root)
        else:
            return "No type of analysis was provided."

        if self.sql_injection_detector is not None:
            self.sql_injection_detector.set_project_struct(prj_struct)
            sql_injection_results = self.sql_injection_detector.do_analysis()
            print(sql_injection_results)
            self.analysis_results['sql_injection'] = sql_injection_results

    def get_results(self):
        return self.analysis_results

    def results_to_JSON(self, filepath: str):
        jform = json.dumps(self.analysis_results)
        if not os.path.exists(filepath) or not os.path.isdir(filepath):
            raise ValueError("Path doesn't exist or it isn't a directory")
        fpath = os.path.join(filepath, 'analysis_results.json')
        with open(fpath, 'w') as f:
            f.write(jform)
        return jform
