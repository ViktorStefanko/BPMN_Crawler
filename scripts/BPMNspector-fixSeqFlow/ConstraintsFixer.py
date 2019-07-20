from scripts.gh_api_crawler.db_handler import DbHandler
import subprocess
import xmltodict
import os


class ConstraintsFixer:

    def __init__(self):
        self.all_files_path = "../../../data_GH_projects/all_files"
        self.BPMNspector_fixSeqFlow = "BPMNspector-fixSeqFlow"

    def fix_bpmn(self):
        cmd = self.BPMNspector_fixSeqFlow + " " + self.all_files_path
        pipe = subprocess.Popen(cmd, shell=True)
        pipe.wait()

    def rename_files(self):
        reposrts_list = os.listdir(self.all_files_path)
        for f in reposrts_list:
            if ".xml" in f:
                f_new = f.split(".xml")[0]
                os.rename(self.all_files_path + "/" + f, self.all_files_path + "/" + f_new + ".bpmn")
