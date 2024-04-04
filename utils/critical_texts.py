import random

nat20texts = [
    "Na pewno oszukiwał!",
    "Przywołajcie druida, bo to była wyraźnie magia lasu!",
    "Czy ktoś sprawdził tę kostkę na obecność mikrochipa?",
    "Czy to możliwe, że twoja kostka to niezidentyfikowany artefakt?",
    "To musiał być długi trening w szkole czarodziejów kosteczek.",
    "To była taka fajna 20, że nawet smok się zdziwił.",
    "Jeśli masz jeszcze taką kostkę, to znaczy, że masz znajomości u samego Boga Kostek!",
    "20 na kostce? Nie jesteś przypadkiem w rzeczywistości bardem, a twoje kostki to instrumenty do tworzenia epickiej muzyki?",
    "Jeśli kiedykolwiek będziesz potrzebował pomocy w życiu, poproś tę kostkę o radę.",
    "Zdecydowanie jesteś ulubieńcem kostek. Jak się nazywasz? Chuck Kostka?",
    "Twoja kostka to prawdziwy zaklinacz sztuczki. Ktoś zna numer do Magicznej Szkoły Kostek?",
    "Gdyby kostka mogła mówić, pewnie wydobyłaby dźwięk 'Ta-da!'",
    "Gdyby to była walka w rzeczywistości, wróg by po prostu podał broń i się poddał.",
    "Jeśli twoja kostka była postacią, to na pewno byłaby superbohaterem w świecie D&D.",
    "Kiedy twoja kostka wyrzuca 20, to cały świat gry staje się bardziej kolorowy i magiczny.",
    "Jeśli to była próba, to na pewno dostałbyś złoty medal od Króla Kostek.",
    "Możliwe, że twoja kostka to wcielenie samozachwytu.",
    "20 na kostce? Chyba teraz jesteś zobowiązany do wygrania gry dla wszystkich!",
    "Ktoś dzwonił do mnie z Eldorado. Twój rzut kostką zgubił się na środku złota!"
    "To nie jest już D&D, to D20-D.",
    "Chyba jesteś magikiem kosteczek. Czy przyjmujesz uczniów?",
    "Czy masz jakieś konkretne życzenie? Twój kostka na pewno spełni.",
    "Wszyscy błagają o 20 na kostce, ale ty musisz mieć autora kostki!",
    "Twoja kostka jest tak dobra, że zasługuje na własny spin-off.",
    "To nie wyrzuciłeś 20 na kostce. To kostka wyrzuciła 20 na tobie.",
    "Chyba właśnie zdobyłeś stopień magistra w Kostkologii.",
    "Jeśli ta kostka była osobą, to miałbyś już z nią ślub.",
    "To nie był rzut kostką, to był rzut przeznaczeniem!",
    "To było takie naturalne 20, że nawet natura się zdziwiła.",
    "Jeśli nadal wyrzucasz takie liczby, Twoja kostka stanie się sławna na całym kontynencie!",
    "Ktoś powinien włączyć alarm przeciwpowodziowy, bo te wyniki są niesamowite!",
    "Twój 20 na kostce to przypadek dla Muzeum Historii Kostek.",
    "Nawet Gandalf byłby zazdrosny o twoje umiejętności rzucania kostką!",
]

nat1texts = [
    "Twój rzut kostką był tak zły, że kostka chce od Ciebie przeprosin!",
    "Czy ktoś sprawdził tę kostkę na ukrytych wadach? Może jest zepsuta.",
    "Nie martw się, 1 to przecież takie nowe 20!",
    "Twoja kostka jest tak zła, że kiedy zjawi się smok, to pewnie zacznie się od śmiechu.",
    "To chyba była próba otwarcia portalu do innego wymiaru, ale coś poszło nie tak.",
    "Właśnie dowiedziałem się, że twoja kostka została wydalona z Akademii Kostkologii.",
    "Twoja kostka jest jak złe sny, które nękają nasze postacie.",
    "Wiesz, twoja kostka była tak nieudana, żebyś był lepiej poszukał innej kostki.",
    "1 na kostce? Nawet skrzat pod stołem się śmieje.",
    "Czy może ktoś podrzucić mu dodatkową kostkę? Chyba ta się uszkodziła.",
    "1 na kostce? To jest dowód na to, że nie wszystko da się osiągnąć w życiu, nawet w świecie fantasy.",
    "Ktoś powinien podać ci zestaw do gier, w którym wszystkie kostki to 1. Byłbyś nie do pokonania!",
    "Twój rzut na pewno został wyprzedany na aukcji kostek jako 'unikatowa rzadkość'.",
    "Twoja kostka jest jak podrabiana moneta - wygląda, jakby była 1, ale naprawdę jest warta więcej.",
    "To musiał być rzut z pogranicza kosmicznej kostki - zawsze w kosmosie nikt nie słyszy twoich krzyków rozpaczy.",
    "Czy twój cel to celowanie w miniony wiek? Bo to wydaje się jedynym wytłumaczeniem.",
    "Oczywiście, to jest takie nowe 20, że trzeba było wymyślić nową skali ocen kostkowych.",
    "Twoja kostka jest tak leniwa, że zawsze jest na wakacjach.",
    "Może powinniśmy dodać do twojej kostki kapsułkę z życzeniem. Może wtedy wyrzucisz coś innego.",
    "Twój rzut jest jak tajemnicza zagadka, której nawet najmądrzejsi magowie nie potrafią rozwiązać.",
    "Twoja kostka była tak leniwa, że myślała, że wyrzuciła 10 i polegała na naszej dezorientacji!"
    "To nie był rzut kostką, to był przesłuchanie na rolę w filmie 'Najgorszy Rzut Kostką na Świecie'.",
    "Twój rzut kostką to jak odcinek fillerowy w grze D&D.",
    "1 na kostce? Czy twoja kostka przypadkiem nie jest modelem dla tabliczki z napisem 'Nie próbuj tego w domu'?",
    "Twój rzut kostką wywołał takie zdziwienie, że zapomniałem, co to za gra.",
    "Widzę, że twoja kostka jest w fazie buntu. Czy potrzebuje terapeuty?",
    "Twoja kostka jest jak teledysk do piosenki - wszyscy się z niej śmieją.",
    "1 na kostce? To jasne, że to jest początek nowej, świetlnej kariery twojej kostki jako papierowej wagi.",
    "Twoja kostka jest jak ktoś, kto zawsze spóźnia się na spotkania - zawsze trafia w złe miejsce.",
    "Czy widziałeś kiedykolwiek taką złą kostkę? Nawet mimik może zazdrościć.",
]

def getRandomNat20Text():
    return random.choice(nat20texts)

def getRandomNat1Text():
    return random.choice(nat1texts)