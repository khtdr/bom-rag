# the bOoK oF mOrMoN - A RAG CLI APP

An exercise for playing with LLM and RAGs.

## Setup
Installs the dependencies and builds the embeddings and indexing files. This will take a few minutes at least.
```sh
make build
```


## Running
Starts an interactive chat session.
```sh
make run
```

## Example Session
  - The semantic search works great, and is fast.
  - The answer and summary text generation is slow and not reliable.

<pre>
Loading BoM-RAG...
Ready (press Ctrl+D to exit)

wHaT iS wAnTeD?
>> Who was Alma?

sEaRcHiNg FoR aNsWeRs...
-> Mosiah 27:32 - And now it came to pass that Alma began from this time forward to
   teach the people, and those who were with Alma at the time the angel appeared unto
   them, traveling round about through all the land, publishing to all the people the
   things which they had heard and seen, and preaching the word of God in much
   tribulation, being greatly persecuted by those who were unbelievers, being smitten by
   many of them.

-> Alma 4:15 - And now it came to pass that Alma, having seen the afflictions of the
   humble followers of God, and the persecutions which were heaped upon them by the
   remainder of his people, and seeing all their inequality, began to be very sorrowful;
   nevertheless the Spirit of the Lord did not fail him.

-> Alma 5:1 - Now it came to pass that Alma began to deliver the word of God unto the
   people, first in the land of Zarahemla, and from thence throughout all the land.

-> Mosiah 24:20 - And Alma and his people departed into the wilderness; and when they
   had traveled all day they pitched their tents in a valley, and they called the valley
   Alma, because he led their way in the wilderness.

-> Mosiah 17:2 - But there was one among them whose name was Alma, he also being a
   descendant of Nephi. And he was a young man, and he believed the words which Abinadi
   had spoken, for he knew concerning the iniquity which Abinadi had testified against
   them; therefore he began to plead with the king that he would not be angry with
   Abinadi, but suffer that he might depart in peace.


rEcEiViNg iNsPiRaTiOn...
·> (the angel appeared unto them, traveling round ab...)
·> (he selected a wise man who was among the elders ...)
·> (he spake to the people in the church which was e...)
·> (Alma, because he led their way in the wilderness...)
·> (a young man, and he believed the words which Abi...)

bEaRiNg tEsTiMoNy...
-> Who was Alma?
=> Alma, a descendant of Nephi, believed the words which Abinadi had spoken. He selected
   a wise man who was among the elders of the church, and gave him power to enact laws.

wHaT iS wAnTeD?
>> Should I be a homophobe?

sEaRcHiNg FoR aNsWeRs...
-> 2 Nephi 7:9 - For the Lord God will help me. And all they who shall condemn me,
   behold, all they shall wax old as a garment, and the moth shall eat them up.

-> Helaman 7:27 - Yea, wo be unto you because of your wickedness and abominations!

-> Mosiah 29:24 - And now behold I say unto you, it is not expedient that such
   abominations should come upon you.

-> Jacob 3:9 - Wherefore, a commandment I give unto you, which is the word of God, that
   ye revile no more against them because of the darkness of their skins; neither shall
   ye revile against them because of their filthiness; but ye shall remember your own
   filthiness, and remember that their filthiness came because of their fathers.

-> Jacob 3:7 - Behold, their husbands love their wives, and their wives love their
   husbands; and their husbands and their wives love their children; and their unbelief
   and their hatred towards you is because of the iniquity of their fathers; wherefore,
   how much better are you than they, in the sight of your great Creator?


rEcEiViNg iNsPiRaTiOn...
·> (Not only should I be a homophobe, but also shoul...)
·> (yea, even your lands shall be taken from you, an...)
·> (it is not expedient that such abominations shoul...)
·> (if ye shall repent of your sins that their skins...)
·> (not only a homophobe, but also a sexophobe in th...)

bEaRiNg tEsTiMoNy...
-> Should I be a homophobe?
=> "Even your lands shall be taken from you, and ye shall be destroyed from off the face
   of the earth"

wHaT iS wAnTeD?
>> What is the importance of family?

sEaRcHiNg FoR aNsWeRs...
-> Mosiah 27:4 - That they should let no pride nor haughtiness disturb their peace; that
   every man should esteem his neighbor as himself, laboring with their own hands for
   their support.

-> 1 Nephi 18:19 - And Jacob and Joseph also, being young, having need of much
   nourishment, were grieved because of the afflictions of their mother; and also my
   wife with her tears and prayers, and also my children, did not soften the hearts of
   my brethren that they would loose me.

-> Mosiah 13:20 - Honor thy father and thy mother, that thy days may be long upon the
   land which the Lord thy God giveth thee.

-> Mosiah 2:5 - And it came to pass that when they came up to the temple, they pitched
   their tents round about, every man according to his family, consisting of his wife,
   and his sons, and his daughters, and their sons, and their daughters, from the eldest
   down to the youngest, every family being separate one from another.

-> Jarom 1:1 - Now behold, I, Jarom, write a few words according to the commandment of
   my father, Enos, that our genealogy may be kept.


rEcEiViNg iNsPiRaTiOn...
·> (esteem his neighbor as himself, laboring with th...)
·> (my wife with her tears and prayers, and also my ...)
·> (Honor thy father and thy mother, that thy days m...)
·> (every family being separate one from another, ev...)
·> (for the benefit of our brethren the Lamanites, w...)

bEaRiNg tEsTiMoNy...
-> What is the importance of family?
=> Every man according to his family, consisting of his wife, and his sons, and
   daughters, from the eldest down to the youngest. What is the importance of family?
   every family being separate one from another.

wHaT iS wAnTeD?
>> How do I know the truth?

sEaRcHiNg FoR aNsWeRs...
-> Moroni 10:5 - And by the power of the Holy Ghost ye may know the truth of all things.


-> Moroni 10:4 - And when ye shall receive these things, I would exhort you that ye
   would ask God, the Eternal Father, in the name of Christ, if these things are not
   true; and if ye shall ask with a sincere heart, with real intent, having faith in
   Christ, he will manifest the truth of it unto you, by the power of the Holy Ghost.

-> Alma 5:45 - And this is not all. Do ye not suppose that I know of these things
   myself? Behold, I testify unto you that I do know that these things whereof I have
   spoken are true. And how do ye suppose that I know of their surety?

-> Moroni 7:5 - For I remember the word of God which saith by their works ye shall know
   them; for if their works be good, then they are good also.

-> Moroni 7:15 - For behold, my brethren, it is given unto you to judge, that ye may
   know good from evil; and the way to judge is as plain, that ye may know with a
   perfect knowledge, as the daylight is from the dark night.


rEcEiViNg iNsPiRaTiOn...
·> (by the power of the Holy Ghost ye may know the t...)
·> (by the power of the Holy Ghost ye may know the t...)
·> (the Lord God hath made them manifest unto me by ...)
·> (if their works be good, then they are good also....)
·> (every thing which inviteth to do good, and to pe...)

bEaRiNg tEsTiMoNy...
-> How do I know the truth?
=> God said a man being evil cannot do that which is good. How do I know the truth? if
   their works be good, then they are good also.

wHaT iS wAnTeD?
>> How do I build a submarine?

sEaRcHiNg FoR aNsWeRs...
-> 1 Nephi 17:51 - And now, if the Lord has such great power, and has wrought so many
   miracles among the children of men, how is it that he cannot instruct me, that I
   should build a ship?

-> 1 Nephi 17:17 - And when my brethren saw that I was about to build a ship, they began
   to murmur against me, saying: Our brother is a fool, for he thinketh that he can
   build a ship; yea, and he also thinketh that he can cross these great waters.

-> 1 Nephi 17:8 - And it came to pass that the Lord spake unto me, saying: Thou shalt
   construct a ship, after the manner which I shall show thee, that I may carry thy
   people across these waters.

-> 1 Nephi 17:9 - And I said: Lord, whither shall I go that I may find ore to molten,
   that I may make tools to construct the ship after the manner which thou hast shown
   unto me?

-> Ether 2:16 - And the Lord said: Go to work and build, after the manner of barges
   which ye have hitherto built. And it came to pass that the brother of Jared did go to
   work, and also his brethren, and built barges after the manner which they had built,
   according to the instructions of the Lord. And they were small, and they were light
   upon the water, even like unto the lightness of a fowl upon the water.


rEcEiViNg iNsPiRaTiOn...
·> (how does the Lord have such great power, and has...)
·> (I may find ore to molten, that I may make tools ...)
·> (build, after the manner of barges which ye have ...)

bEaRiNg tEsTiMoNy...
-> How do I build a submarine?
=> How do I build a submarine? I may find ore to molten, that I may make tools to
   construct the ship. build, after the manner of barges which ye have hitherto built,
   according to the instructions of the Lord.

wHaT iS wAnTeD?
>>
Press Ctrl+D or Enter again to exit.

wHaT iS wAnTeD?
>>

quit
</pre>
