from scripts.statistics.file_statistics.extensions_of_files import get_all_extensions
from scripts.statistics.file_statistics.extensions_of_files import write_extensions_to_csv
from scripts.statistics.file_statistics.files_type import get_files_type
from scripts.statistics.file_statistics.files_type import write_all_types_to_csv
from scripts.statistics.file_statistics.files_type import find_bpmn_files_from_xml
from scripts.statistics.file_statistics.files_type import find_image_files

"""
Create csv Files with statistics about files
"""

[extensions_dict, numb_all_files] = get_all_extensions()
csv_extensions_statistics = 'scripts/statistics/csv_files/csv_file_statistics/extensions_of_all_files.csv'
write_extensions_to_csv(extensions_dict, numb_all_files, 5, csv_extensions_statistics)

files_type_dict = get_files_type(extensions_dict)
csv_files_type_statistics = 'scripts/statistics/csv_files/csv_file_statistics/types_of_all_files.csv'
write_all_types_to_csv(files_type_dict, numb_all_files, csv_files_type_statistics)
#find_bpmn_files_from_xml()
#find_image_files()
