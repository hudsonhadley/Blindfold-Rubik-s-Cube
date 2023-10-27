# Please never delete this. This took like half an hour to copy from the spreadsheet
# FIGURE OUT YOUR PIP MY GUY SO YOU CAN IMPORT SPREADSHEETS AND BE LAZY

# A function which takes two letters and returns the corresponding word from the spreadsheet
def get_word(a, b):
    # Translate the letters into numbers ---> ord("A") == 65
    # We want this to equal 0 so we subtract 65
    num = [int(ord(a)) - 65, int(ord(b) - 65)]

    # Get the word in the spreadsheet
    word = spread_sheet[num[0]][num[1]]

    return word

spread_sheet = ["N/A, Abe (Lincoln), Acura, Ad/Advertisement, American Eagle, Air Force, Alligator, Adolf Hitler, Allen Iverson, AJ (Mathwin), AK-47, Alien, Morning, Anna, Joseph Ayo, Airplane, Antique, Arrow, Ass/Donkey, AT-AT, Gold, Avatar, Cute, Axe",
			   "Ben Affleck, N/A, Bicycle, Bed, Bee, Bobba Fett, Bagel, Behemoth (Battlefield 1), Bilbo, BJ's, Black Knight, Bull, Bob Marley, Ben, Barack Obama, Backpack, Barbeque/BBQ, Bear, Boss, Bat, Boo (Monster's Inc), Beaver, Black Widow, Box",
			   "Calvin (and Hobbes), Cub, Charlie Chaplin, Call of Duty/COD, Clint Eastwood, Coffee, Cigarette, Church, Cinnamon, Cage, Cake, Clown, Cookie Monster, Chuck Norris, Coyote, Chris Pratt, Croquet, Car, Counter Strike/CSGO, Cat, Cup, Cave, Cow, Chex Mix",
			   "Dagger, Dobby, David Copperfield, N/A, Dentist, Daffy Duck, Dog, Dough, (Princess) Diana, DJ (Full House), Donkey Kong, Doll, Darth Maul, Daniel (Greaves), Doe, Dude Perfect, Dairy Queen, Doctor, (Nintendo) DS, Donald Trump, Dunkin Donuts, Darth Vader, Dwarf, Dexter (Doggo)",
			   "Eagle, Emmett Brown, Eclipse, Ed (Sheeran), N/A, Elephant, Egg, Aaron Eckhart (Two Face), Einstein, Elton John, Elk, Ellie (Greaves), Eminem, Ent, Eeyore, Eponine (Les Miserables), Equestrian, ER/Hospital, Eskimo, ET/Extra Terrestrial, Europe, Eve, Ewan (McGregor), Excalibur",
			   "Fat Albert, Facebook, Fifty Cent, Fedora, Ferret, N/A, Frag (Grenade), Fire Helmet, Fishsticks, Fudge, Fork, Flower, Foam, Fan, Fossil, Face Paint, Lord Farquaad, Fruit (Salad), Fish, Photo, Foosball, (High) Five, Ferris Wheel, Fox",
			   "Green Apples, Gob (Arrested Development), Gamecube, God, Gentleman, Giraffe, N/A, Gandhi, GI Joe, Grape Juice, Green Knight, Goal, Gollum, Gun (Pistol), Gorilla, Grapes, Guacamole, Gore, Gas, Goat, Guitar, Gravel, George Washington, Gan X",
			   "Harp, Hobbit, Helicopter, Hot Dog, He-Man, Harrison Ford, Hermione Granger, N/A, Hippo, Hedge, Captain Hook, Hell, Hammer, Honey, Hoe, Harry Potter, Harley Quinn, Horse, High School, Hut, Hunter, Hoverboard, Hawk, Hex",
			   "Ian, Ibrahimovic, Ice, ID Card, Idris Elba (Charles Miner), Isla Fisher, Iguana, Incredible Hulk, Inigo (Montoya), Indiana Jones, IKEA, Ill (Person), Iron Man, Inn, Io (Heifer), IPod, IQ (R6S), Ireland, ISIS, Italian, KPop Singer, Ivy (Doggo), Inch Worm, Ibex",
			   "Jayhawk, James Bond, Julius Caesar, Jedi, Jesus, Jeff (Posey), Jake Gyllenhaal, Jabba the Hutt, Giant, N/A, Joker, Jared Leto, Jim (Dad), John (Bartlett), Joe/Joseph (Ballard), Jaiden Powell, John Quincy (Adams), Jerry (Seinfeld), Josh (Rozelle), Jet, Juliet (O'hara), Javelin, Jackson Whal/JW/J-Dubs, Jackson (Swanson)",
			   "Kangaroo, Kobe Bryant, Kansas City Chiefs, Kevin Durant, Ketchup, KFC, KGB, Khalid, Kite, King Julien, N/A, Katrina Liberto (Hadley), Kermit, Knight, Koala, Kingpin, Chess (King and Queen), Kramer, KSI, Katana, Kung FU, Kevin (Malone), Killer Whale, Kix (cereal)",
			   "(Princess) Leia, Labrador/Lab, Lucifer, Ladder, Lemon, Elf, Lego, Lighthouse, Lion, Lebron James, Mr. Lockhart, N/A, Lamb, Lantern, Lilo (and Stitch), Leprechaun, Liquor, Lorax, Luke Skywalker, Lieutenant, (Professor) Lupin, Lord Voldemort, Lawnmower, Lex (Luthor)",
			   "Mask, Mercedes Benz, Minecraft, Maid, Meth, Muffin, Megamind, Miami Heat, MI5, Michael Jordan, Monkey, Mona Lisa, N/A, Minion, Moana, Max Park, Mannequin, Mark Ruffalo, Mouse, Mr. T, Emu, Mini Van, Mace Windu, Mexican",
			   "Salt, Nebula (Marvel), Nacho (Breaking Bad), Ned (Forrester), Neo, Knife, (Chicken) Nugget, NHL, (Bill) Nye, Ninja, Nick (Attilis), Noelle (Smedley), Nemo, N/A, Gnome, Napolean, NyQuil, Nerd, Nest, Nathan (Docherty), Newman, Navy, Narwhal, Nixon",
			   "Boa (Snake), Obi-wan (Kenobi), Octopus, Odin (Thor's Dad), Oreo, Officer, Ogre, One Hand (Person), Oil, OJ (Simpson), (Lily) Och, Olive, Oatmeal, Onion, N/A, Oprah, Orc, Orange, Ostrich, Otter, Ouiji Board, Oven, Owl, Ox",
			   "Pam (Hadley), Polar Bear, Peacock, Panda, Penguin, Pufferfish, Pig, Pharaoh, Pie, Pajamas/PJs, Pikachu, Platypus, Night, Pen, Po (Kung Fu Panda), N/A, Porcupine, Pear, Playstation, Pterodactyl, Pumbaa (Lion King), Peeves (Harry Potter), Powerpuff Girls, Pickaxe",
			   "Quagga (Extinct Zebra), Quarterback/QB, Quack (Duck), Quidditch, Queen Elizabeth, Quaffle, Qui-Gon (Jinn), Quiche, Quill, Squeegee, Quaker Oats (Person), (Professor) Quirrel, Queen Mary, Queen, Quasimodo, Quarter Pounder (McDonald's Burger), N/A, Quarter, Questiony the Question Mark (Seus Gravity Falls), Q-Tip, Queue (Line), Quiver, QWOP, Quicksand",
			   "Rachel (Friends), Rabbit, Race, Red (Shawshank Redemption), Reese's, Referee/Ref, Rag, Rhino, Rye (Bread), Raj (Big Bang Theory), The Rock, Red Lobster, Rome, Raisin, Ronin (Hawkeye Assassin), Rope, Racquetball, N/A, Ross (Friends), Rat, Roulette, Recreational Vehicle/RV, Ron Weasely, (Captain) Rex",
			   "Saw, Submarine, Scorpion, Scooby Doo, Sea, Softball, Segway, Sheep, Psy (Gangnam Style), Slim Jim, Skeleton, Seal, Sam (Wortendyke), Sonic (the Hedgehog), Soap, Spaghetti, Squirrel, Star, Schutzstaffel/SS, Santa, Steve Urkel, Sven (Pewdiepie doggo), Subway, Saxophone",
			   "Taylor (Swift), Table, Taco, Toad (Nintendo), Telephone, Tie Fighter, Tiger, Thor, Tire, Thomas Jefferson, Tank, Turtle, Tinman, Tenten, Toe, Toilet Paper, Taquitos, Tree, Tom Sawyer, N/A, Tutu, Television/TV, Towel, Tuxedo/Tux",
			   "Under Armour (Shirt), Usain Bolt, Unicorn, Undead (Zombie), Ukulele, UFO, Uggs, Uhaul, Unicycle, Luiji, United Kingdom/UK, Ulysses (S. Grant), Umbrella, Uno, Yu-Gi-Oh, UPS, Uruk-Hai (Lord of the Rings), Urinal, Uncle Sam, Undertaker (WWE), N/A, UAV, Hugo Weaving (Agent Smith Matrix), Horcrux",
			   "V8 (Drink), Volleyball, Vacuum, Video, Vending Machine, Venus Flytrap, Vegetable, Van Halen, Violet (Incrdibles), Viet-John/VJ, Viking, Vladimir (Putin), Venom, Violin, Volcano, Vape, Ventriloquist, Virtual Reality/VR, Vase, Veteran, Vulture, N/A, Volkswagen, Vortex (Nerf Football)",
			   "Whale, Web, Witch, Woody (Toy Story), Weed, Waffle, Wig, Whistle, (Nintendo) Wii, Wedgie, Wookie, Wall-E, Walmart, Window, Wolf, Whopper (Candy), John Wick, War, Wasabi, Water, Woof (Dog Bark), Weave, Walter White, Wax",
			   "Xandar (Marvel Planet), Zeb (Rebels), Zucchini, Zelda, Zeus, Zac Efron, Zigzag, Electrocuted Hitler, Iceman, Juggernaut (X-Men), Zach (Harwood), (Arnum) Zola, Magneto, Christian, Tic-Tac-Toe, Phoenix (X-Men), Quicksilver, X-Ray, Spiderman, Electrocuted Turtle, Electrocuted Unicorn, Xavier, Wolverine, N/A"]




# Parcel up each line into a list
for i in range(len(spread_sheet)):
    spread_sheet[i] = spread_sheet[i].split(",")

    # Go through each line
    for j in range(len(spread_sheet[i])):
        # Get rid of all the spaces
        spread_sheet[i][j] = spread_sheet[i][j].strip(" ")