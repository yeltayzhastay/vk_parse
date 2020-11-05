import vk
import time
import csv

class VK_Parsing:
    def __init__(self, token):
        session = vk.Session(access_token=token)
        self.vk_api = vk.API(session)
        self.result = []

    def parsing(self, group_urls, limit=100):
        results = [['group_url', 'user_id', 'first_name', 'last_name', 'sex', 'bdate', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'music', 'status', 'followers_count', 'relation',
        'city', 'country', 
        'alcohol', 'life_main', 'people_main', 'political', 'smoking', 'religion',
        'langs', 'inspired_by',
        'text', 'comments', 'likes', 'reposts', 'views']]

        for group_url in group_urls:
            members = self.get_members(group_url)
            for member in members[:limit]:
                row = [group_url] + self.get_person_info(member)
                try:
                    row += self.get_posts(member)
                except:
                    row += ''
                results.append(row)
        self.result = results

    def parsing_info(self, urls, limit=100):
        results = [['group_url', 'user_id', 'first_name', 'last_name', 'sex', 'bdate', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'music', 'status', 'followers_count', 'relation',
        'city', 'country', 
        'alcohol', 'life_main', 'people_main', 'political', 'smoking', 'religion',
        'langs', 'inspired_by']]

        for group_url in group_urls:
            members = self.get_members(group_url)
            for member in members[:limit]:
                results.append([group_url] + self.get_person_info(member))
        self.result = results

    def parsing_post(self, group_urls, limit=100):
        results = [['group_url', 'owner_id', 'text', 'comments', 'likes', 'reposts', 'views']]
        for group_url in group_urls:
            members = self.get_members(group_url)
            for member in members[:limit]:
                try:
                    results.append([group_url, member] + self.get_posts(member))
                except:
                    continue
        self.result = results

    def get_members(self, groupid):
        first = self.vk_api.groups.getMembers(group_id=groupid, v=5.92)
        data = first["items"]
        count = first["count"] // 1000
        for i in range(1, count+1):  
            data = data + self.vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*1000)["items"]
        return data
    
    def get_person_info(self, user_id):
        user_features = ['id', 'first_name', 'last_name', 'sex', 'bdate', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'music', 'status', 'followers_count', 'relation',
        'city', 'country', 
        'personal']
        personal_features = ['alcohol', 'life_main', 'people_main', 'political', 'smoking', 'religion',
        'langs', 'inspired_by']

        post_info = self.vk_api.users.get(user_id=user_id, v=5.92, fields='sex, bdate, city, country, status, followers_count, occupation, relatives, relation, personal, interests, music, movies, tv, books, games, about, quotes')[0]
        
        results = []
        for i in user_features:
            try:
                if i in ['city', 'country']:
                    results.append(post_info[i]['title'])
                elif i != 'personal':
                    results.append(post_info[i])
            except:
                results.append('')
            if i == 'personal':
                for j in personal_features:
                    try:
                        if j == 'langs':
                            results.append(' '.join(post_info[i][j]))
                        else:
                            results.append(post_info[i][j])
                    except:
                        results.append('')
        
        return results

    def get_posts(self, owner_id):
        post_features = ['text', 'comments', 'likes', 'reposts', 'views']

        post_info = self.vk_api.wall.get(owner_id=owner_id, v=5.92)['items']

        iter = 0
        text = ''
        clrv = {'comments': 0, 'likes': 0, 'reposts': 0, 'views': 0}
        for post in post_info:
            try:
                for j in post_features:
                    if j in ['comments', 'likes', 'reposts', 'views']:
                        clrv[j] += post[j]['count']
                    else:
                        text += post[j] + ' '
                    iter += 1
            except:
                continue
        return [text, clrv['comments']/iter, clrv['likes']/iter, clrv['reposts']/iter, clrv['views']/iter]

    def to_csv(self, name):
        with open('dataset/'+name, 'w', encoding='utf8') as result_file:
            writetocsv = csv.writer(result_file, delimiter=';', lineterminator='\n')
            for i in self.result:
                writetocsv.writerow(i)
        print('Successfully finished...')

def main():
    first_time = time.time()
    
    urls = ['samsung.galaxy_a', 'kupit_iphone_v_moskve', 'rumicomrussia', 'huaweip20', 'ru_oppo']
    token = "fe91c3a9fe91c3a9fe91c3a96efee5034cffe91fe91c3a9a13265b3a8814f5207fa1f50"

    vk_parse = VK_Parsing(token)
    vk_parse.parsing(urls, 10000)
    vk_parse.to_csv('vk_dataset_2.csv')

    print('Parsing data finished!', round(time.time() - first_time, 2), 'sec')

if __name__ == "__main__":
    main()