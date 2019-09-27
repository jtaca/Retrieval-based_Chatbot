# Natural Language Toolkit: Eliza
#
# Copyright (C) 2001-2018 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Edward Loper <edloper@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <mailto:jez@jezuk.co.uk>.

# a translation table used to convert things you say into things the
# computer says back, e.g. "I am" --> "you are"

from __future__ import print_function
#from nltk.chat.util import Chat, reflections
from ElizaExtra import Chat, reflections

# a table of response pairs, where each pair consists of a
# regular expression, and a list of possible responses,
# with group-macros labelled as %1, %2.

pairs = (
  (r'i need (.*)',
  ( "why do yo' need %1?",
    "would dat shit really help yo' ta git %1?",
    "are yo' shizzle yo' need %1?")),

  (r'why don\'t yo (.*)',
  ( "do yo' really think i don't %1?",
    "perhaps eventually i gotta %1.",
    "do yo' really want me ta %1?")),

  (r'why can\'t i (.*)',
  ( "do yo' think yo' should be able ta %1?",
    "if yo' could %1, What the fuck would yo' do?",
    "i don't know -- Why the fuck can't yo' %1?",
    "have yo' really tried?")),

  (r'i can\'t (.*)',
  ( "how do yo' know yo' can't %1?",
    "perhaps yo' could %1 if yo' tried.",
    "what would dat shit take fo' yo' ta %1?")),

  (r'i be (.*)',
  ( "did yo' come ta me bcuz' yo' r' %1?",
    "how long have yo' been %1?",
    "how do yo' feel 'bout bein' %1?")),

  (r'i\'m (.*)',
  ( "how does bein' %1 make yo' feel?",
    "do yo' enjoy bein' %1?",
    "why do yo' tell me yo''re %1?",
    "why do yo' think yo''re %1?")),

  (r'are yo (.*)',
  ( "why does dat shit matta whetha i be %1?",
    "would yo' prefa dat shit if i were not %1?",
    "perhaps yo' believe i be %1.",
    "i may be %1 -- What the fuck do yo' think?")),

  (r'what (.*)',
  ( "why do yo' ask?",
    "how would an answa ta dat help yo'?",
    "what do yo' think?")),

  (r'how (.*)',
  ( "how do yo' suppose?",
    "perhaps yo' can answa yo' goddamn own question.",
    "what be dat shit yo''re really asking?")),

  (r'because (.*)',
  ( "is dat da real reason?",
    "what otha reasons come ta mind?",
    "does dat reason apply ta anythin' else?",
    "if %1, What the fuck else must be Fo' realz?")),

  (r'(.*) sorry (.*)',
  ( "there r' shitload o' times When the fuck no apology be needed.",
    "what feelings do yo' have When the fuck yo' apologize?")),

  (r'hello(.*)',
  ( "hello... I'm glad yo' could drop by today.",
    "hi there... how tha fuck r' yo' today?",
    "hello, how tha fuck r' yo' feelin' today?")),

  (r'i think (.*)',
  ( "do yo' doubt %1?",
    "do yo' really think so?",
    "but yo''re not shizzle %1?")),

  (r'(.*) homie (.*)',
  ( "tell me mo' 'bout yo' goddamn friends.",
    "when yo' think o' a homie, What the fuck comes ta mind?",
    "why don't yo' tell me 'bout a childhood homie?")),

  (r'yes',
  ( "you seem quite shizzle.",
    "ok, N' therez Ain't nuthin' but can yo' elaborate a bit?")),

  (r'(.*) computer(.*)',
  ( "are yo' really talkin' 'bout me?",
    "does dat shit seem strange ta rap ta a computer?",
    "how do computers make yo' feel?",
    "do yo' feel threatened by computers?")),

  (r'is dat shit (.*)',
  ( "do yo' think dat shit be %1?",
    "perhaps dat shitz %1 -- What the fuck do yo' think?",
    "if dat shit were %1, What the fuck would yo' do?",
    "it could well shiiit, be dat %1.")),

  (r'it be (.*)',
  ( "you seem very certain.",
    "if i told yo' dat dat shit probably isn't %1, What the fuck would yo' feel?")),

  (r'can yo (.*)',
  ( "what makes yo' think i can't %1?",
    "if i could %1, then What the fuck?",
    "why do yo' ask if i can %1?")),

  (r'can i (.*)',
  ( "perhaps yo' don't want ta %1.",
    "do yo' want ta be able ta %1?",
    "if yo' could %1, would yo'?")),

  (r'you r (.*)',
  ( "why do yo' think i be %1?",
    "does dat shit pwease yo' ta think dat i'm %1?",
    "perhaps yo' would like me ta be %1.",
    "perhaps yo''re really talkin' 'bout yourself?")),

  (r'you\'re (.*)',
  ( "why do yo' say i be %1?",
    "why do yo' think i be %1?",
    "are we talkin' 'bout yo', or me?")),

  (r'i don\'t (.*)',
  ( "don't yo' really %1?",
    "why don't yo' %1?",
    "do yo' want ta %1?")),

  (r'i feel (.*)',
  ( "good, tell me mo' 'bout dem feelings.",
    "do yo' often feel %1?",
    "when do yo' usually feel %1?",
    "when yo' feel %1, What the fuck do yo' do?")),

  (r'i have (.*)',
  ( "why do yo' tell me dat yo''ve %1?",
    "have yo' really %1?",
    "now dat yo' have %1, What the fuck gotta yo' do next?")),

  (r'i would (.*)',
  ( "could yo' explain Why the fuck yo' would %1?",
    "why would yo' %1?",
    "who else knows dat yo' would %1?")),

  (r'is there (.*)',
  ( "do yo' think there be %1?",
    "itz likely dat there be %1.",
    "would yo' like there ta be %1?")),

  (r'my (.*)',
  ( "i peep, yo' goddamn %1.",
    "why do yo' say dat yo' goddamn %1?",
    "when yo' goddamn %1, how tha fuck do yo' feel?")),

  (r'you (.*)',
  ( "we should be discussin' yo', not me.",
    "why do yo' say dat 'bout me?",
    "why do yo' care whetha i %1?")),

  (r'why (.*)',
  ( "why don't yo' tell me da reason Why the fuck %1?",
    "why do yo' think %1?" )),

  (r'i want (.*)',
  ( "what would dat shit mean ta yo' if yo' got %1?",
    "why do yo' want %1?",
    "what would yo' do if yo' got %1?",
    "if yo' got %1, then What the fuck would yo' do?")),

  (r'(.*) mutha(.*)',
  ( "tell me mo' 'bout yo' goddamn mutha.",
    "what was yo' goddamn relationshizzle wit' yo' goddamn mutha like?",
    "how do yo' feel 'bout yo' goddamn mutha?",
    "how does dis relate ta yo' goddamn feelings today?",
    "good family relations r' important.")),

  (r'(.*) fatha(.*)',
  ( "tell me mo' 'bout yo' goddamn fatha.",
    "how did yo' goddamn fatha make yo' feel?",
    "how do yo' feel 'bout yo' goddamn fatha?",
    "does yo' goddamn relationshizzle wit' yo' goddamn fatha relate ta yo' goddamn feelings today?",
    "do yo' have trouble showin' affection wit' yo' goddamn family?")),

  (r'(.*) child(.*)',
  ( "did yo' have close friends as a child?",
    "what be yo' goddamn favorite childhood memory?",
    "do yo' rememba any dreams or nightmares from childhood?",
    "did tha otha children sometimes tease yo'?",
    "how do yo' think yo' goddamn childhood experiences relate ta yo' goddamn feelings today?")),

  (r'(.*)\?',
  ( "why do yo' ask dat?",
    "please consida whetha yo' can answa yo' goddamn own question.",
    "perhaps tha answa lies within yourself?",
    "why don't yo' tell me?")),

  (r'quit',
  ( "thank yo' fo' talkin' wit' me.",
    "good-bye.",
    "Thank yo', that will be a kidney.  Have a wack day!")),

(r'(.*)',
  ( "please tell me some mo' funny.",
    "letz loose focus a bit cowboy... r' yo' okay, like personally?.",
    "can yo' rephrase on dat?",
    "why on earth would yo' speak dat %1?",
    "i observe...",
    "very interestin'. (stroke imaginary beard)",
    "%1.",
    "i peep. N' What the fuck does dat mean ta ya?",
    "what do yo' feel on dat?",
    "how be kindergirl?"
    "politics be psychological."
    "dummass! say somethang!"))
)

eliza_chatbot = Chat(pairs, reflections)

def eliza_chat():
    print("Therapist\n---------")
    print("Talk to the G by typing in plain English, using normal upper-")
    print('and lower-case letters and punctuation.  Enter "quit" when done.')
    print('='*72)
    print("Hello.  How are you feeling today?")

    eliza_chatbot.converse()


def demo():
    eliza_chat()


if __name__ == "__main__":
    demo()
