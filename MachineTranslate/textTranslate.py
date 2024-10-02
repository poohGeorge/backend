import subprocess
import importlib
import pkg_resources
import os
import argostranslate.package
import argostranslate.translate
import os.path
from pathlib import Path




# path = r"C:\Users\Administrator\.local\share\argos-translate\packages"
# source = "argos-translate-model"
# def copy_directory(path):
#     try:
#         # os.mkdir(path, exist_ok=True)
#         shutil.copytree(source, path, dirs_exist_ok=True)
#         print(f"Directory '{path}' created successfully.")
#     except Exception as e:
#         print(f"An error occurred: {e}")




def check_package_installed(package_name):
    installed_packages = pkg_resources.working_set
    package_list = {pkg.key for pkg in installed_packages}
    
    if package_name in package_list:
        print(f"Package '{package_name}' is installed.")
        return True
    else:
        print(f"Package '{package_name}' is not installed.")
        return False




# def run_libretranslate_server():
#     # print(check_package_installed("libretranslate"))
#     if(check_package_installed("argostranslate")):
#         try:
#             translate
            
#             # Use subprocess to run the server
#             process = subprocess.Popen(command)
#             print(f"LibreTranslate server started with PID: {process.pid}")
#         except Exception as e:
#             print(f"An error occurred while starting the LibreTranslate server: {e}")





def translate(text, from_code, to_code):
    # line_count = 1
	# translatedText = ''
	# t = argostranslate
	# print(to_code)
	# lang_list=list(LANGUAGES_TRANSLATED.keys())
	# try:
	# 	lang_list.index(from_code)
	# 	print("lang_list.index(from_code)")
	# except:
	# 	from_code = "en"
	# 	print("from_code = ")
	# try:
	# 	translatedText = argostranslate.translate.translate(text, from_code, to_code)
	# 	print("3")
	# except:
	# 	if from_code != "en":
	# 		model_path1 = f"./argosmodels/{from_code}_en.argosmodel"
	# 		try:
	# 			argostranslate.package.install_from_path(model_path1)
	# 		except:
	# 			print(f"{model_path1} does not exist.\n")
	# 			return translatedText
	# 	if to_code != "en":
	# 		model_path2 = f"./argos-translate-model/en_{to_code}.zip"
	# 		try:
	# 			argostranslate.package.install_from_path(model_path2)
	# 		except Exception as e:
	# 			print(e)
	# 			print(f"{model_path2} does not exist.\n")
	# 			# return translatedText
    if from_code == 'auto':
        from_code = 'en'
    if to_code == 'auto':
        to_code = 'en'
    if from_code == to_code:
        return text
    translatedText = ''
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    print("translatedText", translatedText)
    return translatedText

def translate_text(text, source_lang, target_lang):
    if(check_package_installed('argostranslate')):
        translated_text = translate(text, source_lang, target_lang)
        return translated_text
