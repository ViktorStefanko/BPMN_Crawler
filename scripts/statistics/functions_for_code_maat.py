import subprocess
import os


class CodeMaatFunctions:

    @staticmethod
    def create_log_file(repo_path, log_file_path):
        cmd = 'git --git-dir ' + os.path.join(repo_path, ".git") + \
              ' log --pretty=format:"[%h] %aN %ad %s" --date=short --numstat --after=2000-01-01 ' \
              '> ' + log_file_path
        pipe1 = subprocess.Popen(cmd, shell=True)
        pipe1.wait()

    @staticmethod
    def make_repo_statistics(code_maat_path, log_file_path, csv_path):
        cmd = "java -jar " + code_maat_path + " -l " + log_file_path + \
              " -c git -a abs-churn --input-encoding GB18030 > " + csv_path
        pipe = subprocess.Popen(cmd, shell=True)
        pipe.wait()

    @staticmethod
    def make_files_statistics(code_maat_path, log_file_path, statistics_utf16_csv_path,
                              age_utf16_csv_path):
        os.environ["COMSPEC"] = 'powershell'
        cmd2 = "java -jar " + code_maat_path + " -l " + log_file_path + \
               " -c git --input-encoding GB18030 > " + statistics_utf16_csv_path
        cmd4 = "java -jar " + code_maat_path + " -l " + log_file_path + \
               " -c git -a age --input-encoding GB18030 > " + age_utf16_csv_path
        pipe2 = subprocess.Popen(cmd2, shell=True)
        pipe2.wait()
        pipe4 = subprocess.Popen(cmd4, shell=True)
        pipe4.wait()

#git config --global core.quotepath off
