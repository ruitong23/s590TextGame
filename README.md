# intro
ruitong_sun rsun13

Estimate time: 25hrs 

Testing by: assert and doctest I made a spread adventure.py which doctest and assert on it, I try to do it on the original file but it just take too many space to do. and it makes the file looks very unreadable. I also makes many assert which used to test on some small functions. 

During the testing, all the bug that was found has been fixed with the code, or by extra help extention. 


# issues
1. equiped item won't when drop, will not reduce the damage the player curent have, it will only changed after there is a thing equiped
2. Trying to modfiy the get function to make it able to assign a damage boost for the item player pick up like all other games, but we are not allow to modfiy the base function
3. adding attack function but there is no object to attack with. 
4. Trying to make a attack function, but soon notice if able to make attack function reasonable it need to have multiple extra function to make it work as a game. 


# solve
1. by checking if the drop item is same as the equiped item if it is, reset the player damage to 1 
2. making a 2 extra extension called enhance and check, which enhance will able to let the weapon able to assign the damge boots to the item. Check will allow the player able to see how much damage they can get from this weapon. 
3. Maked a new object called monster, Which is part of the map like item. When the map is load it will put the monster in the game which allow player to attack. 

# How to play and use the extensions
there is technologically 7 extensions in the game
1. drop verb
2. equip verb
3. check verb
4. enhance verb
5. attack verb
6. token object
7. monster object

1. Drop function: is work just like what was in the assignment. You can only drop a item with in you inventory. then it will drop the item in your inventory or equiped item
You can use it by >drop <item name> 
2. Equip verb: a function that helps player to get damage boots. player can get attack damage by equip an enhance item. you can only equip the item in your invertory  then you will be able to using enhance function and check function on teh equip item. If you equipped item is enhanced it can also gives you damage boost
you can use it by >equip <item name>
3. Check function: an extra function after notice we can't modify the get function. part of the original get function which will show the item that player equipped. It will gives player information on how many damage boost this item have, and what is the quilty of this item. 
you can use it by >check 
4. Enhance function: an extra function after notice we can't modify the get function. This function will able to adding damge boost to the item that player equipped. there is 2 preconditions before using this. 1. player need to equipped an item, 2. there must be a enhance token in the room. it will ramdomly assign damage between 1-20 to the item, and it will also rename the item from common to legendary as part of the item name that can be checked by using check function. 
you can use this by >enhance 
5. attack function: a function that allow player to attack the monster in the room. Only usable when there is a monster in the same room as what player at. this function will cost ramdom damage between 1-10 to the monster, if player equipped an item it will make 1-10 * item boost damage to the monster. When the monster hp < 0 it will also remove the monster from the room. 
you can use it by >attack 

# map object 
6. token object: an extra object for enhance:  because of the enhance I adding a little extra things for the game play to make enhance little hard to do. 
You can add it to the map by: "token": ["enhance"]

7. monster object: an extra object for attack. Given a target to the player to use the attack function.
You can add it to the map by: "monster": {"name": "Goblin", "health": 30}
