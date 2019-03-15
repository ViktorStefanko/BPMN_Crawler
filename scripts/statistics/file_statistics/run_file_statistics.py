from scripts.statistics.file_statistics.extensions_of_files import get_all_extensions
from scripts.statistics.file_statistics.extensions_of_files import write_extensions_to_csv
from scripts.statistics.file_statistics.files_type import get_files_type
from scripts.statistics.file_statistics.files_type import write_all_types_to_csv
from scripts.statistics.file_statistics.files_type import find_bpmn_files_from_xml
from scripts.statistics.file_statistics.files_type import find_image_files
from scripts.statistics.file_statistics.file_statistics import write_csv_file_n_authors
from scripts.statistics.file_statistics.file_statistics import write_csv_file_bpmn_n_authors
from scripts.statistics.file_statistics.file_statistics import write_csv_file_n_revs
from scripts.statistics.file_statistics.file_statistics import write_csv_file_bpmn_n_revs
from scripts.statistics.file_statistics.file_statistics import write_csv_file_age_months
from scripts.statistics.file_statistics.file_statistics import write_csv_file_bpmn_age_months

"""
Create csv Files with statistics about files
"""

[extensions_dict, numb_all_files] = get_all_extensions()
csv_extensions_statistics = 'scripts/statistics/csv_files/csv_file_statistics/extensions_of_all_files.csv'
write_extensions_to_csv(extensions_dict, numb_all_files, 5, csv_extensions_statistics)

files_type_dict = get_files_type(extensions_dict)
csv_files_type_statistics = 'scripts/statistics/csv_files/csv_file_statistics/types_of_all_files.csv'
write_all_types_to_csv(files_type_dict, numb_all_files, csv_files_type_statistics)

csv_n_authors_all_files = 'scripts/statistics/csv_files/csv_file_statistics/n_authors_all_files.csv'
write_csv_file_n_authors(csv_n_authors_all_files)
csv_n_authors_only_bpmn_files = 'scripts/statistics/csv_files/csv_file_statistics/n_authors_bpmn_files.csv'
write_csv_file_bpmn_n_authors(csv_n_authors_only_bpmn_files)

csv_n_revs_all_files = 'scripts/statistics/csv_files/csv_file_statistics/n_revs_all_files.csv'
write_csv_file_n_revs(csv_n_revs_all_files, 0.001)
csv_n_revs_only_bpmn_files = 'scripts/statistics/csv_files/csv_file_statistics/n_revs_bpmn_files.csv'
write_csv_file_bpmn_n_revs(csv_n_revs_only_bpmn_files, 0.001)

csv_age_months_all_files = 'scripts/statistics/csv_files/csv_file_statistics/age_months_all_files.csv'
write_csv_file_age_months(csv_age_months_all_files, 0.001)
csv_age_months_only_bpmn_files = 'scripts/statistics/csv_files/csv_file_statistics/age_months_bpmn_files.csv'
write_csv_file_bpmn_age_months(csv_age_months_only_bpmn_files, 0.001)

