from scripts.statistics.repo_statistics.languages_of_projects import make_csv_languages_all_repos
from scripts.statistics.repo_statistics.languages_of_projects import make_csv_languages_bpmn_repos
from scripts.statistics.repo_statistics.find_bpmn_repos import count_bpmn_repos
from scripts.statistics.repo_statistics.find_bpmn_repos import count_all_repos
from scripts.statistics.repo_statistics.find_bpmn_repos import make_csv_bpmn_repos
from scripts.statistics.repo_statistics.repo_statistics import write_csv_projects_created_at
from scripts.statistics.repo_statistics.repo_statistics import write_csv_projects_last_commit_at
from scripts.statistics.repo_statistics.location_statistics import get_repo_location2


"""
Create csv Files with statistics about repositories
"""

csv_all_repos_languages = 'scripts/statistics/csv_files/csv_repo_statistics/languages_all_repos.csv'
make_csv_languages_all_repos(csv_all_repos_languages, 5)

csv_repos_with_bpmn = 'scripts/statistics/csv_files/csv_repo_statistics/repos_with_bpmn.csv'
make_csv_bpmn_repos(count_bpmn_repos(), count_all_repos(), csv_repos_with_bpmn)

csv_bpmn_repos_languages = 'scripts/statistics/csv_files/csv_repo_statistics/languages_bpmn_repos.csv'
make_csv_languages_bpmn_repos(csv_bpmn_repos_languages, 5)

csv_created_at_repos = 'scripts/statistics/csv_files/csv_repo_statistics/created_at_repos.csv'
write_csv_projects_created_at(csv_created_at_repos, 0.001)

csv_last_commit_at_repos = 'scripts/statistics/csv_files/csv_repo_statistics/last_commit_at_repos.csv'
write_csv_projects_last_commit_at(csv_last_commit_at_repos, 0.001)


