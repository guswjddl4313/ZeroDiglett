import optparse
from modules.wordpress_crawler import SlugList, SlugDownload
#from modules.exploit.cross_site_scripting import class_name
#from modules.exploit.sql_injection import class_name
#from modules.exploit.php_object_injection import class_name


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