from selenium import webdriver
import time
import csv

class Parsing:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.profile_features = ['Birthday:', 'Current city:', 'Company:', 'Website:', 'Languages:', 
                                'Instagram:', 'Twitter:', 'Facebook:', 'College or university:', 'Political views:', 
                                'Religion:', 'Personal priority:', 'Important in others:', 'Views on smoking:', 'Views on alcohol:',
                                'Inspired by:', 'Favorite movies:', 'Favorite quotes:']
        self.page_features = ['followers', 'posts', 'photos', 'gifts']

    def ParsingData(self, listofurl, limit):
        first_time = time.time()
        result = [['group_url', 'person_url', 'name'] + self.profile_features + self.page_features]
        for _, url in enumerate(listofurl):
            person_urls = self.GetPersonsFromGroup(url, limit)
            for __, person_url in enumerate(person_urls):
                person = self.GetPersonalInfo(person_url)
                result.append([url] + person)

        self.driver.close()
        self.result = result
        print('Parsing data finished!', round(time.time() - first_time), 'sec')

    def GetPersonalInfo(self, url):
        self.driver.get(url)

        try:
            name = self.driver.find_element_by_class_name('page_name').text
        except:
            name = 'NA'

        try:
            self.driver.find_element_by_css_selector("#profile_short > div.profile_more_info > a").click()
        except:
            pass

        try:
            profile_info_row = self.driver.find_elements_by_xpath("//div[@class='clear_fix profile_info_row ']")
            profile_infos = {}
            for i in profile_info_row:
                try:
                    row = i.text.split('\n')
                    profile_infos[row[0]] = row[1]
                except:
                    pass
        except:
            profile_infos = {}


        try:
            page_counter = self.driver.find_elements_by_xpath("//a[@class='page_counter']")
            page_counts = {}
            for i in page_counter:
                row = i.text.split('\n')
                page_counts[row[1]] = row[0]
        except:
            page_counts = {}

        results = [url, name]

        for i in self.profile_features:
            try:
                results.append(profile_infos[i])
            except:
                results.append('NA')
        for i in self.page_features:
            try:
                results.append(page_counts[i])
            except:
                results.append('NA')

        return results

    def GetPersonsFromGroup(self, url, limit):
        result = []
        self.driver.get(url)

        SCROLL_PAUSE_TIME = 0.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while limit:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #[i.click for i in self.driver.find_elements_by_css_selector(".replies_next")]
            time.sleep(SCROLL_PAUSE_TIME)
            '''
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            '''
            limit -= 1
        person_urls = self.driver.find_elements_by_xpath("//a[@class='author']")
        for elem in person_urls:
            try:
                result.append(elem.get_attribute("href"))
            except:
                pass
        return list(set(result))

    def to_csv(self, name):
        with open('dataset/'+name, 'w', encoding='utf8') as result_file:
            writetocsv = csv.writer(result_file, delimiter=';', lineterminator='\n')
            for i in self.result:
                writetocsv.writerow(i)
        print('Successfully finished...')
    '''
    def ScrollingDown(self, limit):
        SCROLL_PAUSE_TIME = 1
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while limit:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            limit -= 1
    '''

def main(num_scrolls: int):
    urls = ['https://vk.com/samsung.galaxy_a', 'https://vk.com/baraholka_apple_vmoskve', 'https://vk.com/rumicomrussia', 'https://vk.com/huaweip20', 'https://vk.com/ru_oppo']
    parse = Parsing()
    parse.ParsingData(urls, num_scrolls)
    parse.to_csv('5g.csv')

if __name__ == "__main__":
    main(20)