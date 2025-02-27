import optparse
from modules.wordpress_crawler import SlugList, SlugDownload
#from modules.exploit.cross_site_scripting import class_name
#from modules.exploit.sql_injection import class_name
#from modules.exploit.php_object_injection import class_name


if __name__ == "__main__":
    # parser = optparse.OptionParser('-u <option> -d <option> -x <option> -p <option> -s <option>')
    # parser.add_option('-u', dest='update', type='string', help='update slug list')

    # options, args = parser.parse_args()

    # print(parser.usage)
    # try:
    #     options, args = getopt.getopt(sys.argv[1:], 'u:d:xps')
    #     print(options)

    #     if options == []:
    #         print("haha")

    #     for op, p in options:
    #         if op == '-u' or op == '--update':
    #             print(f'option -u : {p}')
    #             #SlugList.get_slug_list()
    #         elif op == '-d' or op == '--download':
    #             print(f'option -d : {p}')
    #             #SlugDownload().download_plugin(p)
    #         elif op == '-x' or op == '--XSS':
    #             print(f'option -x : {p}')
    #         elif op == '-p' or op == '--POI':
    #             print(f'option -p : {p}')
    #         elif op == '-s' or op == '--SQL':
    #             print(f'option -s : {p}')

    # except getopt.GetoptError as e:
    #     print(USAGE)
    SlugList().get_slug_list()
    SlugDownload().get_plugin(2, 5)