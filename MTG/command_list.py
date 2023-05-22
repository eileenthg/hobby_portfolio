#command list
import sqlite3

conn = sqlite3.connect('library.sqlite')
cur = conn.cursor()

#===TODO===#
#warn orphaned/empty traits in db feat

#====UTILITY===#
#turn everytning to a specified case and split words by specified character
def cleanup(x, y, z):
    if z == "low":
        cased = x.lower()
    elif z == "hi":
        cased = x.upper()
    else: cased = x
    splitted = cased.split(y)
    result = []
    for key in splitted :
        a = key.strip()
        result.append(a)
    return result

#displays data about a card from db. (must assign label, remember to do cur.execute and join beforehand)
def cardstuff():
    fetch = cur.fetchall()
    cycle = 0
    x = None
    for stuff in fetch:
        if cycle == 0: x = stuff[0]
        else: x = x + ", " + stuff[0]
        cycle = cycle + 1
    cycle = 0
    return x

#view/edit card interface, accesible from multiple places
def viewcard(card_id):
    run = 1
    while run == 1:
        cur.execute("SELECT card, cost, power, toughness, text FROM Cards where id = ?", (card_id, ))
        cardraw = cur.fetchone()
        card = cardraw[0]
        cost = cardraw[1]
        power = cardraw[2]
        toughness = cardraw[3]
        stats = str(cardraw[2]) + "/" + str(cardraw[3])
        text = cardraw[4]
        cur.execute("SELECT colour FROM Cardcolour JOIN Colours ON Cardcolour.colour_id = Colours.id WHERE card_id = ?", (card_id, ))
        colour = cardstuff()
        cur.execute("SELECT tag FROM Cardtag JOIN tags ON Cardtag.tag_id = Tags.id WHERE card_id = ?", (card_id, ))
        tag = cardstuff()
        cur.execute("SELECT pack FROM Cardpack JOIN packs ON Cardpack.pack_id = Packs.id WHERE card_id = ?", (card_id, ))
        pack = cardstuff()
    
        subrun = 1
        while subrun == 1:
            print("")
            print(card)
            print("Colour: ", colour)
            print("Cost: ", cost)
            print("Stats: ", stats)
            print("")
            print(text)
            print("Tag: ", tag)
            print("Pack: ", pack)
            print("")
    
            while True:
                print('Type "edit trait" to edit that trait.')
                print('Type "list traits" to get a list of editable traits.')
                print('Type "delete" to delete this card.')
                print('Type "relist" to relist card details.')
                print('Type "back" to stop looking at this card.')

                subentry = input()
            
                if subentry.startswith("edit name"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current name:", card)
                        print("Please enter updated card name.")
                        print('Type "cancel" to cancel editing.')
                        executionlist = input()                 
                        if executionlist == "cancel":
                            editrun = 0
                            print("Edit canceled.")
                            break
                        cur.execute("UPDATE Cards SET card = ? WHERE id = ?", (executionlist, card_id))
                        conn.commit()
                        print("Done.")
                        editrun = 0
                        subentry = "relist"
                        break

                if subentry.startswith("edit colour"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current colours:", colour)
                        print('Type "add" or "delete" followed by a list of traits/id separated by "," (commas).')
                        print('Type "cancel" to cancel editing.')
                        request = input()
                        if request.startswith("add "):
                            processraw = request.lstrip("add ")
                            processlist = cleanup(processraw, ",", "low")
                            executionlist = []
                            while True:
                                for x in processlist:
                                    altx = "%" + x + "%"
                                    cur.execute("SELECT id, colour FROM Colours WHERE id = ? OR colour LIKE ?", (x, altx))
                                    y = cur.fetchone()
                                    executionlist.append(y[0])
                                    print(y)
                                print("Are these the traits you want to add? yes/no")
                                failsafe = input()
                                if failsafe == "yes":
                                    for x in executionlist:
                                        cur.execute("INSERT OR IGNORE INTO Cardcolour (card_id, colour_id) VALUES (? , ?)", (card_id, x))
                                    conn.commit()
                                    print("Done.")
                                    editrun = 0
                                    subentry = "relist"
                                    break
                                if failsafe == "no":
                                    print("Edit canceled.")
                                    editrun = 0
                                    break
                        if request.startswith("delete"):
                            processraw = request.lstrip("delete ")
                            processlist = cleanup(processraw, ",", "low")
                            executionlist = []
                            while True:
                                for x in processlist:
                                    altx = "%" + x + "%"
                                    cur.execute("SELECT colour_id, colour FROM Cardcolour JOIN Colours ON Cardcolour.colour_id = Colours.id WHERE id = ? OR colour LIKE ? AND card_id = ? ", (x, altx, card_id))
                                    y = cur.fetchone()
                                    executionlist.append(y[0])
                                    print(y)
                                print("Are these the traits you want to delete? yes/no")
                                failsafe = input()
                                if failsafe == "yes":
                                    for x in executionlist:
                                        cur.execute("DELETE FROM Cardcolour WHERE card_id = ? AND colour_id = ?", (card_id, x))
                                    conn.commit()
                                    print("Done.")
                                    editrun = 0
                                    subentry = "relist"
                                    break
                                if failsafe == "no":
                                    print("Edit canceled.")
                                    editrun = 0
                                    break
                    
                        if request == "cancel":
                            editrun = 0
                            print("Edit canceled.")
                            break
                    
                if subentry.startswith("edit cost"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current cost:", cost)
                        print("Please enter new cost.")
                        print('Type "cancel" to cancel editing.')
                        while True:
                            request = input()                 
                            if request == "cancel":
                                editrun = 0
                                print("Edit canceled.")
                                break
                            try: 
                                executionlist = int(request)
                                break
                            except:
                                print("Please enter a number. (1, 2, 3 etc.)")
                        if editrun == 0: break
                        cur.execute("UPDATE Cards SET cost = ? WHERE id = ?", (executionlist, card_id))
                        conn.commit()
                        print("Done.")
                        editrun = 0
                        subentry = "relist"
                        break
           
                if subentry.startswith("edit power"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current power:", power)
                        print("Please enter new power.")
                        print('Type "cancel" to cancel editing.')
                        while True:
                            request = input()                 
                            if request == "cancel":
                                editrun = 0
                                print("Edit canceled.")
                                break
                            try: 
                                executionlist = int(request)
                                break
                            except:
                                print("Please enter a number. (1, 2, 3 etc.)")
                        if editrun == 0: break
                        cur.execute("UPDATE Cards SET power = ? WHERE id = ?", (executionlist, card_id))
                        conn.commit()
                        print("Done.")
                        editrun = 0
                        subentry = "relist"
                        break
                    
                if subentry.startswith("edit toughness"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current toughness:", toughness)
                        print("Please enter new toughness.")
                        print('Type "cancel" to cancel editing.')
                        while True:
                            request = input()                 
                            if request == "cancel":
                                editrun = 0
                                print("Edit canceled.")
                                break
                            try: 
                                executionlist = int(request)
                                break
                            except:
                                print("Please enter a number. (1, 2, 3 etc.)")
                        if editrun == 0: break
                        cur.execute("UPDATE Cards SET toughness = ? WHERE id = ?", (executionlist, card_id))
                        conn.commit()
                        print("Done.")
                        editrun = 0
                        subentry = "relist"
                        break
                    
                if subentry.startswith("edit text"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current text:", text)
                        print("Please enter new text.")
                        print('Type "cancel" to cancel editing.')
                        executionlist = input()                 
                        if executionlist == "cancel":
                            editrun = 0
                            print("Edit canceled.")
                            break
                        cur.execute("UPDATE Cards SET text = ? WHERE id = ?", (executionlist, card_id))
                        conn.commit()
                        print("Done.")
                        editrun = 0
                        subentry = "relist"
                        break
                    
                if subentry.startswith("edit tag") or subentry.startswith("edit tags"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current tags:", tag)
                        print('Type "add" or "delete" followed by a list of traits/id separated by "," (commas).')
                        print('Type "cancel" to cancel editing.')
                        request = input()
                        if request.startswith("add "):
                            processraw = request.lstrip("add ")
                            processlist = cleanup(processraw, ",", "low")
                            executionlist = []
                            while True:
                                for x in processlist:
                                    altx = "%" + x + "%"
                                    cur.execute("SELECT id, tag FROM Tags WHERE id = ? OR tag LIKE ?", (x, altx))
                                    y = cur.fetchone()
                                    executionlist.append(y[0])
                                    print(y)
                                print("Are these the traits you want to add? yes/no")
                                failsafe = input()
                                if failsafe == "yes":
                                    for x in executionlist:
                                        cur.execute("INSERT OR IGNORE INTO Cardtag (card_id, tag_id) VALUES (? , ?)", (card_id, x))
                                    conn.commit()
                                    print("Done.")
                                    editrun = 0
                                    subentry = "relist"
                                    break
                                if failsafe == "no":
                                    print("Edit canceled.")
                                    editrun = 0
                                    break
                        if request.startswith("delete"):
                            processraw = request.lstrip("delete ")
                            processlist = cleanup(processraw, ",", "low")
                            executionlist = []
                            while True:
                                for x in processlist:
                                    altx = "%" + x + "%"
                                    cur.execute("SELECT tag_id, tag FROM Cardtag JOIN Tags ON Cardtag.tag_id = Tags.id WHERE id = ? OR tag LIKE ? AND card_id = ? ", (x, altx, card_id))
                                    y = cur.fetchone()
                                    executionlist.append(y[0])
                                    print(y)
                                print("Are these the traits you want to delete? yes/no")
                                failsafe = input()
                                if failsafe == "yes":
                                    for x in executionlist:
                                        cur.execute("DELETE FROM Cardtag WHERE card_id = ? AND tag_id = ?", (card_id, x))
                                    conn.commit()
                                    print("Done.")
                                    editrun = 0
                                    subentry = "relist"
                                    break
                                if failsafe == "no":
                                    print("Edit canceled.")
                                    editrun = 0
                                    break
                    
                        if request == "cancel":
                            editrun = 0
                            print("Edit canceled.")
                            break
                        
                if subentry.startswith("edit pack") or subentry.startswith("edit packs"):
                    print("")
                    editrun = 1
                    while editrun == 1:
                        print("Current packs:", pack)
                        print('Type "add" or "delete" followed by a list of traits/id separated by "," (commas).')
                        print('Type "cancel" to cancel editing.')
                        request = input()
                        if request.startswith("add "):
                            processraw = request.lstrip("add ")
                            processlist = cleanup(processraw, ",", "low")
                            executionlist = []
                            while True:
                                for x in processlist:
                                    altx = "%" + x + "%"
                                    cur.execute("SELECT id, pack FROM Packs WHERE id = ? OR pack LIKE ?", (x, altx))
                                    y = cur.fetchone()
                                    executionlist.append(y[0])
                                    print(y)
                                print("Are these the traits you want to add? yes/no")
                                failsafe = input()
                                if failsafe == "yes":
                                    for x in executionlist:
                                        cur.execute("INSERT OR IGNORE INTO Cardpack (card_id, pack_id) VALUES (? , ?)", (card_id, x))
                                    conn.commit()
                                    print("Done.")
                                    editrun = 0
                                    subentry = "relist"
                                    break
                                if failsafe == "no":
                                    print("Edit canceled.")
                                    editrun = 0
                                    break
                        if request.startswith("delete"):
                            processraw = request.lstrip("delete ")
                            processlist = cleanup(processraw, ",", "low")
                            executionlist = []
                            while True:
                                for x in processlist:
                                    altx = "%" + x + "%"
                                    cur.execute("SELECT pack_id, pack FROM Cardpack JOIN Packs ON Cardpack.pack_id = Packs.id WHERE id = ? OR pack LIKE ? AND card_id = ? ", (x, altx, card_id))
                                    y = cur.fetchone()
                                    executionlist.append(y[0])
                                    print(y)
                                print("Are these the traits you want to delete? yes/no")
                                failsafe = input()
                                if failsafe == "yes":
                                    for x in executionlist:
                                        cur.execute("DELETE FROM Cardpack WHERE card_id = ? AND pack_id = ?", (card_id, x))
                                    conn.commit()
                                    print("Done.")
                                    editrun = 0
                                    subentry = "relist"
                                    break
                                if failsafe == "no":
                                    print("Edit canceled.")
                                    editrun = 0
                                    break
                        if request == "cancel":
                            editrun = 0
                            print("Edit canceled.")
                            break
                            
                if subentry == "list traits": print('''
name, colour, cost, power, toughness, text, tag, pack
''')
                if subentry == "delete": 
                    subrun = 0
                    run = 0
                    delprocess(card_id)
                    print("")
                    break
                
                if subentry == "relist":
                    print("")
                    subrun = 0
                    break
                
                if subentry == "back" :
                    subrun = 0
                    run = 0
                    break
    return
 
#starts card deletion process, accesible from multiple places
def delprocess(card_id):
    while True:
        print("Are you sure you want to delete this card? yes/no")
        failsafe = input()
        if failsafe == "no":
            out = 1
            break
        if failsafe =="yes":
            out = 0
            break
    if out == 1: return
    cur.execute("SELECT pack_id FROM Cardpack WHERE card_id = ?", (card_id,))
    try: test_id = cur.fetchone()[0]
    except: test_id = None
    if test_id != None:
        cur.execute("DELETE FROM Cardpack WHERE card_id = ?", (card_id,))
        cur.execute("SELECT pack_id FROM Cardpack WHERE pack_id = ?", (test_id,))
        try: test = cur.fetchone()[0]
        except:
            cur.execute("DELETE FROM Packs WHERE id = ?", (test_id,))
            
    cur.execute("SELECT tag_id FROM Cardtag WHERE card_id = ?", (card_id,))
    try: test_id = cur.fetchone()[0]
    except: test_id = None
    if test_id != None:
        cur.execute("DELETE FROM Cardtag WHERE card_id = ?", (card_id,))
        cur.execute("SELECT tag_id FROM Cardtag WHERE tag_id = ?", (test_id,))
        try: test = cur.fetchone()[0]
        except:
            cur.execute("DELETE FROM Tags WHERE id = ?", (test_id,))
  
    cur.execute("SELECT colour_id FROM Cardcolour WHERE card_id = ?", (card_id,))
    try: test_id = cur.fetchone()[0]
    except: test_id = None
    if test_id != None:
        cur.execute("DELETE FROM Cardcolour WHERE card_id = ?", (card_id,))
        cur.execute("SELECT colour_id FROM Cardcolour WHERE colour_id = ?", (test_id,))
        try: test = cur.fetchone()[0]
        except:
            cur.execute("DELETE FROM Colours WHERE id = ?", (test_id,))
    cur.execute("DELETE FROM Cards WHERE id = ?", (card_id, ))
    conn.commit()
    print("Card deleted.")
    
#mass add tags, accesible from multiple places
def massaddtag(newtag, new_id):
    print("Enter id of cards, separated by commas (,).")
    print('Enter "cancel" to cancel operation.')
    cardqraw = input()
    if cardqraw == "cancel": return
    cardq = cleanup(cardqraw, ",", None)
    print("(id, card)")
    for x in cardq:
        cur.execute("SELECT id, card FROM Cards WHERE id = ?", (x, ))
        print(cur.fetchone())
    while True:
        print("Are these the cards you want to add tag", '"' + newtag + '"', "to? yes/no")
        failsafe = input()
        if failsafe == "no":
            out = 1
            break
        elif failsafe == "yes":
            out = 0
            break
    if out == 1:
        print("Action terminated. The new tag is still registered in the database.")
        return
    for x in cardq:
        cur.execute("INSERT OR IGNORE INTO Cardtag (card_id, tag_id) VALUES (?, ?)", (x, new_id))
    conn.commit()
    print("Done.")


#====MAIN CODE===#
#db entry===========
#initiate new db
def newlib():
    failsafe = input('''Do you want to make a new library?
The old library, if it exists, WILL be deleted. 
Make sure you backup if you want to keep your cards!
Enter yes to proceed.
Enter no to stop grabbing for the torch.
''')
    
    if failsafe == "yes":
        cur.executescript('''
        DROP TABLE IF EXISTS Tags;
        DROP TABLE IF EXISTS Colours;
        DROP TABLE IF EXISTS Packs;
        DROP TABLE IF EXISTS Cards;
        DROP TABLE IF EXISTS Cardcolour;
        DROP TABLE IF EXISTS Cardtag;
        DROP TABLE IF EXISTS Cardpack;

        CREATE TABLE Tags (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            tag   TEXT UNIQUE
        );
    
        CREATE TABLE Colours (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            colour  TEXT UNIQUE
        );
  
        CREATE TABLE Packs (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            pack   TEXT UNIQUE
        );
        
        CREATE TABLE Cards (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            card   TEXT UNIQUE,
            cost   INTEGER,
            power  INTEGER,
            toughness   INTEGER,
            text   TEXT
        );
    
        CREATE TABLE Cardcolour (
            card_id     INTEGER,
            colour_id   INTEGER,
            PRIMARY KEY (card_id, colour_id)
        );
        
        CREATE TABLE Cardtag (
            card_id   INTEGER,
            tag_id   INTEGER,
            PRIMARY KEY (card_id, tag_id)
        );
        
        CREATE TABLE Cardpack (
            card_id   INTEGER,
            pack_id   INTEGER,
            PRIMARY KEY (card_id, pack_id)
        )
        ''')
        print('New library created.')
        
    elif failsafe == "no":
        print('Action terminated.')
    else:
        print('Instructions unclear, just give me the torch.')
        print('Action terminated.')

#new card entry
def addcard():
    run = 1
    while run == 1:
        print('To stop entering new card type "cancel" in any of the prompts.')
        
        card = input("Card name:")
        if card == "cancel": 
            print("Action terminated.")
            break
        
        print('If there are multiple colours, please separate them with commas ","')
        print('''If it's colourless, type "colourless".''')
        colourraw = input('Colour: ')
        if colourraw == "cancel":  
            print("Action terminated.")
            break
        
        print('If there is no cost, leave it blank.')
        costraw = input('Cost: ')
        if costraw == "cancel":  
            print("Action terminated.")
            break
#        (alt code)
#        cost = input('Cost: ')
#        if cost == "cancel":
#            print("Action terminated.")
#            break
        
        print('If the card comes from multiple packs, please separate them with commas (,)')                   
        packraw = input("Pack: ")
        if packraw == "cancel":
            print("Action terminated.")
            break
        
        print('If there are multiple tags, please separate them with commas (,)')
        tagraw = input('Tags: ')
        if tagraw == "cancel":  
            print("Action terminated.")
            break
            
        print("If there's no text, leave it blank.")
        text = input("Text: ")
        if text == "cancel":
            print("Action terminated.")
            break
          
        print('Enter as shown on card, (power/toughness). If there is none, leave it blank.')
        statraw = input("Stats: ")
        if statraw == "cancel":
            print("Action terminated.")
            break

        colour = cleanup(colourraw, ",", "low")
        tag = cleanup(tagraw, ",", "low")
        pack = cleanup(packraw, ",", "hi")
        while True :
            if len(costraw) == 0:
                cost = None
                break
            try:
                cost = int(costraw)
                break
            except:
                print("Please enter cost in arabic numerals, ex: 1, 2, 3, 4...")
                costraw = input('Cost: ')
        while True :
            if len(statraw) == 0:
                power = None
                toughness = None
                break
            stat = statraw.split("/")
            try:
                powerraw = stat[0]
                toughnessraw = stat[1]
                if powerraw == "*": power = powerraw
                else: power = int(powerraw)
                if toughnessraw == "*": toughness = toughnessraw
                else:toughness = int(toughnessraw)
                break
            except:
                print("Please enter stats exactly as on card, with the format (power/toughness)")
                statraw = input('Stats: ')
                if statraw == "cancel":
                    run = 0
            
        if run == 0: return
       
        print("Transcribing card...")
        cur.execute('''INSERT OR REPLACE INTO Cards (card, cost, power, toughness, text) 
            VALUES ( ?, ?, ?, ?, ? )''', ( card, cost, power, toughness, text ) )
        cur.execute('SELECT id FROM Cards WHERE card = ? ', (card, ))
        card_id = cur.fetchone()[0]
        
        for x in tag:
            cur.execute('''INSERT OR IGNORE INTO Tags (tag) 
                VALUES ( ? )''', ( x, ) )
            cur.execute('SELECT id FROM Tags WHERE tag = ? ', (x, ))
            tag_id = cur.fetchone()[0]
            cur.execute('''INSERT OR REPLACE INTO Cardtag (card_id, tag_id) 
            VALUES ( ?, ? )''', ( card_id, tag_id ))
    
        for x in colour :
            cur.execute('''INSERT OR IGNORE INTO Colours (colour) 
                VALUES ( ? )''', ( x, ) )
            cur.execute('SELECT id FROM Colours WHERE colour = ? ', (x, ))
            colour_id = cur.fetchone()[0]
            cur.execute('''INSERT OR REPLACE INTO Cardcolour (card_id, colour_id) 
                VALUES ( ?, ? )''', ( card_id, colour_id ) )
                
        for x in pack :
            cur.execute('''INSERT OR IGNORE INTO Packs (pack) 
                VALUES ( ? )''', ( x, ) )
            cur.execute('SELECT id FROM Packs WHERE pack = ? ', (x, ))
            pack_id = cur.fetchone()[0]
            cur.execute('''INSERT OR REPLACE INTO Cardpack (card_id, pack_id) 
                VALUES ( ?, ? )''', ( card_id, pack_id ) )
                
        conn.commit()
        print("Transcription completed.")
        print("Do you want to add another card? yes/no")
        cont = input()
        while True:
            if cont == "yes":
                break
            elif cont == "no":
                run = 0
                break
            else: print("Do you want to add another card? yes/no")
        print("")

#delete card entry
def deletecard():
    print("Enter card name or card id. Please ensure correct spelling.")
    print('Enter "cancel" to exit out of this operation.')
    request = input()
    if request == "cancel": return
    
    altrequest = "%" + request + "%"
    cur.execute("SELECT id FROM Cards WHERE id = ? OR card LIKE ?", (request, altrequest))
    try: card_id = cur.fetchone()[0]
    except:
        print("No card found.")
        return
    cur.execute("SELECT card, cost, power, toughness, text FROM Cards where id = ?", (card_id, ))
    cardraw = cur.fetchone()
    card = cardraw[0]
    cost = cardraw[1]
    power = cardraw[2]
    toughness = cardraw[3]
    stats = str(cardraw[2]) + "/" + str(cardraw[3])
    text = cardraw[4]
    cur.execute("SELECT colour FROM Cardcolour JOIN Colours ON Cardcolour.colour_id = Colours.id WHERE card_id = ?", (card_id, ))
    colour = cardstuff()
    cur.execute("SELECT tag FROM Cardtag JOIN tags ON Cardtag.tag_id = Tags.id WHERE card_id = ?", (card_id, ))
    tag = cardstuff()
    cur.execute("SELECT pack FROM Cardpack JOIN packs ON Cardpack.pack_id = Packs.id WHERE card_id = ?", (card_id, ))
    pack = cardstuff()
    print("")
    print(card)
    print("Colour: ", colour)
    print("Cost: ", cost)
    print("Stats: ", stats)
    print("")
    print(text)
    print("Tag: ", tag)
    print("Pack: ", pack)
    print("")
    delprocess()

#new tag entry
def newtag():
    print("Enter name for new tag.")
    print('Enter "cancel" to stop operation.')
    raw = input()
    if raw == "cancel": return
    newtag = raw.lower()
    try: cur.execute("INSERT INTO Tags (tag) VALUES (?)", (newtag, ))
    except: print("The tag already exists.")
    cur.execute("SELECT id FROM Tags WHERE tag = ?", (newtag, ))
    conn.commit()
    new_id = cur.fetchone()[0]
    print("The id for", newtag, "is", str(new_id) +".")
    while True:
        print("Do you want to attach the tag to new cards? yes/no")
        tagmore = input()
        if tagmore == "no":
            out = 1
            break
        elif tagmore == "yes":
            out = 0
            break
    if out == 1: return
    massaddtag(newtag, new_id)

#db checkup
def checkup():
    print("Scanning for missing traits...")
    cur.execute("SELECT id, card FROM Cards LEFT JOIN Cardpack ON Cardpack.card_id = Cards.id WHERE Cardpack.card_id IS NULL")
    no_pack = cur.fetchall()
    cur.execute("SELECT id, card FROM Cards LEFT JOIN Cardcolour ON Cardcolour.card_id = Cards.id WHERE Cardcolour.card_id IS NULL")
    no_colour = cur.fetchall()
    cur.execute("SELECT id, card FROM Cards LEFT JOIN Cardtag ON Cardtag.card_id = Cards.id WHERE Cardtag.card_id IS NULL")
    no_tag = cur.fetchall()
    
    try:
        testcode = no_pack[0]
        testcode = no_colour[0]
        testcode = no_tag[0]
        print("There are", str(len(no_pack) + len(no_colour) + len(no_tag)), "cards with missing traits.")
        print("")
    except: print("No missing traits found.")
       
    try: 
        testcode = no_pack[0]
        print("Missing packs" )
        print("(id, card)")
        for y in no_pack: print(y)
        print("")        
    except: pass              

    try: 
        testcode = no_colour[0]
        print("Missing colours")
        print("(id, card)")
        for y in no_colour: print(y)
        print("")    
    except: pass           
              
    try: 
        testcode = no_tag[0]
        print("Missing tags")
        print("(id, card)")
        for y in no_tag: print(y)
        print("")
    except: pass
    
    try:
        testcode = no_pack[0]
        testcode = no_colour[0]
        testcode = no_tag[0]
        print("Please update the missing traits.")
        print("")
    except: pass
        

    
    
    print("Scanning for orphaned traits...")
    cur.execute("SELECT id, pack FROM Packs LEFT JOIN Cardpack ON Cardpack.pack_id = Packs.id WHERE Cardpack.pack_id IS NULL")
    no_pack = cur.fetchall()
    cur.execute("SELECT id, colour FROM Colours LEFT JOIN Cardcolour ON Cardcolour.colour_id = Colours.id WHERE Cardcolour.colour_id IS NULL")
    no_colour = cur.fetchall()
    cur.execute("SELECT id, tag FROM Tags LEFT JOIN Cardtag ON Cardtag.tag_id = Tags.id WHERE Cardtag.tag_id IS NULL")
    no_tag = cur.fetchall()
    
    try:
        testcode = no_pack[0]
        testcode = no_colour[0]
        testcode = no_tag[0]
        print("There are", str(len(no_pack) + len(no_colour) + len(no_tag)), " orphaned traits.")
        print("")
    except: print("No orphaned traits found.")

        
    try: 
        testcode = no_pack[0]
        print("Orphaned packs" )
        print("(id, card)")
        for y in no_pack: print(y)
        print("")
        print("Enter the id of packs you would like to delete, separated by comma.")
        print("Otherwise, leave it blank.")
        requestraw = input()
        request = cleanup(requestraw, ",", "")
        for z in request: cur.execute("DELETE FROM Packs WHERE id = ?", (z,))
        conn.commit()
        print("Done!")
        print("")
    except: pass
        

    try: 
        testcode = no_colour[0]
        print("Orphaned colours" )
        print("(id, card)")
        for y in no_colour: print(y)
        print("")
        print("Enter the id of colours you would like to delete, separated by comma.")
        print("Otherwise, leave it blank.")
        requestraw = input()
        request = cleanup(requestraw, ",", None)
        for z in request: cur.execute("DELETE FROM Colours WHERE id = ?", (z,))
        conn.commit()
        print("Done!")
        print("")
    except: pass
        

    try: 
        testcode = no_tag[0]
        print("Orphaned tags" )
        print("(id, card)")
        for y in no_tag: print(y)
        print("")
        print("Enter the id of tags you would like to delete, separated by comma.")
        print("Otherwise, leave it blank.")
        requestraw = input()
        request = cleanup(requestraw, ",", "")
        for z in request: cur.execute("DELETE FROM Tags WHERE id = ?", (z,))
        conn.commit()
        print("Done!")
        print("")
    except: pass


#list================
#list cards
def listcards():
    run = 1
    offsetnum = 0
    cur.execute('''SELECT COUNT() from Cards''')
    limit = cur.fetchone()[0]
    while run == 1:
        cur.execute('''SELECT id, card FROM Cards ORDER BY card ASC LIMIT 10 OFFSET ?''', (offsetnum, ))
        output = cur.fetchall()
        print("Number of cards in library:", limit)
        print("(id, name)")
        for x in output:
            print(x)
 
        while True: 
            print("")
            print("You're currently at page", int(offsetnum / 10) + 1)
            if offsetnum > 0: print('Type "prev" to look at previous 10 entries.')
            if offsetnum + 10 < limit: print('Type "next" to look at next 10 entries.')
            print('''Type "view" followed by card id to view the card's information.''')
            print('Type "relist" to review to last viewed cardlist page.')
            print('Type "cancel" to stop looking at the cardlist.')
            
            entry = input()
            
            if offsetnum > 0 and entry == "prev":
                offsetnum = offsetnum - 10
                print("")
                break
            
            if offsetnum + 10 < limit and entry == "next":
                offsetnum = offsetnum + 10
                print("")
                break
            
            if entry.startswith("view"):
                raw = entry.split()
                try: card_id = raw[1]
                except:
                    print("No id inputted")
                    entry = "relist"
                    print("")
                    break
                viewcard(card_id)
                entry = "relist"
            
            if entry == "relist":
                print("")
                break
            
            if entry == "cancel":
                run = 0
                break


#list packs
def listpacks():
    run = 1
    offsetnum = 0
    cur.execute('''SELECT COUNT() from Packs''')
    limit = cur.fetchone()[0]
    while run == 1:
        cur.execute('''SELECT id, pack FROM Packs ORDER BY pack ASC LIMIT 10 OFFSET ?''', (offsetnum, ))
        output = cur.fetchall()
        print("Number of packs in library:", limit)
        print("(id, name)")
        for x in output:
            print(x)
        
        while True: 
            print("")
            print("You're currently at page", int(offsetnum / 10) + 1)
            if offsetnum > 0: print('Type "prev" to look at previous 10 entries.')
            if offsetnum + 10 < limit: print('Type "next" to look at next 10 entries.')
            print('Type "view" followed by pack id to list all cards that are from this pack.')
            print('Type "relist" to review to last viewed packlist page.')
            print('Type "cancel" to stop looking at the packlist.')
            
            entry = input()
            
            if offsetnum > 0 and entry == "prev":
                offsetnum = offsetnum - 10
                print("")
                break
            
            if offsetnum + 10 < limit and entry == "next":
                offsetnum = offsetnum + 10
                print("")
                break
            
            if entry.startswith("view"):
                raw = entry.split()
                try: listid = raw[1]
                except:
                    print("No id inputted")
                    entry = "relist"
                    print("")
                    break
                
                print("")  
                cur.execute("SELECT pack FROM Packs where id = ?", (listid, ))
                packraw = cur.fetchone()
                pack = packraw[0]
                print("Listing cards from pack", pack + ".")
                cur.execute("SELECT COUNT() from Cardpack WHERE pack_id = ?", (listid, ))
                sublimit = cur.fetchone()[0]
                print("Found", sublimit, "of cards from", pack + ".")
                subrun = 1
                suboffset = 0
                while subrun == 1:
                    cur.execute('''SELECT card_id, card FROM Cardpack JOIN Cards ON Cards.id = Cardpack.card_id WHERE pack_id = ? ORDER BY card ASC LIMIT 10 OFFSET ?''', (listid, suboffset))
                    output = cur.fetchall()
                    print("(id, card name)")
                    for x in output:
                        print(x)

                    while True:
                        print("")        
                        print("You're currently at page", int(suboffset / 10) + 1)
                        if suboffset > 0: print('Type "prev" to look at previous 10 entries.')
                        if suboffset + 10 < sublimit: print('Type "next" to look at next 10 entries.')
                        print('''Type "view" followed by card id to look at the card's details.''')
                        print('Type "relist" to review to last viewed sublist page.')
                        print('Type "back" to stop looking at this sublist.')
        
                        subentry = input()
         
                        if suboffset > 0 and subentry == "prev":
                            suboffset = suboffset - 10
                            print("")
                            break
         
                        if suboffset + 10 < sublimit and subentry == "next":
                            suboffset = suboffset + 10
                            print("")
                            break
                            
                        if subentry.startswith("view"):
                            raw = subentry.split()
                            try: card_id = raw[1]
                            except:
                                print("No id inputted")
                                entry = "relist"
                                print("")
                                break
                            viewcard(card_id)
                            subentry = "relist"
                            
                        if subentry == "relist":
                            print("")
                            break
         
                        if subentry == "back":
                            entry = "relist"
                            subrun = 0
                            break
                
            print("")
            
            if entry == "relist":
                print("")
                break
            
            if entry == "cancel":
                run = 0
                break

#list colours
def listcolours():
    run = 1
    offsetnum = 0
    cur.execute('''SELECT COUNT() from Colours''')
    limit = cur.fetchone()[0]
    while run == 1:
        cur.execute('''SELECT id, colour FROM Colours ORDER BY colour ASC LIMIT 10 OFFSET ?''', (offsetnum, ))
        output = cur.fetchall()
        print("Number of colours in library:", limit)
        print("(id, name)")
        for x in output:
            print(x)
        
        while True: 
            print("")
            print("You're currently at page", int(offsetnum / 10) + 1)
            if offsetnum > 0: print('Type "prev" to look at previous 10 entries.')
            if offsetnum + 10 < limit: print('Type "next" to look at next 10 entries.')
            print('''Type "view" followed by colour id to list all cards with that colour.''')
            print('Type "relist" to review to last viewed colourlist page.')
            print('Type "cancel" to stop looking at the colourlist.')
            
            entry = input()
            
            if offsetnum > 0 and entry == "prev":
                offsetnum = offsetnum - 10
                print("")
                break
            
            if offsetnum + 10 < limit and entry == "next":
                offsetnum = offsetnum + 10
                print("")
                break
            
            if entry.startswith("view"):
                raw = entry.split()
                try: listid = raw[1]
                except:
                    print("No id inputted")
                    entry = "relist"
                    print("")
                    break
                
                print("")                
                cur.execute("SELECT colour FROM Colours where id = ?", (listid, ))
                listraw = cur.fetchone()
                listing = listraw[0]
                print("Listing cards with colour", listing + ".")
                cur.execute("SELECT COUNT() from Cardcolour WHERE colour_id = ?", (listid, ))
                sublimit = cur.fetchone()[0]
                print("Found", sublimit, listing, "cards.")
                subrun = 1
                suboffset = 0
                while subrun == 1:
                    cur.execute('''SELECT card_id, card FROM Cardcolour JOIN Cards ON Cards.id = Cardcolour.card_id WHERE colour_id = ? ORDER BY card ASC LIMIT 10 OFFSET ?''', (listid, suboffset))
                    output = cur.fetchall()
                    for x in output:
                        print(x)

                    while True:
                        print("")        
                        print("You're currently at page", int(suboffset / 10) + 1)
                        if suboffset > 0: print('Type "prev" to look at previous 10 entries.')
                        if suboffset + 10 < sublimit: print('Type "next" to look at next 10 entries.')
                        print('''Type "view" followed by card id to look at the card's details.''')
                        print('Type "relist" to review to last viewed sublist page.')
                        print('Type "back" to stop looking at this sublist.')
        
                        subentry = input()
         
                        if suboffset > 0 and subentry == "prev":
                            suboffset = suboffset - 10
                            print("")
                            break
         
                        if suboffset + 10 < sublimit and subentry == "next":
                            suboffset = suboffset + 10
                            print("")
                            break
                        
                        if subentry.startswith("view"):
                            raw = subentry.split()
                            try: card_id = raw[1]
                            except:
                                print("No id inputted")
                                entry = "relist"
                                print("")
                                break
                            viewcard(card_id)
                            subentry = "relist"
            
                        if subentry == "relist":
                            print("")
                            break
         
                        if subentry == "back":
                            entry = "relist"
                            subrun = 0
                            break
                
            print("")
            
            if entry == "relist":
                print("")
                break
            
            if entry == "cancel":
                run = 0
                break

#list tags
def listtags():
    run = 1
    offsetnum = 0
    cur.execute('''SELECT COUNT() from Tags''')
    limit = cur.fetchone()[0]
    while run == 1:
        cur.execute('''SELECT id, tag FROM Tags ORDER BY tag ASC LIMIT 10 OFFSET ?''', (offsetnum, ))
        output = cur.fetchall()
        print("Number of tags in library:", limit)
        print("(id, name)")
        for x in output:
            print(x)
        
        
        while True: 
            print("")
            print("You're currently at page", int(offsetnum / 10) + 1)
            if offsetnum > 0: print('Type "prev" to look at previous 10 entries.')
            if offsetnum + 10 < limit: print('Type "next" to look at next 10 entries.')
            print('''Type "view" followed by tag id to list all cards with that tag.''')
            print('Type "relist" to review to last viewed taglist page.')
            print('Type "cancel" to stop looking at the taglist.')
            
            entry = input()
            
            if offsetnum > 0 and entry == "prev":
                offsetnum = offsetnum - 10
                print("")
                break
            
            if offsetnum + 10 < limit and entry == "next":
                offsetnum = offsetnum + 10
                print("")
                break
            
            if entry.startswith("view"):
                raw = entry.split()
                try: listid = raw[1]
                except:
                    print("No id inputted")
                    entry = "relist"
                    print("")
                    break
                
                print("")                
                cur.execute("SELECT tag FROM Tags where id = ?", (listid, ))
                listraw = cur.fetchone()
                listing = listraw[0]
                print("Listing cards with tag", listing + ".")
                cur.execute("SELECT COUNT() from Cardtag WHERE tag_id = ?", (listid, ))
                sublimit = cur.fetchone()[0]
                print("Found", sublimit, listing, "cards.")
                subrun = 1
                suboffset = 0
                while subrun == 1:
                    cur.execute('''SELECT card_id, card FROM Cardtag JOIN Cards ON Cards.id = Cardtag.card_id WHERE tag_id = ? ORDER BY card ASC LIMIT 10 OFFSET ?''', (listid, suboffset))
                    output = cur.fetchall()
                    print("(id, card)")
                    for x in output:
                        print(x)

                    while True:
                        print("")        
                        print("You're currently at page", int(suboffset / 10) + 1)
                        if suboffset > 0: print('Type "prev" to look at previous 10 entries.')
                        if suboffset + 10 < sublimit: print('Type "next" to look at next 10 entries.')
                        print('''Type "view" followed by card id to look at the card's details.''')
                        print('Type "mass tag" to tag other cards with this tag.')
                        print('Type "delete tag" to delete this tag.')
                        print('Type "relist" to review to last viewed sublist page.')
                        print('Type "back" to stop looking at this sublist.')
        
                        subentry = input()
         
                        if suboffset > 0 and subentry == "prev":
                            suboffset = suboffset - 10
                            print("")
                            break
         
                        if suboffset + 10 < sublimit and subentry == "next":
                            suboffset = suboffset + 10
                            print("")
                            break
                        
                        if subentry.startswith("view"):
                            raw = subentry.split()
                            try: card_id = raw[1]
                            except:
                                print("No id inputted")
                                entry = "relist"
                                print("")
                                break
                            viewcard(card_id)
                            subentry = "relist"
                            
                        if subentry == "mass tag":
                            massaddtag(listing, listid)
                            subentry = "relist"
                            
                        if subentry == "delete tag":
                            while True:
                                print("All cards with the tag will be affected. Are you sure you want to do this? yes/no")
                                failsafe = input()
                                if failsafe == "no":
                                    out = 1
                                    break
                                elif failsafe == "yes":
                                    out = 0
                                    break
                            if out == 1: return
                            cur.execute("DELETE FROM Cardtag WHERE tag_id = ?", (listid, ))
                            cur.execute("DELETE FROM Tags WHERE id = ?", (listid, ))
                            conn.commit()
                            print("Done.")
                            entry = "relist"
                            subrun = 0
                            break
                        
                        if subentry == "relist":
                            print("")
                            break
         
                        if subentry == "back":
                            entry = "relist"
                            subrun = 0
                            break
                
            print("")
            
            if entry == "relist":
                print("")
                break
            
            if entry == "cancel":
                run = 0
                break
