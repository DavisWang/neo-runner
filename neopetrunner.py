import time, random, sys
import urllib, urllib2
import mechanize
from bs4 import BeautifulSoup

"""TODO: do method for getting neopoints
do auto food club betting/collecting
refactor/clean up code
"""

b = mechanize.Browser()

def init():
    b.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]


def login():
    print "Logging in"
    b.open("http://www.neopets.com/login/")

    username=sys.argv[1]
    password=sys.argv[2]

    b.select_form(nr=0)
    b.form["username"] = username
    b.form["password"] = password
    b.submit()
    b.open('http://www.neopets.com/inventory.phtml')
    assert b.title() == 'Neopets - Inventory'

def randomize():
    print "Calling randomize to avoid detection"
    list = ['http://www.neopets.com/explore.phtml',
    'http://www.neopets.com/island/tradingpost.phtml',
    'http://www.neopets.com/games/',
    'http://www.neopets.com/objects.phtml',
    'http://www.neopets.com/market_bazaar.phtml',
    'http://www.neopets.com/market.phtml?type=wizard',
    'http://www.neopets.com/battledome/battledome.phtml',
    'http://www.neopets.com/market.phtml?type=your']
    time.sleep(random.uniform(0,3))
    b.open(list[random.randint(0,len(list)-1)])
    time.sleep(random.uniform(0,1))

def buyStock():
    print "Buying stocks"
    priceIndex = 5
    tickerIndex = 1
    numToBuy = 1000
    b.open("http://www.neopets.com/stockmarket.phtml?type=list&bargain=true")
    soup = BeautifulSoup(b.response().read())
    table = soup.find('table',align='center')
    rows = table.find_all('tr')

    for row in rows:
        price = row.find_all('td')[priceIndex].get_text()
        ticker = row.find_all('td')[tickerIndex].get_text()
        #print ticker, 'is trading at ', price
        if not price.isdigit() or int(price) < 15:
            continue
        else:
            break
    b.open("http://www.neopets.com/stockmarket.phtml?type=buy")
    b.select_form(nr=1)
    b.form["ticker_symbol"] = ticker
    b.form["amount_shares"] = str(numToBuy)
    respose = b.submit()
    print "Bought",numToBuy,"shares of",ticker,"for",price,"each,total cost:",int(price)*numToBuy
    #currently does no verification, maybe will do soon

def oneclickdailies():
    print "Running dailies"
    snowager()
    #adventcalendar()
    buriedtreasure()
    randomize()
    tombola()
    randomize()
    shrine()
    randomize()
    fruitmachine()
    randomize()
    fishingvortex()
    randomize()
    omelette()
    randomize()
    jelly()
    randomize()
    bankinterest()
    foodclubodds()
    monthlyfreebies()

def buriedtreasure():
    print "Running buried treasure"
    x = random.randint(1,475)
    y = random.randint(1,475)
    url = "http://www.neopets.com/pirates/buriedtreasure/buriedtreasure.phtml?"+str(x)+","+str(y)
    print "Coordinates are",x, "and",y
    b.open(url)
    if "won" in b.response().read():
        print "WINNER IN BURIED TREASURE"
    else:
        print "Not a winner in buried treasure"

def tombola():
    print "Running Tombola"
    b.open("http://www.neopets.com/island/tombola.phtml")
    b.select_form(nr=1)
    b.submit()

    if "winner!" in b.response().read():
        print "WINNING TICKET IN TOMBOLA"
    else:
        print "Not a winning ticket in Tombola"

def shrine():
    print "Running Shrine"
    b.open("http://www.neopets.com/desert/shrine.phtml")
    b.select_form(nr=1)
    b.submit()

    if ("Nothing" or "nothing") in b.response().read():
        print "Nothing happens for Shrine"
    else:
        print "WINNER IN SHRINE"

def fruitmachine():
    print "Running Fruitmachine"
    #not sure if this works, since it's flash based
    b.open("http://www.neopets.com/desert/fruit/index.phtml")
    b.select_form(nr=1)
    b.submit()

def fishingvortex():
    print "Running fishing vortex"
    b.open("http://www.neopets.com/water/fishing.phtml")
    b.select_form(nr=1)
    b.submit()

def omelette():
    print "Running Omelette"
    #if the omelette or jelly doesn't exist, then it just goes back to the map
    #because that is the second form
    b.open("http://www.neopets.com/prehistoric/omelette.phtml")
    try:
        b.select_form(nr=1)
        b.submit()
    except Exception:
        print "Some error has occurred!"

def jelly():
    print "Running jelly"
    b.open("http://www.neopets.com/jelly/jelly.phtml")
    try:
        b.select_form(nr=1)
        b.submit()
    except Exception:
        print "Some error has occurred!"

def monthlyfreebies():
    #mothly only
    print "Running Monthly freebies"
    b.open("http://www.neopets.com/freebies/index.phtml")

def bankinterest():
    print "Running Bank interest"
    b.open("http://www.neopets.com/bank.phtml")
    try:
        b.select_form(nr=3)
        b.submit()
    except Exception:
        print "Some error has occurred!"

def snowager():
    print "Running Snowager"
    b.open("http://www.neopets.com/winter/snowager.phtml")
    try:
        b.select_form(nr=0)
        b.submit()
    except Exception:
        print "Some error has occurred!"

def adventcalendar():
    print "Running AdventCalendar"
    b.open("http://www.neopets.com/winter/adventcalendar.phtml")
    try:
        b.select_form(nr=1)
        b.submit()
    except Exception:
        print "Some error has occurred!"

def getpetstats(name):
    #pretty bad implementation, but it does the job, may cause issues later on
    b.open("http://www.neopets.com/island/training.phtml?type=status")
    soup = BeautifulSoup(b.response().read())
    table = soup.find('table',align='center')
    rows = table.find_all('tr')

    petexists = False
    stats = {}
    for row in rows:
        if petexists:
            list = row.find('td').get_text().split(":")
            for i in list:
                if i[1].isdigit():
                    if len(stats) == 0:
                        stats['Lvl'] = i[:-4].strip()
                    elif len(stats) == 1:
                        stats['Str'] = i[:-4].strip()
                    elif len(stats) == 2:
                        stats['Def'] = i[:-4].strip()
                    elif len(stats) == 3:
                        stats['Mov'] = i[:-4].strip()
                    elif len(stats) == 4:
                        stats['Hp'] = i.split("/")[1].strip()
            break
        if name in row.get_text():
            petexists = True
    return stats

def enrolltrainingschool(petname, coursetype):
    b.open("http://www.neopets.com/island/training.phtml?type=courses")
    b.select_form(nr=1)
    b.form['course_type'] = [coursetype]
    b.form['pet_name'] = [petname]
    b.submit()

def paytrainingschool(petname):
    print "Paying training school"
    #assumes we have the req'd codestones
    #does nothing if in training
    url = "http://www.neopets.com/island/process_training.phtml?type=pay&pet_name=" + petname
    b.open(url)

def completetraining():
    print "Completing training course"
    b.open("http://www.neopets.com/island/training.phtml?type=status")
    try:
        b.select_form(nr=1)
        b.submit()
    except Exception:
        print "Some error has occurred!"

def trainpet(petname):
    #currently we are indifferent to which stat we train, as long as it's str, def, or hp, lvl has lowest priority

    #we need to first determine the stat to train
    #currently, we'll just pick any that is less than half our level

    #complete our training first, this may fail if we train more than one pet at a time
    stats = getpetstats(petname)
    print "Before completing training", petname, "has the following stats:"
    print stats

    completetraining()

    stats = getpetstats(petname)
    print "After completing training", petname, "has the following stats:"
    print stats

    level = int(stats['Lvl'])
    strength = int(stats['Str'])
    defense = int(stats['Def'])
    movement = int(stats['Mov'])
    hp = int(stats['Hp'])

    if strength / 2 >= level or defense / 2 >= level or hp / 2 >= level or movement / 2 >= level:
##    if (strength / 2 or defense / 2 or hp /2 or movement /2) >= level:
        coursetype = "Level"
    elif strength == min(strength,defense,hp):
        coursetype = "Strength"
    elif defense == min(strength,defense,hp):
        coursetype = "Defence"
    elif hp == min(strength,defense,hp):
        coursetype = "Endurance"

    print 'Enrolling', petname, 'in', coursetype
    enrolltrainingschool(petname, coursetype)
    paytrainingschool(petname)
    #wait, then complete course

def zappet(petname):
    print "Zapping pet:", petname
    stats = getpetstats(petname)
    print "Before zapping pet", petname, "has the following stats:"
    print stats

    b.open("http://www.neopets.com/lab2.phtml")
    try:
        b.select_form(nr=1)
        b.form.set_value([petname], name='chosen')
        b.submit()
        stats = getpetstats(petname)
        print "After zapping pet", petname, "has the following stats:"
        print stats
        print "Done zapping pet:", petname
    except Exception:
        print "Some error has occurred!"

def doubleornothing():
    b.open('http://www.neopets.com/medieval/doubleornothing.phtml')


def foodclubodds():
    print "Calculating today's food club odds"
    #calculate the food club oddsd to see if there are any arbitrage situations
    b.open("http://www.neopets.com/pirates/foodclub.phtml?type=bet")
    soup = BeautifulSoup(b.response().read())
    betform = soup.find('form', action='process_foodclub.phtml')
    scripttags = betform.find_all("script")
    dict = {}
    listcounter = 0
    paircounter = 0
    #list counter is the index of the list, there are 5 of them
    #pair counter is the index of the contestants, there are 4 of them per list
    #as it curerntly stands, 50 is the max bet amount
    for tag in scripttags:
        for pair in tag.get_text().strip().split('\n'):
            cell = pair.split('=')
            index = str(listcounter) + str(paircounter)
            if listcounter == 5:
                dict[index] = (cell[1]).strip()
            else:
                dict[index] = (cell[1])[:-1].strip()
            paircounter+=1
        listcounter+=1
        paircounter=0

    oddsum = 0.0
    for i in range(0,6):
        if i == 5:
            print 'Max bet amount is:', dict['50']
            break
        for j in range(0,4):
            oddsum+= 1.0/int(dict[str(i)+str(j)])

        print 'List %s has cumulative odds: %s' %(i,oddsum)
        oddsum=0.0
    print 'Done processing food club odds'

#should save the previous url as this will go to the inventory
def getNPs():
    b.open('http://www.neopets.com/inventory.phtml')
    soup = BeautifulSoup(b.response().read())
    # print soup.find(id="npanchor").string
    return int(soup.find(id="npanchor").string.replace(",",""))


def main():
    print 'Welcome to the Neopets Runner!'
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) == 4 or len(sys.argv) == 5:
        init()
        login()
        print "You have", getNPs(), "NPs"

        if len(sys.argv) == 4:
            #a for all, d for dailies only, b for buy stock
            #format python neopetrunner.py [a|d|b] or any combo
            if 'a' in sys.argv[3]:
                oneclickdailies()
                buyStock()
                foodclubodds()
            else:
                if 'd' in sys.argv[3]:
                    oneclickdailies()
                if 'b' in sys.argv[3]:
                    buyStock()
                if 'fc' in sys.argv[3]:
                    foodclubodds()
                else:
                    print "Please use proper parameters!"

        #options at the moment, only trainpet, format: python neopetrunner.py train <petName>
        elif len(sys.argv) == 5:
            assert sys.argv[3] == 'train' or 'all' or 'lab'
            # assert sys.argv[4] == 'X_Avon_X' #let's stick with this for now

            if sys.argv[3].lower() == 'train':
                trainpet(sys.argv[4])
            elif sys.argv[3].lower() == 'lab':
                zappet(sys.argv[4])
            elif sys.argv[3].lower() == 'all':
                oneclickdailies()
                buyStock()
                zappet(sys.argv[4])
                trainpet(sys.argv[4])

        print "You have", getNPs(), "NPs"
    else:
        print "Please use proper parameters!"

    print 'Done'

def test():
    init()
    login()
    b.open('http://www.neopets.com/inventory.phtml')
    # print b.response().read()
    print "you have", getNPs(), "NPs"

if __name__ == '__main__':
    main()
    # test()

