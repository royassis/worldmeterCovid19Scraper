from functions import *
from selenium import webdriver


browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

link_f = link_factory(browser,WAYBACK_MACHINE_CORONA_URL)
link_f.get_all_urls()

old_urls = get_prev_urls()
list_filter = in_list_filter(old_urls)
reg_filter = regex_filter(URL_REGEX_PATTERN)

link_f.add_filter(in_list_filter)
link_f.add_filter(regex_filter)

link_f.validate_urls()
link_f.valid_urls

link_f.quit()