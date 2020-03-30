from datetime import date
from settings import  *
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def log_errors_and_runtime(errors, delta, log_dir):

    errors = "\n".join(errors)
    date_str = date.today().strftime("%d%m%Y")
    outfile = date_str + '.txt'
    outpath = os.path.join(log_dir, outfile)

    with open(outpath, 'w+') as filehandle:
        filehandle.writelines(f"errors:{errors}")
        filehandle.writelines('\n---------------------\n')
        filehandle.writelines(f"time elapsed in seconds: {delta}")
        filehandle.writelines('\n---------------------\n')


def update_ref_log(hrefs,new_refs, hrefs_path):

    new_refs = pd.DataFrame(new_refs, columns=["href"])
    hrefs = pd.concat([hrefs,new_refs],axis = 0, ignore_index=True, sort=False)
    hrefs.to_csv(hrefs_path, index_label = 'id')


def timeout_get_request(browser, timeout = 50):

    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='search-toolbar-logo']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()


def verbose(i, arrsize):
    print(f'this is iteration number:{i + 1} from {arrsize}')

def download_csv_from_all_links(new_refs):

    errors = []
    for i, ref in enumerate(new_refs):

        verbose(i, len(new_refs))
        try:
            container = pd.read_html(ref)
            # date = "-".join(container[1][1].to_list())
            df = container[-1]
            df['ref'] = ref

            date_str = re.search('\d+',ref).group()
            date_obj = date.strptime(date_str, '%Y%m%d')
            df['date'] = date_obj

            date_repr_to_file = date_obj.strftime('%b-%d-%Y')

            outfile = date_repr_to_file + '.csv'
            outpath = os.path.join(data_dir, outfile)
            df.to_csv(outpath)
        except:
            print('error')
            errors.append(ref)

    return errors


def get_all_urls(browser, url_pattern):

    refs = []
    elems = browser.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        ref = elem.get_attribute("href")
        match = re.search(url_pattern, ref)
        if match:
            refs.append(match.group())
    return refs

def get_fresh_urls(browser, prev_refs, url_pattern):

    # Read all hrefs from html script
    refs = get_all_urls(browser, url_pattern)
    new_refs = set(refs) - set(prev_refs)
    return new_refs