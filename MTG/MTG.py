#program
import sqlite3
import command_list as m
conn = sqlite3.connect('library.sqlite')
cur = conn.cursor()

#backup
try:
    backupCon = sqlite3.connect('rollback.sqlite')
    with backupCon:
        conn.backup(backupCon, pages=3)
#    print("backup successful")
except sqlite3.Error as error:
    print("Error while taking backup: ", error)
finally:
    if(backupCon):
        backupCon.close()


print('''
Welcome to MTG library, your personal card organiser in terminal form.
For command list, type help.''')

while True:
    print('')
    command = input(">>")
    print('')

    if command == "exit":
        print("Library closed.")
        try: 
            cur.executescript('''
            DELETE FROM Cardpack WHERE pack_id IN (SELECT Cardpack.pack_id FROM Cardpack LEFT JOIN Packs ON Cardpack.pack_id = Packs.id WHERE Packs.id IS NULL);
            DELETE FROM Cardpack WHERE card_id IN (SELECT Cardpack.card_id FROM Cardpack LEFT JOIN Cards ON Cardpack.card_id = Cards.id WHERE Cards.id IS NULL);
            DELETE FROM Cardtag WHERE tag_id IN (SELECT Cardtag.tag_id FROM Cardtag LEFT JOIN Tags ON Cardtag.tag_id = Tags.id WHERE Tags.id IS NULL);
            DELETE FROM Cardtag WHERE card_id IN (SELECT Cardtag.card_id FROM Cardtag LEFT JOIN Cards ON Cardtag.card_id = Cards.id WHERE Cards.id IS NULL);
            DELETE FROM Cardcolour WHERE colour_id IN (SELECT Cardcolour.colour_id FROM Cardcolour LEFT JOIN Colours ON Cardcolour.colour_id = Colours.id WHERE Colours.id IS NULL);
            DELETE FROM Cardcolour WHERE card_id IN (SELECT Cardcolour.card_id FROM Cardcolour LEFT JOIN Cards ON Cardcolour.card_id = Cards.id WHERE Cards.id IS NULL)
        )
        ''')
        except: break
        break
    
    if command == "help":
        f = open("commands.txt")
        manual = f.read()
        print(manual)
        
    if command == "new library":
        m.newlib()
    
    if command == "add card" :
        m.addcard()
    
    if command == "list cards" :
        m.listcards()
    
    if command == "list packs" :
        m.listpacks()
    
    if command == "list colours" :
        m.listcolours()
    
    if command == "list tags" :
        m.listtags()
        
    if command == "add tag" :
        m.newtag()
        
    if command == "view card":
        print("Enter card name or card id. Please ensure correct spelling.")
        request = input()
        altrequest = "%" + request + "%"
        cur.execute("SELECT id FROM Cards WHERE id = ? OR card LIKE ?", (request, altrequest))
        try: 
            x = cur.fetchone()[0]
            m.viewcard(x)
        except:
            print("Card not found.")
    
    if command == "delete card":
        m.deletecard()
    
    if command =="checkup":
        m.checkup()
