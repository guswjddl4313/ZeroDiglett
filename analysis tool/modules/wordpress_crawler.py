from bs4 import BeautifulSoup
import os
import re
import requests
import threading
import zipfile

# 워드프레스 slug 리스트 및 다운로드 url
slug_list_url = "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[page]="
slug_download_url = "https://api.wordpress.org/plugins/info/1.0/"

# 워드프레스 slug 리스트 최대 페이지 수
slug_list_page_max_num = 999

# 저장 파일 및 디렉토리 설정
plugins_dir = 'plugins/'
slug_list_dir = 'slug_list/'
slug_list_file_name = 'slug_list.txt'

# 디렉토리 생성
if not os.path.exists(plugins_dir):
    os.makedirs(plugins_dir)
if not os.path.exists(slug_list_dir):
    os.makedirs(slug_list_dir)


### slug 리스트 가져오기
class SlugList:
    def __init__(self):
        self.url = slug_list_url
        self.page_max = slug_list_page_max_num + 1
        self.slug_list_file = slug_list_dir + slug_list_file_name

    ## 기존 slug 목록 불러오기
    def load_existing_slugs(self):
        existing_slugs = {}

        if os.path.exists(self.slug_list_file): # 파일이 존재할 때만 처리
            with open(self.slug_list_file, 'r') as f:
                for line in f: #slug_list.txt 파일을 한 줄씩 읽어서 처리
                    parts = line.strip().split(maxsplit=1)  # 공백을 기준으로 최대 2개의 값만 분리

                    if len(parts) == 2:  # slug와 version이 모두 있는 경우에만 처리
                        slug, version = parts # slug와 version을 각각 변수에 저장
                        existing_slugs[slug] = version # 딕셔너리에 추가
                    else:
                        print(f"error line: {line.strip()}")  # 로그 출력하여 문제를 파악할 수 있게 함
        return existing_slugs # 기존 slug 목록 반환

    ## 업데이트된 slug 목록 쓰기
    def write_updated_slugs(self, existing_slugs):
        # 기존 슬러그 목록을 모두 다시 쓰기 (업데이트 사항 반영)
        with open(self.slug_list_file, 'w') as f:  # 'w' 모드로 파일 덮어쓰기 (이전 내용 삭제 -> 새로운 내용 추가)
            for slug, version in existing_slugs.items(): # 딕셔너리의 key와 value를 각각 slug, version에 저장
                f.write(f"{slug} {version}\n") 

    ## slug 리스트 가져오기
    def get_slug_list(self):
        print("[*]Getting slug list...")
        existing_slugs = self.load_existing_slugs() # 기존 slug 목록 불러오기

        for page in range(1, self.page_max): # 1부터 page_max까지 반복
            url = self.url + str(page)
            response = requests.get(url)
            data = response.json() # json 형태로 데이터를 가져옴

            updated = False  # 업데이트가 있는지 여부

            for plugin in data['plugins']:
                slug = plugin['slug'] # 플러그인 슬러그
                version = plugin['version'] # 플러그인 버전
                
                #기존에 슬러그 존재하면 버전 다른지 확인
                if slug in existing_slugs:
                    if existing_slugs[slug] != version:
                        print(f"[>]Update: {slug} {existing_slugs[slug]} -> {version}")
                        existing_slugs[slug] = version
                        updated = True
                #새로운 슬러그
                else:
                    print(f"[+]New Plugin: {slug} {version}")
                    existing_slugs[slug] = version
                    updated = True

            # 업데이트 즉시 반영
            if updated:
                self.write_updated_slugs(existing_slugs)

        

class SlugDownload:
    def __init__(self):
        self.url = slug_download_url
        self.slug_list_file = slug_list_dir + slug_list_file_name

    def download(self, slug): # 플러그인 다운로드 함수
        url = self.url + slug # 다운로드 링크 + 슬러그
        response = requests.get(url)

        result = {}
        matches = re.findall(r's:(\d+):"(.*?)";|i:(\d+);|b:(\d);|a:(\d+):{|}', response.text) # 직렬화된 데이터 파싱
    
        i = 0
        while i < len(matches): # 위 정규표현식으로 파싱한 결과를 딕셔너리로 변환
            if matches[i][0]:
                key = matches[i][1]
                i += 1
                if matches[i][0]:
                    value = matches[i][1]
                elif matches[i][2]:
                    value = int(matches[i][2])
                elif matches[i][3]:
                    value = bool(matches[i][3])
                else:
                    value = None
                result[key] = value
            i += 1
        
        print("[^]Download Plugin")
        print(f"slug : {result['slug']}")
        print(f"version : {result['version']}\n")

        plugin_zip_url = result['trunk'] # 플러그인 다운로드 링크

        plugin_zip = requests.get(plugin_zip_url) # 플러그인 다운로드 zip
        with open(plugins_dir + slug + '.zip', 'wb') as f:
            f.write(plugin_zip.content)

    def read_plugin_list(self, first_idx, count): # slug 리스트 파일에서 플러그인 목록 읽기
        idx = first_idx - 1
        with open(self.slug_list_file, 'r') as f:
            lines = f.readlines()
            return lines[idx:idx+count]
        
    def get_plugin(self, first_idx, count): # 입력받은 인덱스만큼 플러그인 다운로드
        slugs = self.read_plugin_list(first_idx, count)
        for slug in slugs:
            slug = slug.split()[0]
            self.download(slug)
            self.extract_zip(slug)

    def extract_zip(self, slug): # 다운로드 받은 플러그인 압축 해제
        with zipfile.ZipFile(plugins_dir + slug + '.zip', 'r') as zip_ref:
            zip_ref.extractall(plugins_dir + slug)
        os.remove(plugins_dir + slug + '.zip')



