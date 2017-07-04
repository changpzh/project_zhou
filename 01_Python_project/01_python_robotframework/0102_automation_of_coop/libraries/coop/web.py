''' web testing libraries, based on selenium2 '''
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import re
import time
from robot.running import EXECUTION_CONTEXTS
from glob import glob
import json

_display = None
_driver = None


def start_new_display(visible=0, width=1600, height=900):
    global _display
    if _display is None:
        _display = Display(visible=int(visible), size=(int(width), int(height)))
    _display.start()


def stop_created_display():
    global _display
    if _display:
        _display.stop()


def create_new_firefox_driver(proxy=None):
    global _driver
    profile = webdriver.FirefoxProfile()
    if proxy:
        profile.set_proxy(webdriver.Proxy(proxy))
    _driver = webdriver.Firefox(profile)
    _driver.get_log('browser') # clear browser startup logs

    return _driver


def _driver_is_ready(f):
    ''' decorator function, to check _driver intialization '''
    def new_f(*args, **kwargs):
        global _driver
        if _driver is None:
            raise RuntimeError('webdriver is not initialized')

        return f(*args, **kwargs)

    new_f.func_name = f.func_name

    return new_f


@_driver_is_ready
def quit_web_driver():
    _driver.quit()


@_driver_is_ready
def open_url(url):
    print '*INFO* open url "%s"' % url
    #_driver.get_log('browser')
    _driver.get(url)


@_driver_is_ready
def title_should_be(expect_title):
    _should_be_equal(_driver.title, expect_title)


@_driver_is_ready
def get_all_links():
    links = _driver.find_elements_by_tag_name('a')
    #return list(set([e.get_attribute('href').strip('#/').replace(r'.*html/temp/.*html','') for e in links if e.get_attribute('href')]))
    return list(set([e.get_attribute('href').strip('#/') for e in links if e.get_attribute('href')]))


def get_excluded_links(links, *excluded_links):
    return [e for e in links if e not in excluded_links and ('/html/temp/' not in e) and ('ppt' not in e)\
             and ('issue_list' not in e) and ('/html/quality_metrics/' not in e)\
#             and ('/html/metrics/ci_daily.html' not in e) \
#             and ('/html/metrics/sc_commit_metrics.html' not in e) \
#             and ('javascript:void(0)' not in e) \
#             and ('/html/dashboard/global/PCIDashboard.html?type=scbuild' not in e) \
#             and ('/html/dashboard/global/QTDashboard.html' not in e) \
#             and ('PCIDashboard.html' not in e) \
#             and ('Jane.html' not in e)\
#             and ('readme.html' not in e)\
#             and ('api_monitor.html' not in e)\
            ]


@_driver_is_ready
def no_js_errors():
    browser_logs = _driver.get_log('browser')
    #print '###%s' % (browser_logs)
    error_logs = filter(lambda log: log['level'] in ('ERROR', 'SEVERE'), browser_logs)
    if error_logs:
        print '*WARN* Exist error:%s' % '\n'.join(
            ['%s - %s - %s' % (e['level'], e['timestamp'], e['message']) for e in error_logs])
        #print '###%s' % (browser_logs)
        #print '###%s' % (error_logs)
    _should_be_equal(error_logs, [])


def _should_be_equal(actual, expect):
    if actual != expect:
        capture_screenshot()
        raise RuntimeError('"%s" != "%s"' % (actual, expect))


@_driver_is_ready
def wait_until_page_contains_element_id(element_id, timeout=10, interval=1):
    start_time = time.time()
    while time.time() - start_time < int(timeout):
        try:
            _driver.find_element_by_id(element_id)
            break
        except NoSuchElementException:
            time.sleep(interval)
    else:
        capture_screenshot()
        raise RuntimeError('"%s" undetected in "%s sec"' % (element_id, timeout))
    
@_driver_is_ready
def wait_until_page_contains_element_tag_name(element_tag_name, timeout=10, interval=1):
    start_time = time.time()
    while time.time() - start_time < int(timeout):
        try:
            _driver.find_element_by_tag_name(element_tag_name)
            break
        except NoSuchElementException:
            time.sleep(interval)
    else:
        capture_screenshot()
        raise RuntimeError('"%s" undetected in "%s sec"' % (element_tag_name, timeout))
    
@_driver_is_ready
def get_response_data(element_tag_name):
    result = _driver.find_element_by_tag_name(element_tag_name)    
    return result.text

@_driver_is_ready
def get_response_json_result(element_tag_name):
    result = _driver.find_element_by_tag_name(element_tag_name)    
    return json.loads(result.text)

_SCREENSHOT_PTN = re.compile(r'screen-(\d+)\.png')
@_driver_is_ready
def capture_screenshot():
    output_dir = _get_output_dir()
    screenshots = glob(os.path.join(output_dir, 'screen-*.png'))
    screenshot_ids = map(lambda x: int(_SCREENSHOT_PTN.search(x).group(1)), screenshots) or [0]
    img_name = 'screen-%d.png' % (max(screenshot_ids) + 1)
    img_path = os.path.join(output_dir, img_name)
    if not _driver.save_screenshot(img_path):
        raise RuntimeError('failed to save screenshot "%s"' % img_path)
    print '*HTML* </td></tr><tr><td colspan="3"><a href="%s"><img src="%s"></img></a>' % (img_name, img_name)


def _get_output_dir():
    current = EXECUTION_CONTEXTS.current
    if current:
        return current.variables['${OUTPUT DIR}']
    return os.path.abspath(os.curdir)

# errors = []
# def get_data_from_coop(url):
#     try:
#         req = urllib2.Request(url)
#         res = urllib2.urlopen(req).read().decode('utf-8')        
#         decode_res = json.loads(res)       
#     except urllib2.HTTPError as err:
#         print err, 'message:', err.read()
#     except Exception,err:
#         errors.append(['url is:\n', url, '\n\nerr:\n', err.read()])
#         if errors:
#             print "got errors:\n"
#             for error in errors:
#                 print '\n ', error        
#     return decode_res

