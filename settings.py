# match_list_location = "input_data/matches.csv"
match_list_location = "input_data/merged/merged.csv"
prev_position_location = "input_data/prev_positions.csv"

# EK
match_list_location_EK = "input_data/matches_EK_group.csv"

amount_of_simulations = 100

WIN_POINTS = 3
DRAW_POINTS = 1
LOSE_POINTS = 0

DECAY_RATE = 0.3
YEARS_BACK = 5

DEFAULT_POSITION = None  # the position if the team is not known in previous seasons

# Fixed schedule where winners of match 0 play against winners of match 1, and so on
FIXED_SCHEDULE = [
    [(0, 1), (2, 3), (4, 5), (6, 7), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)],
    [(0, 1), (2, 3), (4, 5), (6, 7)],
    [(0, 1), (2, 3)],  # Round 2 (Quarterfinals)
    [(0, 1)]  # Round 3 (Semifinals)
]

codes = {"Dender": 0, "Union": 1, "St. Gilloise": 1, "Anderlecht": 2, "Antwerpen": 3, "Antwerp": 3, "Club brugge": 4,
         "Club Brugge": 4, "Cercle brugge": 5, "Cercle Brugge": 5, "Krc genk": 6, "Genk": 6,
         "Gent": 7, "Kv mechelen": 8, "Mechelen": 8, "Stvv": 9, "St Truiden": 9, "Standard": 10, "Westerlo": 11,
         "Oh leuven": 12, "Oud-Heverlee Leuven": 12, "Charleroi": 13,
         "Kas eupen": 14, "Eupen": 14, "Kv korterijk": 15, "Kortrijk": 15, "Rwdm": 16, "RWD Molenbeek": 16,
         "Germany": 17, "Scotland": 18, "Hungary": 19, "Switserland": 20, "Spain": 21, "Croatia": 22, "Italy": 23,
         "Albania": 24, "Slovenia": 25, "Denmark": 26, "Serbia": 27, "England": 28, "Poland": 29, "Netherlands": 30,
         "Austria": 31, "France": 32, "Belgium": 33, "Slovakia": 34, "Romania": 35, "Ukrain": 36, "Turkey": 37,
         "Georgia": 38, "Portugal": 39, "Tsjechie": 40, "Canada": 41, "Maroco": 42, "Beveren": 42, "Louvieroise": 43,
         "Mouscron": 44, "Aalst": 45, "Harelbeke": 46, "Lokeren": 47, "Germinal": 48, "Lierse": 49, "Lommel": 50,
         "Molenbeek": 51, "Bergen": 52, "Heusden Zolder": 53, "FC Brussels": 54, "Oostende": 55, "Roeselare": 56,
         "Waregem": 57, "Tubize": 58, "Waasland-Beveren": 59, "Mouscron-Peruwelz": 60, "Beerschot VA": 61,
         "Seraing": 62, "Geel": 63, "Charlton": 64, "Chelsea": 65, "Coventry": 66, "Derby": 67, "Leeds": 68,
         "Leicester": 69, "Liverpool": 70, "Sunderland": 71, "Tottenham": 72, "Man United": 73, "Arsenal": 74,
         "Bradford": 75, "Ipswich": 76, "Middlesbrough": 77, "Everton": 78, "Man City": 79, "Newcastle": 80,
         "Southampton": 81, "West Ham": 82, "Aston Villa": 83, "Bolton": 84, "Blackburn": 85, "Fulham": 86,
         "Birmingham": 87, "West Brom": 88, "Portsmouth": 89, "Wolves": 90, "Wigan": 91, "Reading": 92,
         "Sheffield United": 93, "Watford": 94, "Hull": 95, "Stoke": 96, "Burnley": 97, "Blackpool": 98, "QPR": 99,
         "Swansea": 100, "Norwich": 101, "Crystal Palace": 102, "Cardiff": 103, "Bournemouth": 104, "Brighton": 105,
         "Huddersfield": 106, "Brentford": 107, "Nott'm Forest": 108, "Luton": 109, "Wasquehal": 110, "Ajaccio": 111,
         "Beauvais": 112, "Caen": 113, "Chateauroux": 114, "Creteil": 115, "Laval": 116, "Nice": 117, "Nimes": 118,
         "Niort": 119, "Lorient": 120, "Angers": 121, "Cannes": 122, "Gueugnon": 123, "Le Havre": 124, "Le Mans": 125,
         "Montpellier": 126, "Sochaux": 127, "Nancy": 128, "Martigues": 129, "Amiens": 130, "Grenoble": 131,
         "St Etienne": 132, "Strasbourg": 133, "Istres": 134, "Reims": 135, "Clermont": 136, "Metz": 137,
         "Valence": 138, "Toulouse": 139, "Troyes": 140, "Besancon": 141, "Rouen": 142, "Sedan": 143, "Brest": 144,
         "Guingamp": 145, "Dijon": 146, "Valenciennes": 147, "Bastia": 148, "Sete": 149, "Tours": 150, "Libourne": 151,
         "Nantes": 152, "Boulogne": 153, "Lens": 154, "Vannes": 155, "Arles": 156, "Evian Thonon Gaillard": 157,
         "Monaco": 158, "Ajaccio GFCO": 159, "Auxerre": 160, "CA Bastia": 161, "Orleans": 162, "Bourg Peronnas": 163,
         "Paris FC": 164, "Red Star": 165, "Quevilly Rouen": 166, "Beziers": 167, "Chambly": 168, "Rodez": 169,
         "Dunkerque": 170, "Pau FC": 171, "Annecy": 172, "Bordeaux": 173, "Concarneau": 174, "Charleville": 175,
         "Louhans-Cuis.": 176, "Mulhouse": 177, "Red Star 93": 178, "St Brieuc": 179, "Epinal": 180, "Perpignan": 181,
         "Toulon": 182, "Lille": 183, "Marseille": 184, "Paris SG": 185, "Lyon": 186, "Rennes": 187, "Dortmund": 188,
         "Cottbus": 189, "M'gladbach": 190, "Nurnberg": 191, "Schalke 04": 192, "Stuttgart": 193, "Bielefeld": 194,
         "Hamburg": 195, "Munich 1860": 196, "Bayern Munich": 197, "Bochum": 198, "Hannover": 199, "Hansa Rostock": 200,
         "Hertha": 201, "Kaiserslautern": 202, "Leverkusen": 203, "Werder Bremen": 204, "Wolfsburg": 205,
         "FC Koln": 206, "Freiburg": 207, "Ein Frankfurt": 208, "Mainz": 209, "Duisburg": 210, "Aachen": 211,
         "Karlsruhe": 212, "Hoffenheim": 213, "St Pauli": 214, "Augsburg": 215, "Greuther Furth": 216,
         "Fortuna Dusseldorf": 217, "Braunschweig": 218, "Paderborn": 219, "Darmstadt": 220, "Ingolstadt": 221,
         "RB Leipzig": 222, "Union Berlin": 223, "Heidenheim": 224, "Leipzig": 225, "M'Gladbach": 226,
         "Wattenscheid": 227, "Dresden": 228, "Uerdingen": 229, "Dusseldorf": 230, "Ulm": 231, "Unterhaching": 232,
         "Ein Trier": 233, "Ahlen": 234, "Lubeck": 235, "Mannheim": 236, "Burghausen": 237, "Oberhausen": 238,
         "Reutlingen": 239, "Erzgebirge Aue": 240, "Regensburg": 241, "Osnabruck": 242, "Essen": 243,
         "Saarbrucken": 244, "Erfurt": 245, "Offenbach": 246, "Siegen": 247, "CZ Jena": 248, "Koblenz": 249,
         "Wehen": 250, "Frankfurt FSV": 251, "Kaiserslautern ": 252, "Sandhausen": 253, "Aalen": 254,
         "Wurzburger Kickers": 255, "Holstein Kiel": 256, "Magdeburg": 257, "Elversberg": 258, "Chemnitz": 259,
         "Homburg": 260, "Meppen": 261, "RW Essen": 262, "Stuttgarter K": 263, "TB Berlin": 264, "F Koln": 265,
         "Wuppertaler": 266, "Zwickau": 267, "FSV Frankfurt": 268, "Gutersloh": 269, "Oldenburg": 270, "Bari": 271,
         "Napoli": 272, "Atalanta": 273, "Milan": 274, "Parma": 275, "Perugia": 276, "Reggina": 277, "Roma": 278,
         "Udinese": 279, "Inter": 280, "Lazio": 281, "Bologna": 282, "Brescia": 283, "Fiorentina": 284, "Juventus": 285,
         "Lecce": 286, "Verona": 287, "Vicenza": 288, "Chievo": 289, "Piacenza": 290, "Torino": 291, "Venezia": 292,
         "Como": 293, "Modena": 294, "Empoli": 295, "Ancona": 296, "Sampdoria": 297, "Siena": 298, "Cagliari": 299,
         "Palermo": 300, "Livorno": 301, "Messina": 302, "Ascoli": 303, "Treviso": 304, "Catania": 305, "Genoa": 306,
         "Cesena": 307, "Novara": 308, "Pescara": 309, "Sassuolo": 310, "Frosinone": 311, "Carpi": 312, "Crotone": 313,
         "Benevento": 314, "Spal": 315, "Spezia": 316, "Salernitana": 317, "Monza": 318, "Cremonese": 319,
         "Foggia": 320, "Reggiana": 321, "Padova": 322, "Cittadella": 323, "Cosenza": 324, "Ravenna": 325,
         "Pistoiese": 326, "Ternana": 327, "Triestina": 328, "Albinoleffe": 329, "Avellino": 330, "Arezzo": 331,
         "Catanzaro": 332, "Mantova": 333, "Rimini": 334, "Grosseto": 335, "Pisa": 336, "Gallipoli": 337,
         "Piacenza ": 338, "Portogruaro": 339, "Varese": 340, "Gubbio": 341, "Nocerina": 342, "Juve Stabia": 343,
         "Pro Vercelli": 344, "Virtus Lanciano": 345, "Latina": 346, "Trapani": 347, "Virtus Entella": 348,
         "Pordenone": 349, "Alessandria": 350, "Sudtirol": 351, "FeralpiSalo": 352, "Lecco": 353, "Lucchese": 354,
         "C. Sangro": 355, "F. Andria": 356, "Alzano": 357, "Fermana": 358, "Savoia": 359, "Sparta": 360,
         "Graafschap": 361, "Feyenoord": 362, "NAC Breda": 363, "Groningen": 364, "Roosendaal": 365, "Utrecht": 366,
         "Vitesse": 367, "Ajax": 368, "AZ Alkmaar": 369, "For Sittard": 370, "Willem II": 371, "Nijmegen": 372,
         "Twente": 373, "Waalwijk": 374, "PSV Eindhoven": 375, "Heerenveen": 376, "Roda JC": 377, "Den Bosch": 378,
         "Excelsior": 379, "Zwolle": 380, "Volendam": 381, "Den Haag": 382, "Heracles": 383, "VVV Venlo": 384,
         "Roda": 385, "Heracles ": 386, "Roda ": 387, "Ajax ": 388, "Feyenoord ": 389, "Graafschap ": 390,
         "Groningen ": 391, "Utrecht ": 392, "Vitesse ": 393, "Willem II ": 394, "Cambuur": 395, "Go Ahead Eagles": 396,
         "Dordrecht": 397, "Sparta Rotterdam": 398, "FC Emmen": 399, "Almere City": 400, "MVV Maastricht": 401,
         "Beira Mar": 402, "Porto": 403, "Sp Braga": 404, "Alverca": 405, "Aves": 406, "Gil Vicente": 407,
         "Salgueiros": 408, "Sp Lisbon": 409, "Leiria": 410, "Est Amadora": 411, "Campomaiorense": 412,
         "Guimaraes": 413, "Belenenses": 414, "Pacos Ferreira": 415, "Benfica": 416, "Farense": 417, "Boavista": 418,
         "Maritimo": 419, "Varzim": 420, "Setubal": 421, "Santa Clara": 422, "Academica": 423, "Moreirense": 424,
         "Nacional": 425, "Rio Ave": 426, "Estoril": 427, "Penafiel": 428, "Naval": 429, "Leixoes": 430,
         "Trofense": 431, "Olhanense": 432, "Portimonense": 433, "Feirense ": 434, "Feirense": 435, "Arouca": 436,
         "Tondela": 437, "Uniao Madeira": 438, "Chaves": 439, "Famalicao": 440, "Vizela": 441, "Casa Pia": 442,
         "Estrela": 443, "Desp. Chaves": 444, "Madeira": 445, "Tirsense": 446, "Campomaior": 447, "Felgueiras": 448,
         "Leca": 449, "Espinho": 450, "Ayr": 451, "Clyde": 452, "Inverness C": 453, "Morton": 454, "Raith Rvs": 455,
         "Airdrie": 456, "Alloa": 457, "Falkirk": 458, "Livingston": 459, "Ross County": 460, "Partick": 461,
         "Arbroath": 462, "St Mirren": 463, "Queen of Sth": 464, "St Johnstone": 465, "Brechin": 466,
         "Airdrie Utd": 467, "Hamilton": 468, "Dundee": 469, "Stranraer": 470, "Gretna": 471, "Stirling": 472,
         "Dunfermline": 473, "Cowdenbeath": 474, "Dumbarton": 475, "Hibernian": 476, "Rangers": 477, "Hearts": 478,
         "Dundee United": 479, "Kilmarnock": 480, "Cove Rangers": 481, "Queens Park": 482, "Clydebank": 483,
         "East Fife": 484, "Motherwell": 485, "Aberdeen": 486, "Celtic": 487, "Barcelona": 488, "La Coruna": 489,
         "Real Madrid": 490, "Sociedad": 491, "Zaragoza": 492, "Las Palmas": 493, "Mallorca": 494, "Numancia": 495,
         "Osasuna": 496, "Villarreal": 497, "Ath Bilbao": 498, "Malaga": 499, "Santander": 500, "Valencia": 501,
         "Valladolid": 502, "Alaves": 503, "Celta": 504, "Espanol": 505, "Oviedo": 506, "Vallecano": 507,
         "Sevilla": 508, "Tenerife": 509, "Betis": 510, "Recreativo": 511, "Ath Madrid": 512, "Albacete": 513,
         "Murcia": 514, "Getafe": 515, "Levante": 516, "Cadiz": 517, "Gimnastic": 518, "Almeria": 519, "Sp Gijon": 520,
         "Xerez": 521, "Hercules": 522, "Granada": 523, "Elche": 524, "Eibar": 525, "Cordoba": 526, "Leganes": 527,
         "Girona": 528, "Huesca": 529, "Lerida": 530, "Logrones": 531, "Compostela": 532, "Merida": 533,
         "Salamanca": 534, "Extremadura": 535, "Villareal": 536, "Lleida": 537, "Jaen": 538, "U.Las Palmas": 539,
         "Badajoz": 540, "Ferrol": 541, "Poli Ejido": 542, "Burgos": 543, "Terrassa": 544, "Ciudad de Murcia": 545,
         "Malaga B": 546, "Algeciras": 547, "Pontevedra": 548, "Lorca": 549, "Castellon": 550, "Real Madrid B": 551,
         "Vecindario": 552, "Ponferradina": 553, "Sevilla B": 554, "Granada 74": 555, "Alicante": 556,
         "Real Union": 557, "Villarreal B": 558, "Cartagena": 559, "Alcorcon": 560, "Barcelona B": 561, "Alcoyano": 562,
         "Guadalajara": 563, "Sabadell": 564, "Mirandes": 565, "Lugo": 566, "Llagostera": 567, "Ath Bilbao B": 568,
         "Reus Deportiu": 569, "UCAM Murcia": 570, "Leonesa": 571, "Extremadura UD": 572, "Rayo Majadahonda": 573,
         "Fuenlabrada": 574, "Sociedad B": 575, "Ibiza": 576, "Amorebieta": 577, "Andorra": 578, "Eldense": 579,
         "Toledo": 580, "Ath Madrid B": 581, "Ecija": 582, "Orense": 583, "Mallorca B": 584, "Ourense": 585,
         "Raith": 586
         }
