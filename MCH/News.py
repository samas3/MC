import feedparser,time, html
def news():
    src = ['https://www.minecraftglobal.com/feed/','http://www.9minecraft.net/feed/','https://wikiminecraft.com/feed/']
    s = ''
    for url in src:
        feed = feedparser.parse(url)
        # print("News Source:",feed.channel.title)
        s += "News Source: " + feed.channel.title + '\n'
        # print("There are",len(feed.entries),"pieces of news from this source.\n")
        s += "There are " + str(len(feed.entries)) + " pieces of news from this source.\n\n"
        for e in feed.entries:
            # print('%-70s%s     By %s' %('[ '+e.title+' ]',time.strftime("%b/%d/%Y,%H:%M:%S(%a)", e.published_parsed),e.author))
            s += html.unescape('%-70s%s     By %s\n' %('[ '+e.title+' ]',time.strftime("%b/%d/%Y,%H:%M:%S(%a)", e.published_parsed),e.author))
            # print('>>',e.description[3:200],'...[',e.link[0:100],']')
            s += html.unescape('>> ' + e.description[3:200] + ' ...[ ' + e.link[0:100] + ' ]\n')
        # print('\n\n')
        s += '\n\n'
    return s
if __name__ == '__main__':
    print(news())
