from selenium import webdriver
path="C:\\ProgramData\\Anaconda3-5.2.0\\BrowersDriver\\chromedriver.exe"
browser=webdriver.Chrome(path)
logs = browser.get_log('browser')

try:
    browser.get("http://localhost:8000")
    print(logs)
    assert 'Django' in browser.title
finally:
    browser.close()
    browser.quit()

