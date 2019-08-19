# test file:
##########
#N
#Witch
#T
#ATTACK
#CURSE
#D
#REACTION
#TRASH
#EOF
#
##########
# final newline is necessary!

from random import randint, seed

class Card:
    types = ['ATTACK', 'REACTION', 'CURSE', 'TRASH', 'CARDS', 'BUYS', 'ACTIONS', 'DURATION']
    
    def __init__(self):
        self.name = ''
        self.traits = []
        self.deps = []

    def printMe(self):
        out = self.name + " - traits: "
        for trait in self.traits:
            out += trait + ", "
        out += 'dependancies: '
        for dep in self.deps:
            out += dep + ', '
        return out

owned = []
cardsActions = True
seed(1908)

mode = ''
first = True
infile = open('owned.dat', 'r')
# read = 'ifThisLineEndsUpAnywhereWeAreInBigTrouble'
read = infile.readline()[:-1]
while read != 'EOF':
    print('LOOP, (read) - ' + read)
    # catch header
    if len(read) == 1:
        print('header caught')
        mode = read
        print('   mode now ' + mode)
    elif mode == 'N':
        # name follows, init new card
        print('reading name')
        if not first:
            print("we've done it bois, we loaded a not first card")
            owned += [newCard]
        first = False
        newCard = Card()
        newCard.name = read
    elif mode == 'T':
        print('reading trait')
        newCard.traits += [read]
    elif mode == 'D':
        print('reading dependancy')
        newCard.deps += [read]
        
    read = infile.readline()[:-1]

owned += [newCard]

print('READ OVER - loaded: ' + str(owned))

infile.close()

menu = -1
while menu != '0':
    print('\n 0. Exit')
    print(' 1. Add Card')
    print(' 2. Generate Game')
    print(' 3. Edit Card')
    print(' 4. Delete Card')
    print(' 5. Settings\n')
    menu = input(' ')

    if menu == '1':
        newCard = Card()
        newCard.name = input('\nCard Name: ')
        
        print('\nAdding traits...')
        
        print(' 0. DONE')
        for i in range(len(Card.types)):
            print(' ' + str(i+1) + '. ' + Card.types[i])
        
        choice = input('New Trait: ')
        while choice != '0':
            newTrait = Card.types[int(choice) - 1]
            newCard.traits += [newTrait]
            choice = input('New Trait: ')
        
        print('\nAdding dependancies...\n')
        
        print(' 0. DONE')
        for i in range(len(Card.types)):
            print(' ' + str(i+1) + '. ' + Card.types[i])
            
        choice = input('New Dependancy: ')
        while choice != '0':
            newDep = Card.types[int(choice) - 1]
            newCard.deps += [newDep]
            choice = input('New Dependancy: ')

        owned += [newCard]

    elif menu == '2':
        pool = []
        deck = []
        met = [False] * len(Card.types)
        req = [False] * len(Card.types)
        # pick first card out of all owned
        newCard = owned[randint(0,len(owned) - 1)]
        print(' --<dbg>-- first draw: ' + newCard.printMe())
        deck += [newCard]
        # update met and required dependancies
        for trait in newCard.traits:
            met[Card.types.index(trait)] = True
        for dep in newCard.deps:
            req[Card.types.index(dep)] = True
        ## print(' --<dbg>-- required: ' + str(req))
        ## print(' --<dbg>-- met: ' + str(met))
        # loop to pick 9 more cards
        while len(deck) < 10:
            print(' --<dbg>-- loop start - deck size: ' + str(len(deck)))
            # refresh unmet dependancies
            unmet = []
            for i in range(len(Card.types)):
                if req[i] and not met[i]:
                    unmet += [Card.types[i]]
            print(' --<dbg>-- unmet deps: ' + str(unmet))
            # fill pool to meet dependancies
            pool = []
            for card in owned:
                for trait in card.traits:
                    ## print(' --<dbg>-- -- checking ' + card.name ' 
                    if trait in unmet:
                        pool += [card]
                        print(' --<dbg>-- found unmet trait in deck')
                        # break to prevent duplicate addition _
                        # for multiple matching traits
                        break
            # DEBUG print pool
            print(' --<dbg>-- pool (pre-fix): ', end = '')
            for card in pool:
                print(card.name + ', ', end = '')
            print('')
            # if pool is empty all dependancies are met (or impossible deck?)
            if len(pool) == 0:
                print(' --<dbg>-- pool empty')
                for card in owned:
                    pool += [card]
            # draw new card from pool
            newCard = pool[randint(0,len(pool) - 1)]
            print(' --<dbg>-- draw: ' + newCard.printMe())
            if newCard not in deck:
                deck += [newCard]
                print(' --<dbg>-- not in deck, added')
                # update met and required dependancies
                for trait in newCard.traits:
                    met[Card.types.index(trait)] = True
                for dep in newCard.deps:
                    req[Card.types.index(dep)] = True
                # custom dependancies
                if cardsActions and met[Card.types.index('CARDS')]:
                    req[Card.types.index('ACTIONS')] = True
                ## print(' --<dbg>-- required: ' + str(req))
                ## print(' --<dbg>-- met: ' + str(met))

        # print deck
        for card in deck:
            print(card.name)
        
    elif menu == '3':
        print('lol u want settings')
    elif menu == '4':
        print('that would be a nice feature to have...')
    elif menu == '5':
        choice = -1
        while choice != '0':
            print('\n0. Back')
            print('1. +Cards -> +Actions: ' + ('ON' if cardsActions else 'OFF'))
            print()
            choice = input('')
            if choice == '1':
                cardsActions = not cardsActions
                print('+Cards ' + ('aquired ' if cardsActions else 'lost ') + '+Actions dependancy')
            

outfile = open('owned.dat', 'w')

for card in owned:
    outfile.write('N\n')
    outfile.write(card.name + '\n')
    outfile.write('T\n')
    for trait in card.traits:
        outfile.write(trait + '\n')
    outfile.write('D\n')
    for dep in card.deps:
        outfile.write(dep + '\n')
outfile.write('EOF\n')

outfile.close()
