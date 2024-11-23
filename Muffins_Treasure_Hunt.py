import os
import platform
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
import time
import re
from PyPDF2 import PdfReader
from docx import Document
import csv
import sys

# Paths for results
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Muffins_Treasure_Hunt_Results")
CONSOLE_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Console_Log.txt")
ERROR_LOG_FILE = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Errors.txt")

# Global Variables
KEYWORDS_ICONS = {
    "crypto": "🪙", "wallet": "💰", "bitcoin": "₿", "ethereum": "Ξ", "doge": "🐕",
    "litecoin": "Ł", "key": "🔑", "phrase": "✍️", "secret": "🤫", "password": "🔒",
    "passphrase": "✏️", "xpub": "📜", "0x": "📬", "backup": "📂", "seed": "🌱",
    "private": "🕶️", "important": "⭐", "credentials": "📋", "blockchain": "⛓️",
    "coins": "💵", "hash": "🔗", "wallet.dat": "📄", "ripple": "🌊",
    "stellar": "🌟", "tron": "🚀", "bnb": "⚡", "solana": "☀️",
    "cardano": "🌌", "mnemonic": "🧠", "recovery": "📦", "restore": "🔄",
    "seed phrase": "🔐", "secret phrase": "🔓", "metamask": "🦊",
    "phantom": "👻", "keystore": "📁", "ledger": "📒", "trezor": "🔐",
    "cold storage": "❄️", "pk": "🗝️", "private_key": "🗝️", "xprv": "📜",
    "encrypted": "🔒", "kdfparams": "📑", "cipher": "🔐", "ciphertext": "🔏",
    "btc": "₿", "eth": "Ξ", "ltc": "Ł", "xrp": "🌊", "xlm": "🌟",
    "ada": "🌌", "trx": "🚀", "json": "📄", "dat": "📄", "ftx": "🚩",
    "mtgox": "⚠️", "quadrigacx": "❗", "bitconnect": "❌", "cryptopia": "⚡",
    "nicehash": "💻", "binance": "⚡", "kraken": "🐙", "gemini": "♊",
    "bitstamp": "📈", "okx": "📊", "huobi": "🔥", "bybit": "📉",
    "bitfinex": "🏦", "uniswap": "💱", "exodus": "📂", "trustwallet": "🔒",
    "atomic wallet": "💥", "bluewallet": "🔵", "safepal": "🔐", "guarda": "🔒"
}

# Adjust EXCLUDED_PATHS based on platform
if platform.system() == "Windows":
    EXCLUDED_PATHS = ["C:\\Windows", "C:\\Program Files", os.path.expanduser("~\\AppData")]
else:
    EXCLUDED_PATHS = ["/System", "/Library", "/Applications", "/bin", "/sbin", "/usr", "/var", "/dev", "/proc", "/run", "/sys"]

# File extensions to ignore
IGNORED_EXTENSIONS = [".exe", ".dll", ".sys", ".tmp", ".log", ".ini", ".dat", ".js", ".ts"]

# Folders to exclude
EXCLUDED_FOLDERS = ["images", "icons", "img16_16", "img24_24", "img32_32", "sketches"]

# Mnemonic wordlist (BIP39 English wordlist)
MNEMONIC_WORDLIST = set("""
abandon
ability
able
about
above
absent
absorb
abstract
absurd
abuse
access
accident
account
accuse
achieve
acid
acoustic
acquire
across
act
action
actor
actress
actual
adapt
add
addict
address
adjust
admit
adult
advance
advice
aerobic
affair
afford
afraid
again
age
agent
agree
ahead
aim
air
airport
aisle
alarm
album
alcohol
alert
alien
all
alley
allow
almost
alone
alpha
already
also
alter
always
amateur
amazing
among
amount
amused
analyst
anchor
ancient
anger
angle
angry
animal
ankle
announce
annual
another
answer
antenna
antique
anxiety
any
apart
apology
appear
apple
approve
april
arch
arctic
area
arena
argue
arm
armed
armor
army
around
arrange
arrest
arrive
arrow
art
artefact
artist
artwork
ask
aspect
assault
asset
assist
assume
asthma
athlete
atom
attack
attend
attitude
attract
auction
audit
august
aunt
author
auto
autumn
average
avocado
avoid
awake
aware
away
awesome
awful
awkward
axis
baby
bachelor
bacon
badge
bag
balance
balcony
ball
bamboo
banana
banner
bar
barely
bargain
barrel
base
basic
basket
battle
beach
bean
beauty
because
become
beef
before
begin
behave
behind
believe
below
belt
bench
benefit
best
betray
better
between
beyond
bicycle
bid
bike
bind
biology
bird
birth
bitter
black
blade
blame
blanket
blast
bleak
bless
blind
blood
blossom
blouse
blue
blur
blush
board
boat
body
boil
bomb
bone
bonus
book
boost
border
boring
borrow
boss
bottom
bounce
box
boy
bracket
brain
brand
brass
brave
bread
breeze
brick
bridge
brief
bright
bring
brisk
broccoli
broken
bronze
broom
brother
brown
brush
bubble
buddy
budget
buffalo
build
bulb
bulk
bullet
bundle
bunker
burden
burger
burst
bus
business
busy
butter
buyer
buzz
cabbage
cabin
cable
cactus
cage
cake
call
calm
camera
camp
can
canal
cancel
candy
cannon
canoe
canvas
canyon
capable
capital
captain
car
carbon
card
cargo
carpet
carry
cart
case
cash
casino
castle
casual
cat
catalog
catch
category
cattle
caught
cause
caution
cave
ceiling
celery
cement
census
century
cereal
certain
chair
chalk
champion
change
chaos
chapter
charge
chase
chat
cheap
check
cheese
chef
cherry
chest
chicken
chief
child
chimney
choice
choose
chronic
chuckle
chunk
churn
cigar
cinnamon
circle
citizen
city
civil
claim
clap
clarify
claw
clay
clean
clerk
clever
click
client
cliff
climb
clinic
clip
clock
clog
close
cloth
cloud
clown
club
clump
cluster
clutch
coach
coast
coconut
code
coffee
coil
coin
collect
color
column
combine
come
comfort
comic
common
company
concert
conduct
confirm
congress
connect
consider
control
convince
cook
cool
copper
copy
coral
core
corn
correct
cost
cotton
couch
country
couple
course
cousin
cover
coyote
crack
cradle
craft
cram
crane
crash
crater
crawl
crazy
cream
credit
creek
crew
cricket
crime
crisp
critic
crop
cross
crouch
crowd
crucial
cruel
cruise
crumble
crunch
crush
cry
crystal
cube
culture
cup
cupboard
curious
current
curtain
curve
cushion
custom
cute
cycle
dad
damage
damp
dance
danger
daring
dash
daughter
dawn
day
deal
debate
debris
decade
december
decide
decline
decorate
decrease
deer
defense
define
defy
degree
delay
deliver
demand
demise
denial
dentist
deny
depart
depend
deposit
depth
deputy
derive
describe
desert
design
desk
despair
destroy
detail
detect
develop
device
devote
diagram
dial
diamond
diary
dice
diesel
diet
differ
digital
dignity
dilemma
dinner
dinosaur
direct
dirt
disagree
discover
disease
dish
dismiss
disorder
display
distance
divert
divide
divorce
dizzy
doctor
document
dog
doll
dolphin
domain
donate
donkey
donor
door
dose
double
dove
draft
dragon
drama
drastic
draw
dream
dress
drift
drill
drink
drip
drive
drop
drum
dry
duck
dumb
dune
during
dust
dutch
duty
dwarf
dynamic
eager
eagle
early
earn
earth
easily
east
easy
echo
ecology
economy
edge
edit
educate
effort
egg
eight
either
elbow
elder
electric
elegant
element
elephant
elevator
elite
else
embark
embody
embrace
emerge
emotion
employ
empower
empty
enable
enact
end
endless
endorse
enemy
energy
enforce
engage
engine
enhance
enjoy
enlist
enough
enrich
enroll
ensure
enter
entire
entry
envelope
episode
equal
equip
era
erase
erode
erosion
error
erupt
escape
essay
essence
estate
eternal
ethics
evidence
evil
evoke
evolve
exact
example
excess
exchange
excite
exclude
excuse
execute
exercise
exhaust
exhibit
exile
exist
exit
exotic
expand
expect
expire
explain
expose
express
extend
extra
eye
eyebrow
fabric
face
faculty
fade
faint
faith
fall
false
fame
family
famous
fan
fancy
fantasy
farm
fashion
fat
fatal
father
fatigue
fault
favorite
feature
february
federal
fee
feed
feel
female
fence
festival
fetch
fever
few
fiber
fiction
field
figure
file
film
filter
final
find
fine
finger
finish
fire
firm
first
fiscal
fish
fit
fitness
fix
flag
flame
flash
flat
flavor
flee
flight
flip
float
flock
floor
flower
fluid
flush
fly
foam
focus
fog
foil
fold
follow
food
foot
force
forest
forget
fork
fortune
forum
forward
fossil
foster
found
fox
fragile
frame
frequent
fresh
friend
fringe
frog
front
frost
frown
frozen
fruit
fuel
fun
funny
furnace
fury
future
gadget
gain
galaxy
gallery
game
gap
garage
garbage
garden
garlic
garment
gas
gasp
gate
gather
gauge
gaze
general
genius
genre
gentle
genuine
gesture
ghost
giant
gift
giggle
ginger
giraffe
girl
give
glad
glance
glare
glass
glide
glimpse
globe
gloom
glory
glove
glow
glue
goat
goddess
gold
good
goose
gorilla
gospel
gossip
govern
gown
grab
grace
grain
grant
grape
grass
gravity
great
green
grid
grief
grit
grocery
group
grow
grunt
guard
guess
guide
guilt
guitar
gun
gym
habit
hair
half
hammer
hamster
hand
happy
harbor
hard
harsh
harvest
hat
have
hawk
hazard
head
health
heart
heavy
hedgehog
height
hello
helmet
help
hen
hero
hidden
high
hill
hint
hip
hire
history
hobby
hockey
hold
hole
holiday
hollow
home
honey
hood
hope
horn
horror
horse
hospital
host
hotel
hour
hover
hub
huge
human
humble
humor
hundred
hungry
hunt
hurdle
hurry
hurt
husband
hybrid
ice
icon
idea
identify
idle
ignore
ill
illegal
illness
image
imitate
immense
immune
impact
impose
improve
impulse
inch
include
income
increase
index
indicate
indoor
industry
infant
inflict
inform
inhale
inherit
initial
inject
injury
inmate
inner
innocent
input
inquiry
insane
insect
inside
inspire
install
intact
interest
into
invest
invite
involve
iron
island
isolate
issue
item
ivory
jacket
jaguar
jar
jazz
jealous
jeans
jelly
jewel
job
join
joke
journey
joy
judge
juice
jump
jungle
junior
junk
just
kangaroo
keen
keep
ketchup
key
kick
kid
kidney
kind
kingdom
kiss
kit
kitchen
kite
kitten
kiwi
knee
knife
knock
know
lab
label
labor
ladder
lady
lake
lamp
language
laptop
large
later
latin
laugh
laundry
lava
law
lawn
lawsuit
layer
lazy
leader
leaf
learn
leave
lecture
left
leg
legal
legend
leisure
lemon
lend
length
lens
leopard
lesson
letter
level
liar
liberty
library
license
life
lift
light
like
limb
limit
link
lion
liquid
list
little
live
lizard
load
loan
lobster
local
lock
logic
lonely
long
loop
lottery
loud
lounge
love
loyal
lucky
luggage
lumber
lunar
lunch
luxury
lyrics
machine
mad
magic
magnet
maid
mail
main
major
make
mammal
man
manage
mandate
mango
mansion
manual
maple
marble
march
margin
marine
market
marriage
mask
mass
master
match
material
math
matrix
matter
maximum
maze
meadow
mean
measure
meat
mechanic
medal
media
melody
melt
member
memory
mention
menu
mercy
merge
merit
merry
mesh
message
metal
method
middle
midnight
milk
million
mimic
mind
minimum
minor
minute
miracle
mirror
misery
miss
mistake
mix
mixed
mixture
mobile
model
modify
mom
moment
monitor
monkey
monster
month
moon
moral
more
morning
mosquito
mother
motion
motor
mountain
mouse
move
movie
much
muffin
mule
multiply
muscle
museum
mushroom
music
must
mutual
myself
mystery
myth
naive
name
napkin
narrow
nasty
nation
nature
near
neck
need
negative
neglect
neither
nephew
nerve
nest
net
network
neutral
never
news
next
nice
night
noble
noise
nominee
noodle
normal
north
nose
notable
note
nothing
notice
novel
now
nuclear
number
nurse
nut
oak
obey
object
oblige
obscure
observe
obtain
obvious
occur
ocean
october
odor
off
offer
office
often
oil
okay
old
olive
olympic
omit
once
one
onion
online
only
open
opera
opinion
oppose
option
orange
orbit
orchard
order
ordinary
organ
orient
original
orphan
ostrich
other
outdoor
outer
output
outside
oval
oven
over
own
owner
oxygen
oyster
ozone
pact
paddle
page
pair
palace
palm
panda
panel
panic
panther
paper
parade
parent
park
parrot
party
pass
patch
path
patient
patrol
pattern
pause
pave
payment
peace
peanut
pear
peasant
pelican
pen
penalty
pencil
people
pepper
perfect
permit
person
pet
phone
photo
phrase
physical
piano
picnic
picture
piece
pig
pigeon
pill
pilot
pink
pioneer
pipe
pistol
pitch
pizza
place
planet
plastic
plate
play
please
pledge
pluck
plug
plunge
poem
poet
point
polar
pole
police
pond
pony
pool
popular
portion
position
possible
post
potato
pottery
poverty
powder
power
practice
praise
predict
prefer
prepare
present
pretty
prevent
price
pride
primary
print
priority
prison
private
prize
problem
process
produce
profit
program
project
promote
proof
property
prosper
protect
proud
provide
public
pudding
pull
pulp
pulse
pumpkin
punch
pupil
puppy
purchase
purity
purpose
purse
push
put
puzzle
pyramid
quality
quantum
quarter
question
quick
quit
quiz
quote
rabbit
raccoon
race
rack
radar
radio
rail
rain
raise
rally
ramp
ranch
random
range
rapid
rare
rate
rather
raven
raw
razor
ready
real
reason
rebel
rebuild
recall
receive
recipe
record
recycle
reduce
reflect
reform
refuse
region
regret
regular
reject
relax
release
relief
rely
remain
remember
remind
remove
render
renew
rent
reopen
repair
repeat
replace
report
require
rescue
resemble
resist
resource
response
result
retire
retreat
return
reunion
reveal
review
reward
rhythm
rib
ribbon
rice
rich
ride
ridge
rifle
right
rigid
ring
riot
ripple
risk
ritual
rival
river
road
roast
robot
robust
rocket
romance
roof
rookie
room
rose
rotate
rough
round
route
royal
rubber
rude
rug
rule
run
runway
rural
sad
saddle
sadness
safe
sail
salad
salmon
salon
salt
salute
same
sample
sand
satisfy
satoshi
sauce
sausage
save
say
scale
scan
scare
scatter
scene
scheme
school
science
scissors
scorpion
scout
scrap
screen
script
scrub
sea
search
season
seat
second
secret
section
security
seed
seek
segment
select
sell
seminar
senior
sense
sentence
series
service
session
settle
setup
seven
shadow
shaft
shallow
share
shed
shell
sheriff
shield
shift
shine
ship
shiver
shock
shoe
shoot
shop
short
shoulder
shove
shrimp
shrug
shuffle
shy
sibling
sick
side
siege
sight
sign
silent
silk
silly
silver
similar
simple
since
sing
siren
sister
situate
six
size
skate
sketch
ski
skill
skin
skirt
skull
slab
slam
sleep
slender
slice
slide
slight
slim
slogan
slot
slow
slush
small
smart
smile
smoke
smooth
snack
snake
snap
sniff
snow
soap
soccer
social
sock
soda
soft
solar
soldier
solid
solution
solve
someone
song
soon
sorry
sort
soul
sound
soup
source
south
space
spare
spatial
spawn
speak
special
speed
spell
spend
sphere
spice
spider
spike
spin
spirit
split
spoil
sponsor
spoon
sport
spot
spray
spread
spring
spy
square
squeeze
squirrel
stable
stadium
staff
stage
stairs
stamp
stand
start
state
stay
steak
steel
stem
step
stereo
stick
still
sting
stock
stomach
stone
stool
story
stove
strategy
street
strike
strong
struggle
student
stuff
stumble
style
subject
submit
subway
success
such
sudden
suffer
sugar
suggest
suit
summer
sun
sunny
sunset
super
supply
supreme
sure
surface
surge
surprise
surround
survey
suspect
sustain
swallow
swamp
swap
swarm
swear
sweet
swift
swim
swing
switch
sword
symbol
symptom
syrup
system
table
tackle
tag
tail
talent
talk
tank
tape
target
task
taste
tattoo
taxi
teach
team
tell
ten
tenant
tennis
tent
term
test
text
thank
that
theme
then
theory
there
they
thing
this
thought
three
thrive
throw
thumb
thunder
ticket
tide
tiger
tilt
timber
time
tiny
tip
tired
tissue
title
toast
tobacco
today
toddler
toe
together
toilet
token
tomato
tomorrow
tone
tongue
tonight
tool
tooth
top
topic
topple
torch
tornado
tortoise
toss
total
tourist
toward
tower
town
toy
track
trade
traffic
tragic
train
transfer
trap
trash
travel
tray
treat
tree
trend
trial
tribe
trick
trigger
trim
trip
trophy
trouble
truck
true
truly
trumpet
trust
truth
try
tube
tuition
tumble
tuna
tunnel
turkey
turn
turtle
twelve
twenty
twice
twin
twist
two
type
typical
ugly
umbrella
unable
unaware
uncle
uncover
under
undo
unfair
unfold
unhappy
uniform
unique
unit
universe
unknown
unlock
until
unusual
unveil
update
upgrade
uphold
upon
upper
upset
urban
urge
usage
use
used
useful
useless
usual
utility
vacant
vacuum
vague
valid
valley
valve
van
vanish
vapor
various
vast
vault
vehicle
velvet
vendor
venture
venue
verb
verify
version
very
vessel
veteran
viable
vibrant
vicious
victory
video
view
village
vintage
violin
virtual
virus
visa
visit
visual
vital
vivid
vocal
voice
void
volcano
volume
vote
voyage
wage
wagon
wait
walk
wall
walnut
want
warfare
warm
warrior
wash
wasp
waste
water
wave
way
wealth
weapon
wear
weasel
weather
web
wedding
weekend
weird
welcome
west
wet
whale
what
wheat
wheel
when
where
whip
whisper
wide
width
wife
wild
will
win
window
wine
wing
wink
winner
winter
wire
wisdom
wise
wish
witness
wolf
woman
wonder
wood
wool
word
work
world
worry
worth
wrap
wreck
wrestle
wrist
write
wrong
yard
year
yellow
you
young
youth
zebra
zero
zone
zoo
""".split())

SEED_WORD_COUNTS = [12, 15, 18, 21, 24]

# Logger class with flush method
class Logger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = open(log_file, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

os.makedirs(DESKTOP_PATH, exist_ok=True)
sys.stdout = Logger(CONSOLE_LOG_FILE)

def get_drives():
    """
    Detect available drives to scan.
    """
    if platform.system() == "Windows":
        import string
        return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    else:
        return [os.path.expanduser("~")]

def display_intro_and_select_drives():
    """
    Display introductory text and prompt the user to select drives to scan.
    """
    print("🔍 Welcome to Muffin's Treasure Hunting Tool!")
    print("🐾 Muffin is here to help sniff out crypto treasures!")
    print("\nWhat does this tool do?")
    print("🦴 Searches your drives for crypto wallets, keys, and related treasures.")
    print("📄 Scans files for sensitive data, including text, spreadsheets, images, and more.")
    print("📊 Exports results to both a text file and a spreadsheet.")
    print("\n🐶 Let’s get started! Muffin is ready to sniff out hidden treasures!")
    print("\n------------------------------------------------------------\n")

    # Detect drives
    drives = get_drives()
    if not drives:
        print("🚫 No drives detected. Exiting...")
        sys.exit(0)

    if platform.system() == "Windows":
        print(f"1. Type ALL to scan all of the 📂 Detected Drives: {' '.join(drives)}")
        print("2. Or type only drive letters you want to scan separated by spaces (e.g., C or C D or E).")
    else:
        print(f"📂 On this system, only the home directory can be scanned: {drives[0]}")

    print()  # Adds a blank line for better readability
    print("✨Type your answer and press Enter to continue:", flush=True)  # Ensures immediate display

    # User input for drive selection
    response = input().strip().upper()
    if platform.system() != "Windows":
        # For non-Windows systems, only home directory is scanned
        print("⚠️ On non-Windows systems, only the home directory is available for scanning.")
        return drives

    if response == "ALL":
        return drives
    else:
        selected_drives = []
        for d in response.split():
            drive = f"{d.upper()}:\\" if not d.endswith(":\\") else d.upper()
            if drive in drives:
                selected_drives.append(drive)
            else:
                print(f"🚫 Drive {d} is not a valid drive.")
        if not selected_drives:
            print("🚫 No valid drives selected. Exiting...")
            sys.exit(0)
        return selected_drives

def log_error(message):
    """
    Log errors to the error log file and print them to the console.
    """
    print(f"❌ {message}", flush=True)
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as error_log:
        error_log.write(f"{message}\n")

def is_valid_ethereum_address(file_name):
    """
    Check if a string in the file name is a valid Ethereum address.
    """
    return bool(re.search(r"\b0x[a-fA-F0-9]{40}\b", file_name))

def is_valid_bitcoin_key(file_name):
    """
    Check if a string in the file name is a valid Bitcoin address or key.
    """
    btc_regex = r"\b(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,62}\b"
    return bool(re.search(btc_regex, file_name))

def contains_json_wallet_structure(file_path):
    """
    Check if a JSON file contains wallet structure indicators.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return any(key in content for key in ["ciphertext", "cipherparams", "kdfparams", "mac", "address"])
    except Exception as e:
        log_error(f"Error reading JSON file {file_path}: {e}")
    return False

def scan_spreadsheet(file_path):
    """
    Scan a spreadsheet file for crypto-related keywords.
    """
    try:
        if file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if any(cell and any(keyword.lower() in str(cell).lower() for keyword in KEYWORDS_ICONS) for cell in row):
                        return True
        else:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            for sheet in workbook.sheetnames:
                ws = workbook[sheet]
                for row in ws.iter_rows(values_only=True):
                    if any(cell and any(keyword.lower() in str(cell).lower() for keyword in KEYWORDS_ICONS) for cell in row):
                        return True
    except Exception as e:
        log_error(f"Error reading spreadsheet {file_path}: {e}")
    return False

def detect_seed_phrase(content):
    """
    Detect potential seed phrases in the content.
    """
    words = re.findall(r'\b\w+\b', content.lower())
    for count in SEED_WORD_COUNTS:
        for i in range(len(words) - count + 1):
            word_sequence = words[i:i+count]
            if all(word in MNEMONIC_WORDLIST for word in word_sequence):
                return True
    return False

def search_file_content(file_path):
    """
    Search the content of a file for crypto-related keywords and seed phrases.
    """
    try:
        if file_path.endswith(".txt") or '.' not in os.path.basename(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if any(keyword.lower() in content.lower() for keyword in KEYWORDS_ICONS):
                    return True
                if detect_seed_phrase(content):
                    return True
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            content = "\n".join(full_text)
            if any(keyword.lower() in content.lower() for keyword in KEYWORDS_ICONS):
                return True
            if detect_seed_phrase(content):
                return True
        elif file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            full_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
            content = "\n".join(full_text)
            if any(keyword.lower() in content.lower() for keyword in KEYWORDS_ICONS):
                return True
            if detect_seed_phrase(content):
                return True
    except Exception as e:
        log_error(f"Error processing file {file_path}: {e}")
    return False

def search_files(drive):
    """
    Recursively searches the specified drive for files matching crypto-related keywords.
    """
    found_items = []
    print(f"🔍 Searching drive {drive}...", flush=True)

    # Normalize the drive letter to lower case for consistent comparison
    drive_letter = os.path.splitdrive(drive)[0].lower()

    # Filter EXCLUDED_PATHS to include only those on the same drive
    excluded_paths_on_same_drive = [
        os.path.abspath(excluded) for excluded in EXCLUDED_PATHS
        if os.path.splitdrive(excluded)[0].lower() == drive_letter
    ]

    for root, dirs, files in os.walk(drive, topdown=True, followlinks=False):
        normalized_root = os.path.abspath(root)

        # Exclude specified folders
        dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_FOLDERS]

        # Check if the current root is within any excluded paths
        exclude = False
        for excluded in excluded_paths_on_same_drive:
            if normalized_root.lower().startswith(excluded.lower()):
                exclude = True
                break
        if exclude:
            continue

        print(f"📂 Scanning directory: {root}", flush=True)
        for file in files:
            file_path = os.path.join(root, file)
            file_name = file
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in IGNORED_EXTENSIONS:
                continue

            keyword_matches = [kw for kw in KEYWORDS_ICONS if kw.lower() in file_name.lower()]

            if "0x" in keyword_matches and not is_valid_ethereum_address(file_name):
                keyword_matches.remove("0x")
            if is_valid_bitcoin_key(file_name):
                keyword_matches.append("bitcoin_key")
            if file_extension == ".json" and contains_json_wallet_structure(file_path):
                keyword_matches.append("json_wallet")
            if file_extension in [".xlsx", ".xls", ".csv"] and scan_spreadsheet(file_path):
                keyword_matches.append("spreadsheet_content")
            if (not keyword_matches and (file_extension in [".txt", ".docx", ".pdf"] or '.' not in file_name)):
                if search_file_content(file_path):
                    keyword_matches.append("content_match")

            # Include images with keywords in filenames
            if file_extension in [".png", ".jpg", ".jpeg", ".gif"]:
                if any(kw.lower() in file_name.lower() for kw in KEYWORDS_ICONS):
                    keyword_matches.append("image_keyword_match")

            if keyword_matches:
                icon = KEYWORDS_ICONS.get(keyword_matches[0], "📄")
                main_folder = (
                    normalized_root.split(os.sep)[2] if normalized_root.startswith(f"{drive}Users") and len(normalized_root.split(os.sep)) > 2
                    else normalized_root.split(os.sep)[1] if len(normalized_root.split(os.sep)) > 1 else normalized_root
                )
                main_folder = main_folder if main_folder.lower() not in ["program files", "windows"] else normalized_root.split(os.sep)[2] if len(normalized_root.split(os.sep)) > 2 else normalized_root

                found_items.append({
                    "Drive": drive[0],
                    "Main Folder": main_folder,
                    "Keyword Match": ", ".join(keyword_matches),
                    "File Extension": file_extension,
                    "File Name": file_name,
                    "File Path": file_path,
                })
                print(f"{icon} Found: {file_name}", flush=True)
    return found_items

def export_results(found_items):
    """
    Export the search results to a text file and an Excel spreadsheet.
    """
    text_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Path_Log.txt")
    excel_file = os.path.join(DESKTOP_PATH, "Muffins_Treasure_Hunt_Results.xlsx")

    with open(text_file, "w", encoding="utf-8") as txt:
        txt.write("🔍 Muffin's Treasure Hunt Results\n")
        txt.write(f"🏆 Total treasures found: {len(found_items)}\n\n")
        for item in found_items:
            txt.write(f"Drive: {item['Drive']} | Folder: {item['Main Folder']} | File: {item['File Name']} | Path: {item['File Path']}\n")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Muffin's Results"

    headers = ["Drive", "Main Folder", "Keyword Match", "File Extension", "File Name", "File Path"]
    for col, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    sheet.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    for row_num, item in enumerate(found_items, start=2):
        sheet.cell(row=row_num, column=1, value=item["Drive"])
        sheet.cell(row=row_num, column=2, value=item["Main Folder"])
        sheet.cell(row=row_num, column=3, value=item["Keyword Match"])
        sheet.cell(row=row_num, column=4, value=item["File Extension"])
        sheet.cell(row=row_num, column=5, value=item["File Name"])
        path_cell = sheet.cell(row=row_num, column=6, value=item["File Path"])
        # Create hyperlink to the file path
        if platform.system() == "Windows":
            path_cell.hyperlink = f"file:///{item['File Path'].replace(os.sep, '/')}"
        else:
            path_cell.hyperlink = f"file://{item['File Path']}"

    for col in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col)].width = 25

    workbook.save(excel_file)

    print("\n🎉 Export Complete!")
    print(f"📄 Text File: {text_file}")
    print(f"📊 Spreadsheet: {excel_file}")
    print(f"🏆 Total treasures found: {len(found_items)} 🐾", flush=True)

def muffins_treasure_hunt():
    """
    Main function to run Muffin's Treasure Hunt.
    """
    start_time = time.time()
    selected_drives = display_intro_and_select_drives()
    all_found_items = []
    for drive in selected_drives:
        found_items = search_files(drive)
        all_found_items.extend(found_items)
    export_results(all_found_items)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\n⏰ Total time taken: {total_time:.2f} seconds")
    print("\n🐶 Muffin's hunt is complete! Happy treasure hunting! 🦴", flush=True)

if __name__ == "__main__":
    try:
        muffins_treasure_hunt()
    except KeyboardInterrupt:
        print("\n🛑 Scan interrupted by user. Exiting gracefully.", flush=True)
