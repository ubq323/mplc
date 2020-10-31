# multiplayer lambda calculus - initial design

two players selected, fight against each other. probably use some kind of matchmaking elo thing system or something.

## gameplay
you have some (smallish) number of "slots". (probably 10ish?). each contains a lambda function expression.
there are also a fixed number of "cards"/"combinators" in front of you (possibly have special gamemodes with different sets?)
some of these are standard ski combinators, some are like 0 and succ, some have sideeffects that you use to hurt your opponent.

on each turn you can either apply a combinator to the value of one of your slots or apply a slot to a card. in the 
default gamemode you have an unlimited amount of each card and can use any card on any turn. 
probably you can apply slots to other slots as well.

after this the slot in question gets β-reduced until it is in β-normal form.
if it does not halt after a certain number of steps then it explodes and gets 
replaced with the identity function.

each slot has a health. a slot with a health of 0 cannot be used. if all of a player's
slots have health 0 the other player wins. after some number of turns if neither player has
won, the one with the most living slots wins (or it's a draw if they're even).

or, alternatively, each player just has a single health amount. idk.

## combinators
there will be an SKI gamemode where the only way to do complicated things is to use S and 
K combinators, but that's quite annoying for base gameplay so there will probably be
easier ones available by default. not entirely sure how that would work though hmm.

the list is probably something like
- identity **I**: λx.x
- **S** and **K** combinators
  - **S**: λx.λy.λz.xz(yz)
  - **K**: λx.λy.x
- numbers: **0** and **succ** and probably **pred** and **double** and maybe some others
- **apply**: some way of applying functions to each other. maybe takes a value and a slot number and applies one to the other then returns the result, or something.
- **get** takes a church-encoded slot number and returns the current value of that slot, **put** takes a church-encoded slot number and a value and sets the slot's value to that value.
- **clear** takes a church-encoded slot number and sets that slot's value to **I**.
- **attack** allows you to sacrifice some health of one of your slots (or maybe some other resource?) to damage one of the opponent's slots somehow. maybe **dec** decreases the health of the given slot of the opponent by 1 and **inc** increases the health of your given slot by 1.
- maybe in some gamemodes there is an **number[*n*]** which is really a family of combinators that allows the player to create any given (church-encoded) number without messing about with succ. then in some gamemodes this wouldn't be available.
- **copy** which returns the current value of the given slot of the opponent.

we can probably think of plenty of other ones too.

## implementation details
client will be a web app. ideally communication with the server won't use websockets
at all, so that it can work behind strange proxies and lans and things as well.

we will need to develop some sort of system for doing β-reduction on arbitrary lambda
expressions, with support for builtin functions with arbitrary side effects. this will
ideally be developed as a separate library because it'll probably be quite useful
for other stuff as well besides this.

most game code will probably be done on the server to avoid cheating and things. the client
will basically just display the current match state and send http requests when buttons are clicked.
