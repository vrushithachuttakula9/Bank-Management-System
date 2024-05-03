def entryBannerPrinting():
    with open('entry_banner.txt', 'r') as entryBanner_file:
        inbanner = entryBanner_file.read()
    print(inbanner)

def exitBannerPrinting():
    with open('exit_banner.txt', 'r') as exitBanner_file:
        outbanner = exitBanner_file.read()
    print(outbanner)