import optparse, os
from modules.wordpress_crawler import SlugList, SlugDownload
from modules.exploit.cross_site_scripting import XSS
#from modules.exploit.sql_injection import class_name
#from modules.exploit.php_object_injection import class_name

PLUGINSS_DIR = "plugins"  # 플러그인 소스 코드 디렉터리
RESULTS_DIR = "results"  # 결과 저장 디렉터리

if __name__ == "__main__":
    parser = optparse.OptionParser('-u -d 2 5 -x <option> -p <option> -s <option>')
    parser.add_option('-u', '--update', dest='update', help='update slug list')
    parser.add_option('-d', '--download', dest='download', nargs=2, type='int', help='Download items starting from the specified line number. '
        'The first argument is the starting line, and the second argument is the number of items to download.')

    (options, args) = parser.parse_args()


    if options.update:
        SlugList().get_slug_list()
    elif options.download:
        first_num, count = options.download
        SlugDownload().get_plugin(first_num, count)
        
        
    # 다운로드한 플러그인 디렉터리 목록 가져오기
    plugin_dirs = [f for f in os.listdir(PLUGINSS_DIR) if os.path.isdir(os.path.join(PLUGINSS_DIR, f))]
    
    # 결과 저장 디렉터리 생성
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # 각 플러그인 디렉토리에 대해 XSS 검사 실행
    for plugin in plugin_dirs:
        plugin_path = os.path.join(PLUGINSS_DIR, plugin)
        
        # 플러그인 정보 가져오기
        slug_version = "unknown_version"
        with open("slug_list/slug_list.txt", "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == plugin:
                    slug_version = parts[1]
                    break

        # 플러그인별 결과 저장 디렉토리 설정
        plugin_result_dir = os.path.join(RESULTS_DIR, f"{plugin}_{slug_version}", "XSS")
        os.makedirs(plugin_result_dir, exist_ok=True)

        print(f"[*] {plugin} 플러그인(XSS 검사) -> 결과 저장: {plugin_result_dir}")
        scanner = XSS(plugin_path, plugin_result_dir)
        scanner.run_scan()