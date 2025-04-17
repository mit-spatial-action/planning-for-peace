import pandas as pd
import re
from collections import Counter
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords
nltk.download('stopwords')

# Load the Excel file
FILE_PATH = "/path/to/exported.results"

# Initialize translator (using `deep_translator` instead of `googletrans`)
def translate_text(text):
    try:
        # Translate text to English
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text  # Return original text if translation fails


df = pd.read_excel(FILE_PATH)

# Define a comprehensive set of stopwords
STOPWORDS = set(stopwords.words('english')).union({
    "reparation", "reparations", "study", "research", "paper", "article", "analysis", "discussion"
})

# Clean the text by removing special characters and converting to lowercase
def clean_text(text):
    if not isinstance(text, str):  # Handle non-string inputs
        return ""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    return text

# Apply cleaning and translation to the 'Summary' column (previously 'Description')
df['Summary'] = df['Summary'].dropna().apply(clean_text).apply(translate_text)

# Ensure 'Summary' values are strings
df['Summary'] = df['Summary'].astype(str)

# Define a list of geographical regions and case studies related to reparations

# ----------------------------------------------------------------------------------------------------------------

geographical_keywords = [
    # Americas
    # Comprehensive list of Americas regions, historical terms, and reparations-related search terms

    # North America
    "united states", "usa", "america", "thirteen colonies",
    "confederate states", "union states", "reconstruction era",
    "jim crow", "civil rights movement", "indian territory",
    "alaska native claims", "hawaii kingdom", "mexican cession",

    "canada", "british north america", "upper canada", "lower canada",
    "northwest territories", "nunavut", "first nations", "métis",
    "inuit", "residential schools", "sixties scoop",

    "mexico", "new spain", "mexican empire", "porfiriato",
    "ejido system", "hacienda system", "mexican revolution",

    # Caribbean
    "cuba", "spanish cuba", "american occupation",
    "dominican republic", "santo domingo", "española",
    "haiti", "saint-domingue", "haitian revolution",

    "jamaica", "british jamaica", "spanish jamaica",
    "maroon communities", "accompong", "moore town",

    "trinidad and tobago", "british trinidad", "spanish trinidad",
    "barbados", "british barbados", "little england",
    "bahamas", "british bahamas", "lucayan archipelago",

    "antigua and barbuda", "british leeward islands",
    "dominica", "french dominica", "british dominica",
    "grenada", "french grenada", "british grenada",
    "saint lucia", "french saint lucia", "british saint lucia",
    "saint vincent", "grenadines", "british windward islands",
    "saint kitts and nevis", "federation", "anguilla",

    # Central America
    "belize", "british honduras", "maya civilization",
    "costa rica", "spanish costa rica", "united provinces",
    "el salvador", "cuzcatlán", "federal republic",
    "guatemala", "captaincy general", "mayan states",
    "honduras", "spanish honduras", "banana republics",
    "nicaragua", "mosquito coast", "central american federation",
    "panama", "gran colombia", "panama canal zone",

    # South America
    "argentina", "viceroyalty of río de la plata", "pampas",
    "patagonia", "tierra del fuego", "conquest of the desert",

    "bolivia", "upper peru", "potosí", "silver mining",
    "brazil", "portuguese brazil", "empire of brazil",
    "quilombos", "palmares", "rubber boom",

    "chile", "captaincy general", "mapuche territory",
    "wallmapu", "araucanía", "pacification",

    "colombia", "new granada", "gran colombia",
    "palenques", "san basilio", "pacific coast",

    "ecuador", "kingdom of quito", "royal audience",
    "peru", "inca empire", "viceroyalty of peru",
    "tahuantinsuyu", "spanish peru", "guano era",

    "paraguay", "jesuit reductions", "guarani missions",
    "uruguay", "banda oriental", "cisplatine province",
    "venezuela", "captaincy general", "great colombia",

    "guyana", "british guiana", "dutch guiana",
    "suriname", "dutch guiana", "maroon societies",
    "french guiana", "cayenne", "penal colony",

    # Indigenous Peoples & Nations
    "first nations", "métis", "inuit", "alaska natives",
    "american indians", "native americans", "indigenous peoples",

    "navajo nation", "diné", "cherokee nation",
    "lakota", "dakota", "nakota", "sioux",
    "apache", "comanche", "iroquois confederacy",
    "haudenosaunee", "mohawk", "oneida", "onondaga",
    "cayuga", "seneca", "tuscarora",

    "maya peoples", "k'iche'", "q'eqchi'", "kaqchikel",
    "aztec", "mexica", "nahua peoples", "toltec",
    "zapotec", "mixtec", "tarascan state",

    "inca", "quechua", "aymara", "guarani",
    "mapuche", "tehuelche", "selk'nam", "atacameño",

    "taíno", "arawak", "carib", "garifuna",
    "kalina", "lokono", "warao", "yanomami",

    # Historical Events & Atrocities
    "trail of tears", "indian removal", "forced relocation",
    "wounded knee massacre", "sand creek massacre",
    "residential schools", "boarding schools", "sixties scoop",

    "conquest of the desert", "pacification of araucanía",
    "rubber boom atrocities", "putumayo atrocities",

    "slavery", "transatlantic slave trade", "middle passage",
    "plantation system", "slave codes", "slave patrols",

    "haitian revolution", "maroon wars", "quilombo wars",
    "caste war of yucatán", "caste war of chan santa cruz",

    # Reparations-Specific Terms
    "slavery reparations", "indigenous reparations",
    "land restitution", "treaty rights", "land claims",
    "tribal sovereignty", "self-determination",

    "h.r. 40", "commission to study reparation proposals",
    "rosewood reparations", "tulsa race massacre reparations",

    "truth and reconciliation commission", "residential schools settlement",
    "sixties scoop settlement", "day scholars settlement",

    "caricom reparations commission", "reparatory justice",
    "ten point plan", "caribbean reparations",

    "quilombo land rights", "collective land titles",
    "indigenous land demarcation", "ancestral territories",

    # Legal & Political Terms
    "treaties", "indian treaties", "numbered treaties",
    "peace and friendship treaties", "robinson treaties",
    "douglas treaties", "williams treaties",

    "indian claims commission", "specific claims",
    "comprehensive claims", "land claims agreements",
    "modern treaties", "self-government agreements",

    "aboriginal title", "indigenous title", "native title",
    "tribal sovereignty", "reserved rights", "usufruct rights",

    "inter-american court", "human rights court",
    "oas", "organization of american states",

    # Organizations & Movements
    "national coalition of blacks for reparations in america",
    "n'cobra", "national african american reparations commission",

    "assembly of first nations", "congress of aboriginal peoples",
    "inuit tapiriit kanatami", "métis national council",

    "american indian movement", "idle no more",
    "zapatista movement", "ejército zapatista",

    "black lives matter", "movement for black lives",
    "reparations movement", "land back movement",

    # Contemporary Issues
    "environmental justice", "climate reparations",
    "resource extraction", "mining rights", "water rights",

    "cultural repatriation", "artifact return",
    "sacred objects", "ancestral remains",
    "museum restitution", "nagpra",

    "language revitalization", "cultural preservation",
    "traditional knowledge", "indigenous education",

    # Economic Terms
    "slave economy", "plantation economy",
    "extractive economy", "dependency theory",
    "neocolonialism", "structural adjustment",

    "tribal gaming", "resource revenue sharing",
    "impact benefit agreements", "modern treaties",

    "haiti independence debt", "guano bonds",
    "external debt", "odious debt", "sovereign debt",

    # Documentation & Memory
    "oral history", "oral tradition", "storytelling",
    "traditional knowledge", "indigenous knowledge",
    "cultural memory", "collective memory",

    "slave narratives", "wpa slave narratives",
    "underground railroad", "freedom narratives",

    "truth commissions", "historical commissions",
    "memory projects", "documentation centers",
    "memorial sites", "museums"

# ----------------------------------------------------------------------------------------------------------------

    # Europe
   # Comprehensive list of European regions, historical terms, and reparations-related search terms

    # Western Europe
    "france", "french republic", "vichy france", "free france", "french empire",
    "french colonial empire", "french west africa", "french equatorial africa",
    "french indochina", "french algeria", "french protectorate",

    "germany", "german reich", "weimar republic", "nazi germany", "third reich",
    "federal republic", "german democratic republic", "prussia",
    "german empire", "german colonial empire", "german east africa",
    "german south west africa", "german new guinea",

    "united kingdom", "great britain", "british empire", "commonwealth",
    "england", "scotland", "wales", "northern ireland",
    "british raj", "british west indies", "british africa",
    "british mandate", "british protectorate",

    "netherlands", "dutch republic", "dutch east indies",
    "dutch west indies", "dutch gold coast", "dutch empire",
    "kingdom of netherlands", "benelux",

    "belgium", "belgian congo", "belgian empire", "congo free state",
    "ruanda-urundi", "kingdom of belgium", "flemish region", "walloon region",

    # Northern Europe
    "denmark", "danish empire", "danish west indies", "greenland",
    "faroe islands", "danish colonial empire",

    "norway", "kingdom of norway", "norwegian empire",
    "union with sweden", "german occupation",

    "sweden", "swedish empire", "great power era",
    "swedish colonial empire", "new sweden",

    "finland", "grand duchy of finland", "finnish civil war",
    "winter war", "continuation war", "lapland war",

    # Southern Europe
    "spain", "spanish empire", "spanish colonial empire",
    "spanish east indies", "spanish west indies", "spanish africa",
    "francoist spain", "second republic",

    "portugal", "portuguese empire", "portuguese colonial empire",
    "portuguese india", "portuguese africa", "portuguese timor",
    "estado novo", "carnation revolution",

    "italy", "italian empire", "italian colonial empire",
    "italian east africa", "italian libya", "italian somalia",
    "fascist italy", "kingdom of italy",

    "greece", "hellenic republic", "kingdom of greece",
    "ottoman greece", "axis occupation", "greek civil war",

    # Eastern Europe
    "poland", "polish-lithuanian commonwealth", "partitioned poland",
    "second polish republic", "general government", "people's republic",

    "russia", "russian empire", "soviet union", "ussr",
    "russian federation", "russian sphere of influence",

    "ukraine", "ukrainian ssr", "ukrainian people's republic",
    "holodomor", "soviet occupation", "german occupation",

    "belarus", "byelorussian ssr", "belarusian people's republic",
    "soviet occupation", "german occupation",

    # Central Europe
    "austria", "austro-hungarian empire", "habsburg monarchy",
    "first republic", "federal state", "german austria",

    "hungary", "kingdom of hungary", "austria-hungary",
    "hungarian soviet republic", "people's republic",

    "czechoslovakia", "czech republic", "slovakia",
    "first republic", "protectorate", "federal republic",

    # Balkans
    "yugoslavia", "kingdom of yugoslavia", "socialist yugoslavia",
    "serbia", "croatia", "slovenia", "bosnia", "montenegro",
    "macedonia", "kosovo",

    # Historical Events & Atrocities
    "holocaust", "shoah", "final solution", "concentration camps",
    "death camps", "forced labor camps", "ghettos",
    "nuremberg trials", "denazification", "aryanization",

    "armenian genocide", "greek genocide", "assyrian genocide",
    "pontic genocide", "great catastrophe", "death marches",

    "porajmos", "roma genocide", "sinti persecution",
    "romani holocaust", "gypsy persecution",

    "holodomor", "ukrainian famine", "soviet famines",
    "dekulakization", "collectivization",

    "colonial atrocities", "congo free state", "herero genocide",
    "maji maji rebellion", "italian libya", "french algeria",

    "balkan wars", "yugoslav wars", "bosnian war",
    "croatian war", "kosovo war", "ethnic cleansing",

    # World War Related
    "world war i", "wwi", "great war", "versailles treaty",
    "war reparations", "war debt", "occupation costs",

    "world war ii", "wwii", "second world war",
    "axis occupation", "collaboration", "resistance",
    "forced labor", "slave labor", "war crimes",

    # Reparations-Specific Terms
    "wiedergutmachung", "restitution", "compensation",
    "indemnification", "luxembourg agreements",
    "claims conference", "article 2 fund",

    "colonial reparations", "slavery reparations",
    "indigenous reparations", "cultural restitution",
    "art restitution", "land restitution",

    "war reparations", "occupation reparations",
    "forced labor compensation", "victim compensation",
    "property restitution", "bank accounts",

    # Legal & Political Terms
    "washington agreement", "london debt agreement",
    "2+4 treaty", "peace treaties", "bilateral agreements",

    "class action", "collective claims", "individual claims",
    "property claims", "insurance claims", "bank claims",

    "statute of limitations", "legal barriers",
    "sovereign immunity", "state responsibility",
    "universal jurisdiction",

    # Organizations & Institutions
    "claims conference", "jewish claims conference",
    "world jewish congress", "world jewish restitution organization",

    "european union", "council of europe", "european court",
    "united nations", "international court of justice",

    "restitution committees", "compensation funds",
    "reconciliation foundations", "memorial foundations",

    # Cultural Property
    "nazi-looted art", "degenerate art", "art restitution",
    "cultural property", "museum collections",
    "provenance research", "washington principles",

    "colonial artifacts", "benin bronzes", "museum returns",
    "cultural heritage", "indigenous artifacts",

    # Contemporary Issues
    "historical memory", "memory politics", "commemoration",
    "memorial sites", "documentation centers",

    "truth commissions", "reconciliation commissions",
    "historical commissions", "expert commissions",

    "transitional justice", "historical justice",
    "restorative justice", "victim recognition",

    # Economic Terms
    "marshall plan", "economic reconstruction",
    "development aid", "technical assistance",
    "bilateral cooperation",

    "frozen assets", "blocked accounts", "dormant accounts",
    "unclaimed property", "heirless property",

    # Additional Terms
    "forced migration", "population transfer", "ethnic cleansing",
    "refugee compensation", "displaced persons",

    "slave labor", "forced labor", "conscript labor",
    "labor battalions", "prisoner labor",

    "property seizure", "aryanization", "nationalization",
    "expropriation", "confiscation",

    # Victim Groups
    "holocaust survivors", "second generation",
    "third generation", "survivor organizations",

    "roma and sinti", "slavic peoples", "jews",
    "political prisoners", "resistance members",

    "colonial subjects", "indigenous peoples",
    "enslaved peoples", "forced laborers",

    # Documentation & Memory
    "oral history", "survivor testimony", "witness accounts",
    "historical documentation", "archives",
    "memorial sites", "museums", "documentation centers",

    # Modern Movements
    "restitution movement", "reparations movement",
    "decolonization movement", "memory activism",
    "historical justice movement"

# ----------------------------------------------------------------------------------------------------------------

    # Africa
   # Comprehensive list of African regions, historical terms, and reparations-related search terms

    # North Africa
    "egypt", "ancient egypt", "ptolemaic egypt", "roman egypt", "fatimid caliphate",
    "mamluk sultanate", "ottoman egypt", "muhammad ali dynasty", "british egypt",
    "arab republic of egypt", "united arab republic",

    "libya", "ottoman libya", "italian libya", "cyrenaica", "tripolitania", "fezzan",
    "kingdom of libya", "jamahiriya", "great socialist people's libyan arab jamahiriya",

    "tunisia", "carthage", "ottoman tunisia", "french protectorate", "husainid dynasty",
    "republic of tunisia", "habib bourguiba", "ben ali regime",

    "algeria", "french algeria", "ottoman algeria", "regency of algiers",
    "national liberation front", "war of independence", "pied-noirs",

    "morocco", "alaouite dynasty", "french protectorate", "spanish protectorate",
    "kingdom of morocco", "western sahara", "spanish sahara", "rio de oro",

    # West Africa
    "mali", "mali empire", "french sudan", "french soudan", "mande empire",
    "songhai empire", "wassoulou empire", "bambara empire", "toucouleur empire",
    "french west africa", "afrique occidentale française",

    "nigeria", "british nigeria", "northern nigeria protectorate",
    "southern nigeria protectorate", "colony and protectorate of nigeria",
    "biafra", "sokoto caliphate", "benin empire", "oyo empire", "bornu empire",

    "ghana", "gold coast", "british gold coast", "ashanti empire", "asante kingdom",
    "fante confederacy", "nzema kingdom", "ga-dangme states",

    "senegal", "french senegal", "four communes", "wolof empire", "jolof empire",
    "waalo kingdom", "cayor kingdom", "baol kingdom",

    "ivory coast", "cote d'ivoire", "french ivory coast", "kong empire",
    "gyaaman", "indenie kingdom", "sanwi kingdom",

    "burkina faso", "upper volta", "haute volta", "mossi kingdoms",
    "french upper volta", "thomas sankara regime",

    "guinea", "french guinea", "wassoulou empire", "futa jallon",
    "kaabu empire", "nalu kingdom", "landuma kingdom",

    "sierra leone", "british sierra leone", "sierra leone colony",
    "sierra leone protectorate", "temne kingdom", "mende kingdom",

    "liberia", "american colonization society", "commonwealth of liberia",
    "americo-liberians", "indigenous peoples", "doe regime", "taylor regime",

    # East Africa
    "ethiopia", "abyssinia", "italian east africa", "british occupation",
    "derg regime", "zemene mesafint", "solomonic dynasty", "italian invasion",

    "somalia", "british somaliland", "italian somaliland", "french somaliland",
    "trust territory", "ajuran sultanate", "adal sultanate", "warsangali sultanate",
    "majeerteen sultanate", "hobyo sultanate", "dervish state",

    "kenya", "british east africa", "east africa protectorate",
    "kenya colony", "mau mau uprising", "kikuyu central association",

    "uganda", "buganda kingdom", "bunyoro kingdom", "toro kingdom",
    "ankole kingdom", "british uganda", "busoga kingdom",

    "tanzania", "tanganyika", "zanzibar", "german east africa",
    "british tanganyika", "maji maji rebellion", "nyamwezi kingdom",

    # Central Africa
    "democratic republic of the congo", "belgian congo", "congo free state",
    "zaire", "katanga", "south kasai", "kongo kingdom", "luba empire",
    "lunda empire", "yeke kingdom",

    "angola", "portuguese angola", "portuguese west africa",
    "kongo kingdom", "ndongo kingdom", "matamba kingdom", "mpla",
    "unita", "civil war", "luena memorandum",

    "cameroon", "german kamerun", "french cameroun", "british cameroons",
    "bamum kingdom", "bamileke kingdoms", "fulbe kingdom",

    "chad", "french chad", "bornu empire", "wadai empire", "bagirmi kingdom",
    "ennedi kingdom", "tibesti kingdom",

    # Southern Africa
    "south africa", "union of south africa", "cape colony", "natal colony",
    "orange free state", "transvaal republic", "boer republics",
    "apartheid", "bantustans", "homelands",

    "zimbabwe", "southern rhodesia", "rhodesia", "british south africa company",
    "great zimbabwe", "mutapa empire", "rozwi empire", "ndebele kingdom",

    "mozambique", "portuguese east africa", "portuguese mozambique",
    "gaza empire", "maravi confederation", "frelimo", "renamo",

    "namibia", "german south west africa", "south west africa",
    "mandate territory", "swapo", "herero", "nama",

    # Colonial Powers & Systems
    "british empire", "french empire", "portuguese empire", "belgian empire",
    "german empire", "italian empire", "spanish empire",
    "colonial administration", "indirect rule", "direct rule",
    "settler colonialism", "colonial borders", "berlin conference",

    # Historical Events & Atrocities
    "herero and nama genocide", "maji maji rebellion", "mau mau uprising",
    "algerian war", "congo free state atrocities", "apartheid crimes",
    "gukurahundi", "rwandan genocide", "burundi genocide",
    "darfur genocide", "biafran war", "first congo war", "second congo war",

    # Slavery & Slave Trade
    "transatlantic slave trade", "arab slave trade", "east african slave trade",
    "internal african slave trade", "slave coast", "slave ports",
    "slave markets", "slave routes", "middle passage",
    "slave castles", "door of no return", "gorée island",
    "elmina castle", "cape coast castle", "christiansborg castle",

    # Liberation & Independence
    "african nationalism", "pan-africanism", "uhuru movement",
    "independence movements", "decolonization", "liberation struggles",
    "armed struggle", "guerrilla warfare", "national liberation",

    # Reparations-Specific Terms
    "colonial reparations", "slavery reparations", "genocide reparations",
    "apartheid reparations", "war crime reparations", "atrocity reparations",
    "land restitution", "asset return", "cultural property return",
    "art repatriation", "human remains repatriation",

    # Truth & Reconciliation
    "truth commission", "reconciliation commission", "truth and reconciliation",
    "transitional justice", "historical justice", "restorative justice",
    "memorial commission", "historical memory", "collective memory",

    # Legal & Political Terms
    "class action", "group claims", "collective reparations",
    "individual reparations", "symbolic reparations", "material reparations",
    "compensation", "restitution", "rehabilitation",
    "satisfaction", "guarantees of non-repetition",

    # Organizations & Institutions
    "african union", "organization of african unity",
    "economic community of west african states", "ecowas",
    "southern african development community", "sadc",
    "east african community", "eac",
    "intergovernmental authority on development", "igad",
    "arab maghreb union", "amu",

    # Contemporary Issues
    "land reform", "redistribution", "economic justice",
    "resource nationalism", "sovereign wealth", "development rights",
    "environmental justice", "climate reparations", "ecological debt",

    # Cultural & Social Terms
    "cultural heritage", "traditional knowledge", "indigenous rights",
    "customary law", "traditional authorities", "community rights",
    "ancestral lands", "sacred sites", "burial grounds",

    # Economic Terms
    "colonial debt", "odious debt", "structural adjustment",
    "economic exploitation", "resource extraction", "mineral rights",
    "land grabbing", "agricultural colonialism", "labor exploitation",

    # Additional Historical Terms
    "scramble for africa", "partition of africa", "spheres of influence",
    "protectorates", "mandates", "trust territories",
    "colonial charters", "royal charters", "concession companies",

    # Modern Political Movements
    "black lives matter", "rhodes must fall", "fees must fall",
    "anti-colonial movement", "decolonial movement", "land back movement",
    "restitution movement", "reparations movement",

    # Specific Claims & Cases
    "mau mau compensation", "herero reparations case",
    "apartheid litigation", "khulumani support group",
    "bristol slavery reparations", "caribbean reparations claims",
    "benin bronzes restitution", "ethiopia treasures return",

    # International Law & Policy
    "un declaration", "african charter", "human rights law",
    "international criminal law", "humanitarian law",
    "universal jurisdiction", "state responsibility",

    # Documentation & Memory
    "oral history", "living memory", "survivor testimony",
    "historical documentation", "archives", "memory projects",
    "memorial sites", "museums", "heritage sites"

# ----------------------------------------------------------------------------------------------------------------

    # Asia
    # Comprehensive list of Asian regions, historical terms, and reparations-related search terms

    # East Asia
    "china", "chinese", "republic of china", "people's republic of china", "manchuria", "manchukuo",
    "qing dynasty", "ming dynasty", "yuan dynasty", "tang dynasty", "han dynasty",
    "warlord period", "beiyang government", "nationalist china", "kuomintang", "kmt",
    "tibet", "xinjiang", "inner mongolia", "outer mongolia", "guangxi", "ningxia",

    "japan", "japanese", "imperial japan", "state of japan", "empire of japan",
    "meiji", "taisho", "showa", "heisei", "reiwa",
    "bakufu", "tokugawa", "shogunate", "daimyo",
    "ryukyu kingdom", "okinawa", "bonin islands", "kuril islands",

    "korea", "north korea", "south korea", "dprk", "rok", "joseon", "chosen",
    "goryeo", "silla", "baekje", "goguryeo", "three kingdoms",
    "korean empire", "great han empire", "provisional government",

    "taiwan", "formosa", "chinese taipei", "republic of taiwan",
    "japanese taiwan", "dutch formosa", "spanish formosa",

    "hong kong", "british hong kong", "new territories", "kowloon",
    "macau", "portuguese macau", "aomen",

    "mongolia", "inner mongolia", "outer mongolia", "mongolian people's republic",
    "dzungar empire", "bogd khanate", "yuan dynasty",

    # Southeast Asia
    "vietnam", "north vietnam", "south vietnam", "democratic republic of vietnam", "republic of vietnam",
    "french indochina", "tonkin", "annam", "cochinchina", "dai viet", "dai nam",
    "nguyen dynasty", "tay son dynasty", "champa", "dai co viet",

    "cambodia", "kampuchea", "khmer republic", "democratic kampuchea",
    "french protectorate", "khmer empire", "angkor empire", "funan", "chenla",

    "laos", "lan xang", "french laos", "kingdom of laos", "pathet lao",
    "luang prabang", "vientiane", "champasak",

    "thailand", "siam", "sukhothai", "ayutthaya", "thonburi", "rattanakosin",
    "lan na", "pattani", "monthon",

    "myanmar", "burma", "british burma", "union of burma", "socialist burma",
    "konbaung dynasty", "toungoo dynasty", "pagan kingdom", "ava kingdom",
    "arakan", "rakhine", "shan states", "karenni states",

    "malaysia", "malaya", "british malaya", "straits settlements",
    "federated malay states", "unfederated malay states", "north borneo",
    "sarawak", "malacca sultanate", "johor sultanate", "kedah sultanate",

    "singapore", "syonan-to", "temasek", "british singapore",

    "indonesia", "dutch east indies", "netherlands east indies", "netherlands india",
    "majapahit", "srivijaya", "mataram sultanate", "aceh sultanate",
    "dutch colony", "voc", "portuguese east indies", "british east indies",

    "philippines", "spanish east indies", "commonwealth of the philippines",
    "american philippines", "japanese philippines", "las islas filipinas",
    "pre-colonial barangay", "sultanate of sulu", "sultanate of maguindanao",

    "brunei", "brunei darussalam", "british protectorate brunei",
    "timor-leste", "east timor", "portuguese timor", "indonesian east timor",

    # South Asia
    "india", "british india", "british raj", "east india company",
    "mughal empire", "maratha empire", "vijayanagara empire",
    "maurya empire", "gupta empire", "delhi sultanate",
    "princely states", "french india", "portuguese india",
    "bengal presidency", "madras presidency", "bombay presidency",

    "pakistan", "east pakistan", "west pakistan", "dominion of pakistan",
    "bengal partition", "partition of india", "radcliffe line",

    "bangladesh", "east bengal", "bengal presidency", "bengal sultanate",

    "sri lanka", "ceylon", "british ceylon", "dutch ceylon", "portuguese ceylon",
    "kingdom of kandy", "jaffna kingdom", "anuradhapura", "polonnaruwa",

    "nepal", "kingdom of nepal", "shah dynasty", "rana dynasty",
    "bhutan", "druk yul", "british bhutan", "sikkim", "british sikkim",

    "maldives", "british maldives", "sultanate of maldives", "portuguese maldives",

    # Central Asia
    "kazakhstan", "kazakh ssr", "kazakh khanate", "alash autonomy",
    "uzbekistan", "uzbek ssr", "khanate of khiva", "khanate of kokand",
    "turkmenistan", "turkmen ssr", "transcaspia",
    "kyrgyzstan", "kirghiz ssr", "kyrgyz khanate",
    "tajikistan", "tajik ssr", "emirate of bukhara",
    "soviet central asia", "turkestan", "russian turkestan",
    "transoxiana", "sogdiana", "bactria", "margiana",

    # West Asia / Middle East
    "afghanistan", "durrani empire", "hotaki dynasty", "ghaznavid empire",
    "ghurids", "timurid empire", "afghan emirate", "afghan kingdom",

    "iran", "persia", "qajar dynasty", "pahlavi dynasty", "safavid empire",
    "achaemenid empire", "sassanid empire", "parthian empire",
    "elam", "media", "british iran", "soviet iran",

    "iraq", "mesopotamia", "british mesopotamia", "ottoman iraq",
    "babylonia", "assyria", "sumer", "akkad", "british mandate",
    "hashemite kingdom", "republic of iraq", "ba'athist iraq",

    "syria", "french mandate", "umayyad caliphate", "ayyubid dynasty",
    "lebanon", "greater lebanon", "ottoman lebanon", "french lebanon",
    "phoenicia", "crusader states",

    "jordan", "transjordan", "emirate of transjordan", "british mandate",

    "palestine", "british palestine", "ottoman palestine", "mandatory palestine",
    "israel", "state of israel", "british mandate palestine",

    "saudi arabia", "arabia", "hejaz", "nejd", "kingdom of hejaz",
    "rashidun caliphate", "first saudi state", "second saudi state",

    "yemen", "north yemen", "south yemen", "yemen arab republic",
    "people's democratic republic of yemen", "himyarite kingdom",
    "ottoman yemen", "british aden", "aden protectorate",

    "oman", "muscat and oman", "sultanate of muscat", "imamate of oman",
    "portuguese oman", "british oman",

    "united arab emirates", "uae", "trucial states", "trucial oman",
    "trucial coast", "pirate coast", "british protectorate",

    "qatar", "ottoman qatar", "british qatar", "al thani dynasty",
    "kuwait", "british kuwait", "ottoman kuwait", "al sabah dynasty",
    "bahrain", "british bahrain", "portuguese bahrain", "al khalifa dynasty",

    "turkey", "ottoman empire", "asia minor", "anatolia", "sublime porte",
    "seljuk empire", "byzantine empire", "roman empire", "hittite empire",

    # Pacific Islands
    "papua new guinea", "british new guinea", "german new guinea",
    "territory of papua", "territory of new guinea", "dutch new guinea",

    "fiji", "british fiji", "kingdom of fiji", "colony of fiji",
    "solomon islands", "british solomon islands", "german solomon islands",
    "vanuatu", "new hebrides", "french new hebrides", "british new hebrides",

    "samoa", "western samoa", "german samoa", "american samoa",
    "tonga", "friendly islands", "british protected state",

    "kiribati", "gilbert islands", "british gilbert islands",
    "marshall islands", "german marshall islands", "japanese mandate",
    "micronesia", "caroline islands", "trust territory",

    "palau", "british palau", "german palau", "spanish east indies",
    "nauru", "pleasant island", "german nauru", "british nauru",
    "tuvalu", "ellice islands", "british colony",

    # Historical Events & Specific Incidents
    "comfort women", "military comfort women", "sexual slavery",
    "forced labor", "slave labor", "romusha", "coolie", "indentured servitude",
    "conscripted labor", "forced mobilization", "labor conscription",

    "unit 731", "unit 100", "biological warfare", "chemical warfare",
    "human experimentation", "medical experimentation",

    "nanking massacre", "rape of nanking", "nanjing massacre",
    "manila massacre", "bataan death march", "sandakan death marches",
    "sook ching massacre", "bangkok massacre",

    "atomic bombings", "hiroshima", "nagasaki", "nuclear weapons",
    "firebombing", "conventional bombing", "civilian casualties",

    "POW", "prisoner of war", "internment camps", "concentration camps",
    "civilian internment", "death railway", "burma railway",

    "great famine", "bengal famine", "chinese famine", "vietnam famine",
    "holodomor", "kazakh famine", "great leap forward",

    "cultural revolution", "red guards", "struggle sessions",
    "anti-rightist campaign", "hundred flowers campaign",

    "killing fields", "khmer rouge", "democratic kampuchea",
    "year zero", "s-21", "tuol sleng", "choeung ek",

    "partition violence", "direct action day", "calcutta killings",
    "punjab massacres", "kashmir conflict", "indo-pak wars",

    "indonesian genocide", "indonesian killings", "communist purge",
    "east timor genocide", "santa cruz massacre",

    "vietnamese boat people", "refugees", "asylum seekers",
    "population transfer", "forced migration", "ethnic cleansing",

    # Colonial & Imperial Terms
    "colonial", "colonialism", "imperialism", "occupation",
    "military occupation", "puppet state", "vassal state",
    "protectorate", "mandate", "sphere of influence",
    "extraterritoriality", "concessions", "treaty ports",
    "unequal treaties", "capitulations", "sovereign rights",

    "war crimes", "crimes against humanity", "genocide",
    "ethnic cleansing", "mass atrocity", "human rights violations",
    "forced conscription", "military service", "draft",

    "partition", "independence", "decolonization", "self-determination",
    "nationalism", "national liberation", "sovereignty",

    # Reparations-Specific Terms
    "reparations", "war reparations", "compensation", "restitution",
    "reconciliation", "historical reconciliation", "transitional justice",

    "treaty", "peace treaty", "san francisco treaty", "treaty of peace",
    "bilateral treaty", "multilateral treaty", "international agreement",

    "war claims", "claims commission", "settlement", "legal settlement",
    "comfort women agreement", "bilateral agreement", "diplomatic agreement",

    "asset seizure", "frozen assets", "confiscated property",
    "looted artifacts", "cultural property", "art restitution",
    "stolen property", "war booty", "plundered resources",

    "official development assistance", "ODA", "economic aid",
    "economic cooperation", "technical cooperation", "grant aid",
    "yen loans", "soft loans", "development projects",

    "apology", "formal apology", "state apology", "acknowledgment",
    "statement of remorse", "official statement", "joint declaration",

    "victims", "survivors", "bereaved families", "affected communities",
    "comfort women survivors", "forced laborers", "war victims",
    "civilian victims", "military victims", "displaced persons",

    "historical justice", "transitional justice", "restorative justice",
    "historical memory", "collective memory", "historical responsibility",

    "truth commission", "investigation commission", "fact-finding mission",
    "historical commission", "joint research", "history dialogue",

    # Legal & Diplomatic Terms
    "international law", "humanitarian law", "human rights law",
    "war crimes law", "criminal law", "civil law",
    "customary law", "treaty law", "diplomatic law",

    "jurisdiction", "legal jurisdiction", "territorial jurisdiction",
    "universal jurisdiction", "domestic courts", "international courts",

    "statute of limitations", "legal barriers", "sovereign immunity",
    "state immunity", "diplomatic immunity", "act of state",

    "class action", "group litigation", "collective claims",
    "individual claims", "corporate liability", "state responsibility",

    "diplomatic relations", "bilateral relations", "multilateral relations",
    "normalization", "diplomatic recognition", "state succession",

    # Organizations & Institutions
    "united nations", "league of nations", "security council",
    "general assembly", "international court of justice",
    "permanent court of arbitration",

    "international military tribunal", "tokyo trials", "nuremberg trials",
    "war crimes tribunal", "international criminal court",
    "special courts", "hybrid tribunals",

    "asian development bank", "ADB", "world bank", "IMF",
    "asian infrastructure investment bank", "AIIB",

    "asian african legal consultative organization", "AALCO",
    "ASEAN", "southeast asian nations", "SAARC", "south asian association",

    "british commonwealth", "commonwealth of nations",
    "non-aligned movement", "bandung conference",

    "NGOs", "civil society organizations", "advocacy groups",
    "victims' organizations", "support groups", "legal aid organizations",

    "museums", "memorial museums", "peace museums",
    "war museums", "historical archives", "documentation centers",

    # Financial & Economic Terms
    "war bonds", "victory bonds", "military scrip",
    "occupation currency", "military currency", "puppet currency",

    "gold reserves", "foreign reserves", "national treasury",
    "central bank", "monetary authority", "exchange rate",

    "war damage", "reconstruction costs", "rebuilding costs",
    "economic losses", "material damages", "moral damages",

    "hyperinflation", "currency devaluation", "economic collapse",
    "black market", "informal economy", "war economy",

    # Contemporary Issues
    "historical revisionism", "historical denialism", "textbook controversy",
    "memory politics", "politics of memory", "historical memory",

    "shrine visits", "yasukuni shrine", "war memorials",
    "commemoration", "remembrance", "memorial services",

    "comfort women statues", "peace monuments", "memorial monuments",
    "historical markers", "sites of memory", "lieu de memoire",

    "historical education", "peace education", "reconciliation education",
    "museum education", "public history", "oral history"

# ----------------------------------------------------------------------------------------------------------------

    # Oceania
    # Comprehensive list of Oceanian regions, historical terms, and reparations-related search terms

    # Australia and Surrounding Regions
    "australia", "commonwealth of australia", "british australia", "new holland",
    "terra australis", "new south wales", "victoria", "queensland",
    "western australia", "south australia", "tasmania", "van diemen's land",
    "northern territory", "australian capital territory", "norfolk island",
    "christmas island", "cocos islands", "heard and mcdonald islands",
    "australian antarctic territory", "aboriginal australia", "torres strait islands",

    # New Zealand and Associated Territories
    "new zealand", "aotearoa", "british new zealand", "dominion of new zealand",
    "north island", "te ika-a-māui", "south island", "te waipounamu",
    "stewart island", "rakiura", "chatham islands", "rekohu", "wharekauri",
    "ross dependency", "tokelau", "niue", "cook islands",

    # Melanesia
    "papua new guinea", "territory of papua", "german new guinea", "british new guinea",
    "territory of new guinea", "papua", "west papua", "west new guinea",
    "irian jaya", "dutch new guinea", "kaiser-wilhelmsland",

    "solomon islands", "british solomon islands", "german solomon islands",
    "guadalcanal", "malaita", "santa isabel", "choiseul", "new georgia",

    "vanuatu", "new hebrides", "french new hebrides", "british new hebrides",
    "condominium of the new hebrides", "efate", "espiritu santo",

    "new caledonia", "nouvelle-calédonie", "french new caledonia",
    "grande terre", "loyalty islands", "isle of pines",

    "fiji", "british fiji", "colony of fiji", "viti", "rotuma",
    "kingdom of fiji", "dominion of fiji", "republic of fiji",

    # Micronesia
    "federated states of micronesia", "caroline islands", "trust territory",
    "yap", "chuuk", "pohnpei", "kosrae", "german new guinea",

    "palau", "belau", "german palau", "japanese palau",
    "trust territory of the pacific islands",

    "marshall islands", "german marshall islands", "japanese mandate",
    "american occupation", "trust territory", "bikini atoll", "enewetak atoll",

    "nauru", "pleasant island", "german nauru", "british nauru",
    "australian nauru", "phosphate mining", "central pacific",

    "kiribati", "gilbert islands", "british gilbert islands",
    "gilbert and ellice islands", "phoenix islands", "line islands",

    # Polynesia
    "samoa", "western samoa", "german samoa", "american samoa",
    "upolu", "savai'i", "tutuila", "manu'a islands",

    "tonga", "friendly islands", "british protected state",
    "kingdom of tonga", "tongatapu", "vava'u", "ha'apai",

    "tuvalu", "ellice islands", "british colony", "funafuti",
    "gilbert and ellice islands colony",

    "french polynesia", "établissements français de l'océanie",
    "society islands", "tahiti", "marquesas islands", "tuamotu archipelago",
    "austral islands", "gambier islands",

    "wallis and futuna", "territory of the wallis and futuna islands",
    "uvea", "futuna", "alofi",

    "pitcairn islands", "british overseas territory", "henderson",
    "ducie", "oeno", "bounty mutineers",

    # Historical Events & Specific Incidents
    "blackbirding", "pacific slave trade", "kanaka labour",
    "south sea islanders", "indentured labour", "coolie trade",

    "nuclear testing", "british nuclear tests", "french nuclear tests",
    "american nuclear tests", "operation grapple", "maralinga",
    "montebello islands", "emu field", "mururoa", "fangataufa",

    "stolen generations", "child removal", "assimilation policy",
    "aboriginal protection board", "half-caste institutions",

    "frontier wars", "black war", "killing times", "aboriginal massacres",
    "colonial violence", "resistance wars", "myall creek massacre",

    "land wars", "new zealand wars", "māori wars", "flagstaff war",
    "taranaki wars", "waikato invasion", "te kooti's war",

    "phosphate mining", "ocean island", "banaba mining",
    "environmental destruction", "forced relocation",

    "world war ii occupation", "pacific war", "japanese occupation",
    "comfort women", "forced labor", "pow camps", "sandakan death marches",

    # Indigenous Peoples & Terms
    "aboriginal australians", "torres strait islanders",
    "first nations", "indigenous australians", "koori", "murri",
    "nunga", "noongar", "yolŋu", "anangu", "tiwi", "palawa",

    "māori", "tangata whenua", "iwi", "hapu", "whanau",
    "rangatiratanga", "mana whenua", "kaitiakitanga",

    "kanaka maoli", "pacific islanders", "pasifika", "melanesians",
    "polynesians", "micronesians", "chamorro", "kanak",

    # Colonial Powers & Systems
    "british empire", "french empire", "german empire",
    "japanese empire", "dutch empire", "american colonialism",
    "colonial administration", "indirect rule", "direct rule",
    "protectorates", "mandates", "trust territories",

    # Reparations-Specific Terms
    "indigenous reparations", "colonial reparations", "nuclear reparations",
    "land rights", "native title", "aboriginal land rights",
    "treaty settlements", "compensation", "restitution",

    "treaty of waitangi", "waitangi tribunal", "treaty settlements",
    "treaty claims", "historical claims", "contemporary claims",

    "stolen generations compensation", "bringing them home report",
    "national apology", "healing foundation", "link-up services",

    "nuclear compensation", "radiation exposure compensation",
    "environmental restoration", "health monitoring",

    # Legal & Political Terms
    "native title", "aboriginal title", "indigenous title",
    "customary land rights", "traditional ownership",
    "land councils", "prescribed bodies corporate",

    "self-determination", "sovereignty", "indigenous rights",
    "constitutional recognition", "voice to parliament",
    "treaty making", "makarrata", "truth-telling",

    "traditional custodians", "cultural heritage protection",
    "sacred sites", "cultural property", "repatriation",

    # Organizations & Institutions
    "pacific islands forum", "secretariat of the pacific community",
    "melanesian spearhead group", "polynesian leaders group",
    "pacific regional environment programme",

    "national aboriginal conference", "aboriginal and torres strait islander commission",
    "land councils", "prescribed bodies corporate",

    "māori council", "iwi authorities", "urban māori authorities",
    "treaty of waitangi fisheries commission",

    # Contemporary Issues
    "climate change reparations", "environmental justice",
    "sea level rise", "climate refugees", "environmental migration",

    "cultural repatriation", "artifact return", "museum restitution",
    "ancestral remains return", "cultural property rights",

    "language revival", "cultural revival", "traditional knowledge",
    "indigenous education", "bilingual education",

    # Economic Terms
    "resource extraction", "mining royalties", "native title compensation",
    "treaty settlement assets", "indigenous business development",
    "benefit sharing agreements", "impact benefit agreements",

    # Documentation & Memory
    "oral history", "songlines", "dreaming stories", "traditional knowledge",
    "cultural mapping", "indigenous archaeology", "community archives",
    "memorial sites", "keeping places", "cultural centers"

# ----------------------------------------------------------------------------------------------------------------

    # Explicit Keywords
    "native american", "indigenous", "first nations", "aboriginal", "maori", "caricom",
    "african american", "black", "afro-descendant", "afro-caribbean", "transatlantic slave trade",
    "africa", "african diaspora", "systemic racism", "police brutality", "mass incarceration",
    "slavery", "colonialism", "imperialism", "genocide", "armenian genocide", "rwandan genocide",
    "cambodian genocide", "bosnian genocide", "forced displacement", "land theft", "trail of tears",
    "nakba", "jim crow", "segregation", "civil rights movement", "apartheid", "south african apartheid",
    "institutional racism", "racial inequality", "war on drugs", "prison industrial complex",
    "native american reparations", "treaty rights", "indigenous sovereignty", "stolen generations",
    "aboriginal land rights", "treaty of waitangi", "maori land claims", "world war ii reparations",
    "german reparations", "japanese american internment", "comfort women", "agent orange reparations",
    "iraq war reparations", "environmental racism", "toxic waste", "flint water crisis",
    "climate reparations", "loss and damage", "small island developing states", "indentured labor",
    "coolie trade", "economic reparations", "wealth gap", "reparative justice", "migrant worker exploitation",
    "gulf states labor rights", "comfort women reparations", "sexual violence reparations",
    "war crimes reparations", "forced sterilization", "eugenics reparations", "cultural genocide",
    "language preservation", "stolen artifacts", "repatriation of cultural property", "british museum repatriation",
    "sacred site protection", "indigenous cultural heritage", "caricom reparations commission",
    "united nations reparations", "international court of justice reparations", "truth and reconciliation commission",
    "south african truth and reconciliation commission", "haiti indemnity", "french reparations to haiti",
    "holocaust reparations", "german reparations to israel", "ta-nehisi coates reparations", "hr 40",
    "australian stolen generations reparations", "canadian residential schools reparations",
    "south african land reform", "apartheid reparations", "reparations funds", "reparations tribunals",
    "reparations policies", "reparations frameworks", "environmental degradation", "climate justice",
    "oil spills", "deforestation", "repatriation of human remains", "cultural restitution",
    "sacred land protection", "mapuche", "quechua", "aimara", "guarani", "maya", "navajo",
    "cherokee", "sioux", "inuit", "korean war", "vietnam war", "syrian civil war", "chagos", "mau mau"
]

# Count the frequency of geographical regions/case studies
geographical_counts = Counter()
for text in df['Summary']:  # Changed from 'Description' to 'Summary'
    if not isinstance(text, str):  # Skip non-string entries to prevent errors
        continue
    for keyword in geographical_keywords:
        if keyword in text:
            geographical_counts[keyword] += 1

# Show the frequency of geographical regions/case studies
print("Frequency of geographical regions/case studies related to reparations:")
for region, count in geographical_counts.most_common():  # This will print ALL terms, sorted by frequency
    print(f"{region}: {count}")