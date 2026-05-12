# FAQ — szablon do uzupełnienia (NIE publikowany)

Ten plik jest **wykluczony z output Jekyll** (`exclude:` w `_config.yml`).
Służy jako notatka dla właściciela: jak dodać FAQ do strony specjalizacji.

---

## Jak działa pole `faq:` we front-matter

Na każdej stronie specjalizacji w `_specjalizacje/` można dodać pole `faq:`
z listą par pytanie/odpowiedź. Jeżeli pole istnieje i ma co najmniej jeden
wpis, na stronie pojawi się sekcja "Najczęściej zadawane pytania" oraz
strukturalne dane FAQPage dla Google/Bing/ChatGPT.

Jeżeli pole jest puste lub nie istnieje, nic się nie renderuje.

## Format YAML

W front-matter (między dwoma `---` na górze pliku), po standardowych polach,
dodaj:

```yaml
faq:
  - q: "Treść pytania?"
    a: "Treść odpowiedzi. Może być **pogrubienie** oraz [linki](https://example.com)."
  - q: "Kolejne pytanie?"
    a: "Kolejna odpowiedź. Można też podzielić na akapity — wystarczy
        pusta linia w środku tekstu."
```

**Ważne:**
- Cudzysłowy wokół `q:` i `a:` są wymagane (YAML).
- Odpowiedź obsługuje Markdown — bold, kursywa, linki, listy.
- 3-5 pytań na stronę to optymalne dla SEO i AI.
- Pytanie powinno być pełnym zdaniem (tak właśnie ludzie pytają wyszukiwarki).

## Co warto dodać do każdej specjalizacji

Idea: **odpowiadać na pytania, które klient faktycznie wpisuje do Google
albo zadaje ChatGPT**. Poniżej propozycje wyjściowe — Piotr może je zmienić,
przepisać lub całkiem zignorować, ale niech będą jako punkt startu.

---

### Prawo karne (`_specjalizacje/prawo-karne.md`)

```yaml
faq:
  - q: "Co zrobić w razie zatrzymania przez Policję?"
    a: "Zachować spokój i jak najszybciej skontaktować się z obrońcą.
        Masz prawo do milczenia oraz do kontaktu z adwokatem. Nie podpisuj
        protokołów, których treści nie rozumiesz — czekaj na obecność
        pełnomocnika."

  - q: "Ile kosztuje obrońca w sprawie karnej?"
    a: "Wynagrodzenie ustalane jest indywidualnie i zależy od skomplikowania
        sprawy, etapu postępowania i przewidywanego nakładu pracy. Możliwe
        są ryczałty za sprawę, stawki godzinowe lub model mieszany.
        Pierwsza konsultacja zawsze obejmuje wycenę."

  - q: "Czy mogę odwołać się od wyroku sądu?"
    a: "Tak, od wyroku sądu I instancji przysługuje apelacja — termin
        wynosi zazwyczaj 14 dni od doręczenia wyroku z uzasadnieniem.
        Po wyroku sądu II instancji w niektórych przypadkach przysługuje
        kasacja do Sądu Najwyższego."

  - q: "Jaka jest różnica między obrońcą a pełnomocnikiem w sprawie karnej?"
    a: "Obrońca reprezentuje oskarżonego lub podejrzanego.
        Pełnomocnik reprezentuje pokrzywdzonego, oskarżyciela posiłkowego
        lub prywatnego. Adwokat może występować w obu rolach — ale nie
        w tej samej sprawie po obu stronach."

  - q: "Czy warto przyjąć dobrowolne poddanie się karze?"
    a: "Zależy od sytuacji. Czasem to najlepsze wyjście (mniejsza kara,
        szybsze zakończenie sprawy), czasem strategiczny błąd. Decyzja
        powinna być poprzedzona analizą dowodów i realnych szans
        na pełne uniewinnienie."
```

### Prawo cywilne (`_specjalizacje/prawo-cywilne.md`)

```yaml
faq:
  - q: "Jakie są terminy przedawnienia roszczeń cywilnych?"
    a: "Podstawowy termin to 6 lat (od 2018 r.), dla roszczeń związanych
        z działalnością gospodarczą — 3 lata. Niektóre roszczenia mają
        krótsze terminy specjalne (np. z umowy o dzieło — 2 lata).
        Po przedawnieniu dłużnik może uchylić się od zapłaty."

  - q: "Czy mogę domagać się odszkodowania bez pomocy adwokata?"
    a: "Tak, ale w sprawach cywilnych przygotowanie pozwu, gromadzenie
        dowodów i prowadzenie negocjacji wymaga wiedzy procesowej.
        Profesjonalne wsparcie znacząco zwiększa szanse na korzystne
        rozstrzygnięcie i pełną kwotę roszczenia."

  - q: "Co to jest zachowek i kiedy mi przysługuje?"
    a: "Zachowek to roszczenie pieniężne przysługujące najbliższym
        krewnym spadkodawcy (zstępnym, małżonkowi, rodzicom), którzy
        zostali pominięci w testamencie. Wysokość to 1/2 udziału
        spadkowego (dla osób trwale niezdolnych do pracy i małoletnich
        — 2/3)."

  - q: "Jak długo trwa sprawa o zapłatę przed sądem?"
    a: "Zależy od wartości przedmiotu sporu i obciążenia sądu.
        W postępowaniu uproszczonym (do 20 tys. zł) — często do roku
        w I instancji. Sprawy bardziej skomplikowane — 1,5 do 3 lat
        z apelacją włącznie."
```

### Prawo rodzinne (`_specjalizacje/prawo-rodzinne.md`)

```yaml
faq:
  - q: "Ile trwa sprawa rozwodowa?"
    a: "Rozwód bez orzekania o winie i bez sporów dotyczących dzieci
        — często 2-4 miesiące. Rozwód z orzekaniem o winie i ze sporem
        o opiekę nad dziećmi — 1 do 3 lat. Pierwsze posiedzenie sądu
        wyznaczane jest zazwyczaj 2-6 miesięcy po złożeniu pozwu."

  - q: "Czy mogę uzyskać rozwód jeżeli małżonek się nie zgadza?"
    a: "Tak. Sąd orzeka rozwód, jeżeli stwierdzi trwały i zupełny rozkład
        pożycia małżeńskiego — zgoda drugiego małżonka nie jest wymagana.
        Brak zgody zazwyczaj wydłuża postępowanie i wpływa na ustalenie winy."

  - q: "Jak ustalana jest wysokość alimentów?"
    a: "Sąd bierze pod uwagę usprawiedliwione potrzeby dziecka
        (utrzymanie, edukacja, leczenie, rozrywka) oraz możliwości
        zarobkowe i majątkowe rodzica zobowiązanego. Nie ma sztywnej
        tabeli — orzecznictwo wskazuje na 15-25% dochodów netto rodzica
        na każde dziecko, ale konkretna kwota wynika z analizy stanu
        faktycznego."

  - q: "Czy podział majątku musi odbyć się przy rozwodzie?"
    a: "Nie. Podział majątku można przeprowadzić w trakcie sprawy
        rozwodowej, ale częściej robi się to osobnym postępowaniem
        (lub umową między byłymi małżonkami) po prawomocnym rozwodzie.
        Łączenie tych spraw wydłuża rozwód."
```

### Prawo spadkowe (`_specjalizacje/prawo-spadkowe.md`)

```yaml
faq:
  - q: "Ile czasu mam na odrzucenie spadku?"
    a: "Sześć miesięcy od dnia, w którym dowiedziałeś się o tytule
        powołania do spadku (najczęściej — od śmierci spadkodawcy).
        Po upływie tego terminu domyślnie spadek jest przyjęty
        z dobrodziejstwem inwentarza (od 2015 r.)."

  - q: "Jak udowodnić, że jestem spadkobiercą?"
    a: "Potrzebne jest postanowienie sądu o stwierdzeniu nabycia spadku
        lub notarialny akt poświadczenia dziedziczenia. Bez tego nie
        możesz zarządzać majątkiem spadkowym ani dochodzić wynikających
        z niego roszczeń."

  - q: "Czy muszę spłacać długi spadkodawcy?"
    a: "Zależy od formy przyjęcia spadku. Przyjęcie wprost — pełna
        odpowiedzialność za długi. Przyjęcie z dobrodziejstwem
        inwentarza — odpowiedzialność tylko do wysokości czynnej wartości
        spadku. Odrzucenie — żadnej odpowiedzialności, ale spadku
        też się nie dziedziczy."

  - q: "Co to jest zachowek i kto może go żądać?"
    a: "Roszczenie pieniężne przysługujące najbliższym krewnym
        (zstępnym, małżonkowi, rodzicom) pominiętym w testamencie.
        Wynosi 1/2 udziału spadkowego, który by im przysługiwał
        z ustawy (lub 2/3 dla osób małoletnich i trwale niezdolnych
        do pracy). Termin dochodzenia — 5 lat od ogłoszenia testamentu."
```

### Prawo pracy (`_specjalizacje/prawo-pracy.md`)

```yaml
faq:
  - q: "Ile mam czasu na odwołanie od wypowiedzenia umowy o pracę?"
    a: "21 dni od doręczenia wypowiedzenia (przed 2017 r. było 7 dni
        — ten przepis już nie obowiązuje). Termin liczy się ściśle.
        Po jego upływie sąd odrzuci pozew nawet jeżeli wypowiedzenie
        było rażąco bezprawne."

  - q: "Czy pracodawca może mnie zwolnić bez podania przyczyny?"
    a: "Przy umowie na czas nieokreślony — nie, wypowiedzenie musi
        zawierać uzasadnienie, które jest weryfikowane przez sąd.
        Przy umowie na okres próbny lub na czas określony — przyczyny
        podawać nie trzeba, ale wypowiedzenie z naruszeniem przepisów
        może rodzić odpowiedzialność odszkodowawczą."

  - q: "Co przysługuje mi w przypadku zwolnienia dyscyplinarnego?"
    a: "Jeżeli rozwiązanie umowy bez wypowiedzenia było bezzasadne,
        możesz domagać się: przywrócenia do pracy z wynagrodzeniem
        za czas pozostawania bez pracy LUB odszkodowania w wysokości
        wynagrodzenia za okres wypowiedzenia. Termin na pozew — 21 dni."

  - q: "Jak udowodnić mobbing przed sądem?"
    a: "Dokumentacja — maile, wiadomości, świadkowie, zaświadczenia
        lekarskie o pogorszeniu stanu zdrowia. Sąd wymaga wykazania
        długotrwałości, uporczywości i zorganizowanego charakteru
        nękania. To trudne dowodowo postępowania — warto zacząć od
        konsultacji prawnej."
```

### Służby mundurowe (`_specjalizacje/sluzby-mundurowe.md`)

```yaml
faq:
  - q: "Czy żołnierz zawodowy może zatrudnić cywilnego adwokata w postępowaniu dyscyplinarnym?"
    a: "Tak. Obwiniony żołnierz ma prawo do obrońcy z wyboru — może nim
        być adwokat lub inny żołnierz wskazany przez obwinionego.
        Korzystanie z cywilnego adwokata bywa korzystne ze względu na
        niezależność od struktury wojskowej."

  - q: "Jakie są terminy w postępowaniu dyscyplinarnym żołnierzy?"
    a: "Postępowanie wyjaśniające — co do zasady 30 dni (z możliwością
        przedłużenia). Od orzeczenia dyscyplinarnego przysługuje
        odwołanie w terminie 7 dni. Od orzeczenia organu II instancji
        — skarga do Wojewódzkiego Sądu Administracyjnego w terminie
        30 dni."

  - q: "Czy mogę odwołać się od decyzji o zwolnieniu ze służby?"
    a: "Tak — od rozkazu personalnego o zwolnieniu ze służby
        przysługuje odwołanie do organu wyższego stopnia (zazwyczaj
        7-14 dni), a następnie skarga do sądu administracyjnego.
        Wcześnie podjęta obrona prawna zwiększa szanse na uchylenie
        decyzji."

  - q: "Jak ustalana jest wojskowa emerytura?"
    a: "Wysokość emerytury zależy od stażu służby, ostatniego
        uposażenia i przeliczników (np. praca w warunkach szczególnych,
        służba w misjach zagranicznych). Decyzję wydaje Wojskowe Biuro
        Emerytalne. Od decyzji przysługuje odwołanie do sądu okręgowego
        — wydziału pracy i ubezpieczeń społecznych."

  - q: "Czy mogę uzyskać podwyższenie emerytury wojskowej z tytułu inwalidztwa?"
    a: "Tak, jeżeli inwalidztwo pozostaje w związku ze służbą.
        Konieczne jest orzeczenie wojskowej komisji lekarskiej oraz
        ustalenie związku przyczynowego między służbą a powstaniem
        niezdolności do pracy. Często wymaga to postępowania sądowego."
```

---

## Wskazówki redakcyjne

- **Pytania zaczynaj od typowego sformułowania klienta** — "Ile kosztuje",
  "Czy mogę", "Jak długo", "Co zrobić jeżeli". To są frazy, które ludzie
  wpisują do Google.
- **Odpowiedzi krótkie i konkretne** — 2-4 zdania. Jeżeli temat
  wymaga długiej odpowiedzi, zostaw ją na osobny wpis blogowy
  i zalinkuj go w odpowiedzi.
- **Unikaj prawniczego żargonu** — jeżeli musisz użyć terminu (np.
  "kasacja"), wytłumacz go w nawiasie. Klient czyta to przed
  podjęciem decyzji o kontakcie.
- **Nie obiecuj wyników** — to wbrew etyce adwokackiej i sąd / izba
  może mieć zastrzeżenia. Zamiast "wygramy sprawę" — "zwiększymy
  szanse na korzystne rozstrzygnięcie".
- **Sprawdzaj aktualność** — jeżeli zmieniają się przepisy (np.
  terminy procesowe), zaktualizuj FAQ. AI engines indeksują te dane
  i klienci mogą zacytować je przeciwko Tobie jeżeli będą nieaktualne.

## Jak dodać/zaktualizować

1. Otwórz `_specjalizacje/<slug>.md`
2. W sekcji front-matter dodaj pole `faq:` (skopiuj jeden z bloków powyżej
   jako punkt startu).
3. Commit + push. Po ~1 minucie FAQ pojawi się na stronie pod sekcją
   z aktualnościami, a nad sekcją kontaktową.
4. Sprawdź w Google Rich Results Test
   (https://search.google.com/test/rich-results), że FAQ schema jest
   poprawnie wykryta.
