# Zajęcia 12. Dryf, ciągłe trenowanie, incydent i wprowadzenie do LLMOps

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 11, monitoring we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_12.ipynb`; `evidently`, `nannyml`
- **Rezultat:** detekcja dryfu, estymacja jakości bez etykiet metodą CBPE, kontrolowany ponowny trening, runbook i ewaluacja promptów

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. rozróżnia cztery rodzaje dryfu i wie, który z nich naprawdę szkodzi;
2. mierzy zmianę rozkładu i zna ograniczenia testów statystycznych;
3. szacuje jakość modelu w oknie bez etykiet;
4. definiuje wyzwalacze ponownego treningu i bramkę promocji;
5. prowadzi analizę przyczyn źródłowych i zapisuje runbook;
6. wersjonuje prompty, ocenia je na stałym zbiorze i zna typowe zagrożenia aplikacji LLM.

## 2. Cztery rodzaje dryfu

| Rodzaj | Co się zmienia | Objaw | Czy szkodzi |
|---|---|---|---|
| **Data drift** | rozkład wejścia `P(X)` | inne wartości cech niż w treningu | nie zawsze |
| **Concept drift** | zależność `P(y\|X)` | ta sama obserwacja ma dziś inną etykietę | zawsze |
| **Quality drift** | jakość danych | więcej braków, błędne typy, nowe kategorie | zawsze |
| **Training-serving skew** | różnica między ścieżkami | model widzi co innego niż w treningu | zawsze |

Najczęstsze nieporozumienie: **data drift sam w sobie nie jest awarią**. Rozkład wejścia może się zmienić bez żadnego wpływu na jakość — na przykład gdy przybyło klientów z segmentu, który model i tak dobrze obsługuje. Alarmowanie na każdą zmianę rozkładu jest prostą drogą do zignorowania alertów.

Groźny jest **concept drift**: świat zmienił reguły, a model nadal stosuje stare. Objawia się spadkiem jakości, więc wykryjemy go dopiero po etykietach — i dlatego potrzebujemy sygnałów pośrednich.

## 3. Jak mierzyć zmianę rozkładu

### Wskaźnik stabilności populacji (PSI)

Dzielimy zakres wartości na kubełki i porównujemy udziały w oknie referencyjnym i bieżącym. Interpretacja praktyczna:

| PSI | Interpretacja |
|---|---|
| < 0,1 | brak istotnej zmiany |
| 0,1 – 0,25 | zmiana warta obserwacji |
| > 0,25 | zmiana istotna, wymaga reakcji |

PSI ma zaletę: **nie zależy od liczności próby**. Mierzy wielkość różnicy, a nie pewność, że różnica istnieje.

### Testy statystyczne i ich pułapka

Test Kołmogorowa-Smirnowa dla cech liczbowych i test chi-kwadrat dla kategorycznych odpowiadają na pytanie „czy różnica jest istotna statystycznie". Przy dużych próbach odpowiedź brzmi **zawsze tak**, bo nawet mikroskopijna różnica staje się istotna.

Konsekwencja praktyczna: przy strumieniu miliona żądań dziennie test istotności zapali się codziennie i przestanie nieść informację. Dlatego:

- **wielkość efektu** (PSI, odległość rozkładów) jest ważniejsza niż wartość p;
- próg dobiera się na podstawie **historycznej zmienności**, a nie z podręcznika;
- alarmować należy na skutku (spadek jakości, wzrost udziału danych spoza zakresu), a nie na samej istotności.

### Dobór okien

Wynik detekcji zależy od tego, co porównujemy. Okno referencyjne powinno być stabilne i reprezentatywne — zwykle jest to zbiór treningowy albo okres uznany za „normalny". Okno bieżące musi być na tyle długie, żeby wygładzić szum, i na tyle krótkie, żeby zmiana nie zdążyła się rozmyć. Ten sam strumień oceniony w oknie godzinowym i tygodniowym daje dwa różne werdykty — i oba mogą być poprawne.

## 4. Jakość bez etykiet

W oknie, w którym etykiet jeszcze nie ma, jakość można **oszacować**. Najprostsza rodzina metod opiera się na pewności modelu: jeżeli dobrze skalibrowany klasyfikator zwraca prawdopodobieństwo 0,95, to średnio w 95% przypadków ma rację. Uśredniając pewność po oknie, otrzymujemy przybliżenie dokładności.

Metoda działa tylko przy spełnionych założeniach:

- model jest **skalibrowany** — deklarowane prawdopodobieństwa odpowiadają częstościom;
- zmienił się rozkład wejścia, **nie** zależność między wejściem a etykietą;
- okno jest dostatecznie liczne.

Przy concept drifcie ta metoda zawodzi: model jest pewny i jednocześnie się myli. To nie jest wada estymatora, tylko informacja — **rozbieżność między szacunkiem a rzeczywistością sama w sobie jest sygnałem**, że zmieniła się zależność, a nie tylko dane.

### CBPE — to samo, tylko porządnie

Narzędziem referencyjnym jest NannyML z metodą **CBPE** (*Confidence-Based Performance Estimation*). Działa w trzech krokach:

1. na oknie referencyjnym **z etykietami** kalibruje prawdopodobieństwa modelu;
2. dla okna analizy **bez etykiet** wyznacza oczekiwaną macierz pomyłek;
3. z niej wyprowadza szacunek metryki wraz z przedziałem ufności.

Różnica wobec zwykłej średniej z pewności jest istotna: CBPE nie zakłada, że model jest skalibrowany — samo go kalibruje — i podaje niepewność własnego oszacowania. Założenie pozostaje jedno i trzeba je znać: **zależność między cechami a etykietą się nie zmieniła**.

W ćwiczeniu zobaczysz to na liczbach: przy dryfie koncepcji CBPE szacuje dokładność na około 0,95, podczas gdy rzeczywista wynosi 0,40. Estymator myli się o pół punktu — spokojnie i z przekonaniem. Dlatego estymacja jakości **nie zastępuje** etykiet; ona jedynie skraca czas do pierwszego sygnału.

## 5. Ciągłe trenowanie

Wyzwalacze ponownego treningu, od najprostszego do najlepszego:

1. **harmonogram** — co tydzień, co miesiąc; prosty, ale trenuje też wtedy, gdy nie trzeba;
2. **nowe dane** — po napłynięciu określonej liczby nowych obserwacji z etykietami;
3. **sygnał z monitoringu** — spadek jakości albo istotny dryf;
4. **decyzja człowieka** — zmiana produktu, prawa, procesu biznesowego.

W praktyce łączy się kilka. Kluczowa zasada: **ponowny trening nie jest tym samym co wdrożenie**. Nowy model jest kandydatem, który musi przejść tę samą bramkę jakości co każdy inny (zajęcia 7) i to samo bezpieczne wdrożenie (zajęcia 10).

Automat trenujący bez bramki to najszybszy znany sposób na wdrożenie gorszego modelu.

### Champion i challenger

Nowo wytrenowany model porównujemy z obecnym na **tym samym, ustalonym zbiorze** oraz — jeśli to możliwe — na ruchu w trybie shadow. Decyzja musi być zapisana wraz z uzasadnieniem, także wtedy, gdy brzmi „odrzucamy".

## 6. Incydent: runbook i analiza przyczyn

Runbook incydentowy odpowiada na cztery pytania: **jak rozpoznać**, **co zrobić natychmiast**, **jak potwierdzić**, **kogo poinformować**. Ma być krótki i wykonalny przez osobę, która nie pisała systemu.

Analiza przyczyn źródłowych szuka mechanizmu, nie winnego. Prosta technika „pięciu dlaczego":

```text
Spadła jakość modelu.
→ Dlaczego? Bo dane wejściowe mają inny rozkład.
→ Dlaczego? Bo zmieniła się jednostka jednej z kolumn.
→ Dlaczego? Bo system źródłowy został zaktualizowany.
→ Dlaczego? Bo nikt nie poinformował o zmianie kontraktu.
→ Dlaczego? Bo nie istniał uzgodniony kontrakt danych.
```

Przyczyną nie jest „model się zepsuł", tylko brak kontraktu danych. Wniosek z analizy powinien być **zmianą w systemie**, a nie apelem o uważność.

Przegląd incydentu prowadzimy bez wskazywania winnych. Zespół, który obawia się konsekwencji, przestaje zgłaszać problemy — i wtedy traci się jedyne wczesne źródło informacji.

## 7. Fairness i jakość w podgrupach

Metryka globalna ukrywa nierówności. Model o dokładności 0,94 może mieć 0,97 w jednej podgrupie i 0,71 w innej. Dlatego jakość liczy się **także w podziale** na istotne grupy — a wybór tych grup jest decyzją projektową, którą trzeba udokumentować.

Zasada praktyczna: jeżeli system podejmuje decyzje dotyczące ludzi, monitoring w podgrupach nie jest rozszerzeniem, tylko wymaganiem podstawowym.

## 8. Wprowadzenie do LLMOps

Systemy oparte na dużych modelach językowych zmieniają część elementów, ale nie zmieniają natury problemu.

| Element | Klasyczny MLOps | System z LLM |
|---|---|---|
| Artefakt do wersjonowania | model | **prompt**, konfiguracja, dokumenty, wersja modelu dostawcy |
| Zbiór ewaluacyjny | dane z etykietami | zestaw przypadków z oczekiwaniami, często bez jednej poprawnej odpowiedzi |
| Metryka | accuracy, F1 | zgodność z wymaganiami, poprawność formatu, ocena sędziego, koszt, opóźnienie |
| Powtarzalność | ziarno losowości | temperatura, wersja modelu po stronie dostawcy — poza naszą kontrolą |
| Koszt | czas obliczeń | liczba tokenów, rozliczana za każde wywołanie |

### Prompt jest artefaktem

Prompt zmienia zachowanie systemu tak samo jak zmiana kodu, więc podlega tym samym regułom: wersjonowanie, przegląd, ewaluacja przed wdrożeniem, możliwość wycofania. Prompt wklejony do kodu i poprawiany „na szybko" jest odpowiednikiem edycji modelu na produkcji.

### Ocena modelem sędziowskim

Gdy nie ma jednej poprawnej odpowiedzi, jakość ocenia inny model według zapisanych kryteriów. To użyteczne, ale obarczone wadami: sędzia bywa stronniczy wobec dłuższych odpowiedzi i wobec własnego stylu, a jego oceny nie są w pełni powtarzalne. Dlatego ocenę sędziowską **kalibruje się na próbce ocenionej przez człowieka** i uzupełnia sprawdzeniami deterministycznymi: poprawność formatu, obecność wymaganych pól, brak treści zabronionych.

### Koszt i opóźnienie jako metryki pierwszej kategorii

W systemie z LLM koszt jest proporcjonalny do liczby tokenów i naliczany przy każdym wywołaniu. Dłuższy prompt to trwale wyższy rachunek. Koszt na tysiąc żądań należy mierzyć od pierwszego dnia — inaczej ujawni się dopiero na fakturze.

### Zagrożenia specyficzne

- **Wstrzyknięcie polecenia** — dane od użytkownika zawierają instrukcję, którą model traktuje jak polecenie systemowe.
- **Wyciek promptu systemowego** wraz z zawartymi w nim zasadami albo danymi.
- **Nadmierne uprawnienia** — model wywołuje narzędzia, których nie powinien mieć.
- **Zatrucie bazy wiedzy** w systemach RAG.

Podstawowa zasada obrony: **dane od użytkownika nigdy nie są instrukcją**. Traktujemy je jako treść do przetworzenia, oddzielamy strukturalnie od instrukcji i walidujemy wyjście, zanim ktokolwiek na jego podstawie zadziała.

### Jeden szew do dostawcy

Cały system powinien rozmawiać z modelem przez **jedną funkcję**, na przykład `call_llm(prompt, tekst)`. Wszystko inne — ewaluacja, strażnik wyjścia, liczenie kosztów — woła tę funkcję i nie wie, co jest po drugiej stronie.

Trzy rzeczy, które z tego wynikają:

- podmiana dostawcy albo wersji modelu to zmiana w jednym miejscu, a nie w całym kodzie;
- **w testach podstawiamy atrapę** — deterministyczną, darmową i zawsze dostępną, więc nadającą się do potoku CI; prawdziwy model kosztuje, bywa niedostępny i odpowiada za każdym razem trochę inaczej;
- pomiar tokenów, opóźnienia i liczby błędów robi się w tym jednym miejscu, więc żaden przypadek użycia nie umknie.

Wybór realizacji sterujemy zmienną środowiskową, a klucz dostępu czytamy ze środowiska — **nigdy z repozytorium**. Klucz do modelu językowego jest sekretem rozliczanym co do wywołania; jego wyciek to nie tylko problem bezpieczeństwa, ale też rachunek.

## 9. Ćwiczenie praktyczne

### Cel

Wykrycie dryfu, oszacowanie jakości bez etykiet metodą CBPE, kontrolowany ponowny trening z bramką, runbook incydentowy oraz ewaluacja dwóch wersji promptu na stałym zbiorze.

Część dotycząca LLM działa **bez połączenia z jakimkolwiek dostawcą** — używamy deterministycznej atrapy ukrytej za funkcją `call_llm`. Celem jest mechanika procesu: wersjonowanie promptu, zbiór ewaluacyjny, ocena, koszt i zabezpieczenie przed wstrzyknięciem polecenia.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_12.ipynb`.

### Punkty kontrolne

1. **Okno referencyjne.** Porównaj wynik detekcji przy dwóch długościach okna. Dlaczego oba werdykty mogą być poprawne?
2. **Granica estymacji.** Porównaj szacunek CBPE z rzeczywistą dokładnością w trzech scenariuszach. Który z nich obnaża ograniczenie metody i o ile się ona myli?
3. **Dryf bez spadku jakości.** Znajdź scenariusz, w którym rozkład się zmienił, a jakość nie. Co zrobiłbyś, gdyby alert zapalał się w takiej sytuacji codziennie?
4. **Wstrzyknięcie polecenia.** Sprawdź, co się dzieje bez zabezpieczenia i z nim. Dlaczego sama walidacja wejścia nie wystarcza?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_12/
    ├── prompts/{v1.txt,v2.txt}
    └── reports/
        ├── drift_report.json
        ├── quality_estimation.csv
        ├── retraining_decision.json
        ├── incident_runbook.md
        └── prompt_evaluation.csv
```

## 10. Zadanie projektowe (po zajęciach)

1. Zaimplementuj detekcję dryfu dla swoich danych: okno referencyjne, okno bieżące, wskaźnik wielkości efektu.
2. Wygeneruj raport dryfu jako artefakt.
3. Dodaj szacowanie jakości w oknie bez etykiet (CBPE albo własne) i porównaj je z rzeczywistą jakością, gdy etykiety już będą. Opisz, o ile się pomyliło.
4. Zdefiniuj **wyzwalacze ponownego treningu** i uruchom go co najmniej raz.
5. Porównaj nowy model z obecnym przez bramkę jakości; zapisz decyzję wraz z uzasadnieniem, także przy odrzuceniu.
6. Napisz **runbook incydentowy** i przeprowadź analizę przyczyn źródłowych jednego zdarzenia.
7. Policz jakość w co najmniej dwóch podgrupach istotnych dla twojego problemu.
8. Jeżeli twój projekt korzysta z LLM: wersjonuj prompty, utrzymuj stały zbiór ewaluacyjny, mierz koszt, ukryj dostawcę za **jedną funkcją** i zabezpiecz się przed wstrzyknięciem polecenia.

**Kryterium ukończenia:** zasymulowany dryf uruchamia ponowny trening, a bramka jakości samodzielnie decyduje o promocji albo odrzuceniu nowego modelu.

## 11. Literatura

1. Evidently, **wykrywanie dryfu danych**:
   <https://docs.evidentlyai.com/>
2. NannyML, **szacowanie jakości modelu bez etykiet**:
   <https://nannyml.readthedocs.io/>
3. J. Gama i in., **A Survey on Concept Drift Adaptation**:
   <https://dl.acm.org/doi/10.1145/2523813>
4. OWASP, **Top 10 dla aplikacji LLM**:
   <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
5. MLflow, **ewaluacja i tracing systemów GenAI**:
   <https://mlflow.org/docs/latest/llms/>
6. Google SRE Book, **Postmortem Culture: Learning from Failure**:
   <https://sre.google/sre-book/postmortem-culture/>
