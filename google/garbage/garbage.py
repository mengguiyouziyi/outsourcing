# def _js_click(driver, real_url):
#     # try:
#     driver.get(real_url)
#     driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]').click()
#     time.sleep(6)
#     cross = driver.find_element_by_xpath('//div[@class="IA8gLe"]')
#     print(cross.get_attribute('outerHTML'))
#     cross.click()
#     # except Exception as e:
#     #     print(e.args[0], e.args[1])
#     #     try:
#     #         driver.get(real_url)
#     #         driver.find_element_by_xpath('//a[@class="wXeWr islib nfEiy mM5pbd"]').click()
#     #         time.sleep(6)
#     #         cross = driver.find_element_by_xpath('//div[@class="IA8gLe"]')
#     #         print(cross.get_attribute('innerHTML'))
#     #         cross.click()
#     #     except:
#     #         print(e.args[0], e.args[1])
#     #         return
#     #     else:
#     #         return True
#     # else:
#     return True

# driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
# is_generate = _js_click(driver, real_url)
# if is_generate:
#     driver.quit()
#     os.rmdir(item_dir)
#     return True
# for pic_a in pic_as:
#     pic_url = pic_a.get_attribute('href')
#     site_url = pic_a.find_element_by_xpath('//div[@class="fxgdke"]').text
# pic_name = '{} {}_1'.format(kw, time_now)
#
# for b in driver.find_elements_by_xpath('//a[@class="VFACy kGQAp"]'):
#     print(b.get_attribute('outerHTML'))
#     print(b.find_element_by_class_name('fxgdke').get_attribute('outerHTML'))
#     print(b.find_element_by_class_name('fxgdke').text)
"""    xls_lst = [
        [
            pic_a.get_attribute('href'),
            pic_a.find_element_by_class_name('fxgdke').text.replace(' · 有货', '') if pic_a.find_element_by_class_name(
                'fxgdke').text else '',
            '{} {}_{}'.format(kw, time_now, i + 1),
            '{} {}_{}m'.format(kw, time_now, i + 1)
        ] for i, pic_a in enumerate(pic_as)
    ]"""