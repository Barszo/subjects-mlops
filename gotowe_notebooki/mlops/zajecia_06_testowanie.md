# Zajęcia 6. Testowanie systemów ML

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 5, potok i eksperymenty we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_06.ipynb`, `pytest` uruchamiany jedną komendą
- **Rezultat:** zestaw testów wykrywający cztery klasy defektów, uruchamiany jedną komendą

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. rozróżnia testy kodu, danych, modelu i kontraktu;
2. pisze testy jednostkowe transformacji cech;
3. definiuje próg jakości modelu jako test, a nie jako komentarz;
4. testuje zachowanie modelu, a nie tylko jego metrykę;
5. rozpoznaje testy kruche i wie, jak je naprawić;
6. utrzymuje czas wykonania zestawu testów w rozsądnych granicach.

## 2. Cztery rzeczy do przetestowania

W zwykłym projekcie testuje się kod. W projekcie ML kod jest tylko jednym z czterech źródeł awarii.

| Warstwa | Co sprawdzamy | Przykład testu |
|---|---|---|
| **Kod** | logika transformacji, obsługa przypadków brzegowych | „`build_features` nie zwraca kolumny z etykietą” |
| **Dane** | schemat, typy, zakresy, niezmienniki | „schemat odrzuca kolumnę tekstową tam, gdzie oczekiwana jest liczba” |
| **Model** | próg jakości, stabilność, zachowanie | „macro F1 na zbiorze kontrolnym nie spada poniżej 0,90” |
| **Kontrakt** | format wejścia i wyjścia usługi | „odpowiedź zawiera pola `prediction` i `model_version`” |

Test kodu przechodzi, a system i tak nie działa — bo zmieniło się źródło danych albo model przestał spełniać wymaganie jakości. Dlatego zestaw testów w projekcie ML musi obejmować wszystkie cztery warstwy.

## 3. Piramida testów w projekcie ML

Od podstawy do wierzchołka:

1. **Testy jednostkowe** — pojedyncze funkcje, milisekundy, uruchamiane przy każdej zmianie. Powinno ich być najwięcej.
2. **Testy danych** — schemat i niezmienniki na małej próbce. Szybkie, uruchamiane razem z jednostkowymi.
3. **Testy modelu** — trening na próbce i sprawdzenie progu jakości oraz zachowania. Wolniejsze, ale nadal liczone w sekundach.
4. **Testy integracyjne potoku** — cały przebieg na małych danych. Najwolniejsze, uruchamiane rzadziej.

Zestaw, który wykonuje się dwie minuty, będzie uruchamiany. Zestaw, który wykonuje się dwadzieścia minut, zostanie wyłączony. Dlatego testy modelu wykonuje się na **próbce** danych, a pełny trening zostaje w potoku, nie w testach.

## 4. Testy progu jakości

Próg jakości zamienia zdanie „model jest wystarczająco dobry” w warunek, który da się sprawdzić automatycznie:

```text
macro F1 na ustalonym zbiorze kontrolnym >= 0,90
```

Trzy zasady:

- **próg wynika z wymagań**, a nie z aktualnego wyniku modelu — inaczej test jedynie utrwala stan faktyczny;
- **zbiór kontrolny jest ustalony i wersjonowany**, bo test porównujący z ruchomym celem nic nie znaczy;
- **próg jest jawną decyzją** — jego obniżenie musi być widoczne w historii repozytorium.

Ten sam mechanizm posłuży później jako bramka jakości blokująca promocję modelu (zajęcia 7 i 10).

## 5. Testy zachowania modelu

Metryka mówi, jak często model się myli. Nie mówi, **czy zachowuje się sensownie**. Do tego służą trzy rodzaje testów zachowania:

- **Testy niezmienniczości** — zmiana, która nie powinna wpływać na wynik, nie zmienia predykcji. Przykłady: dodanie nieużywanej kolumny, zmiana kolejności kolumn, zmiana wielkości liter w tekście.
- **Testy kierunkowe** — zmiana, która powinna wpływać na wynik w określony sposób, faktycznie tak działa. Przykład: zwiększenie wartości cechy skorelowanej dodatnio z klasą nie powinno obniżać przewidywanego prawdopodobieństwa tej klasy.
- **Testy minimalnej funkcjonalności** — zestaw prostych, oczywistych przypadków, które model musi rozwiązać poprawnie, nawet jeśli globalna metryka jest wysoka.

Taki test wykrywa problemy, których metryka nie widzi — na przykład model, który osiąga dobrą accuracy, ale reaguje na cechę techniczną zamiast na sygnał merytoryczny.

## 6. Testy kruche

Test kruchy to test, który potrafi zawieść bez zmiany w kodzie. W ML powstaje najczęściej z trzech powodów:

| Przyczyna | Objaw | Naprawa |
|---|---|---|
| Brak ustalonego ziarna | test przechodzi co drugi raz | ustalone ziarno w podziale i modelu |
| Porównanie liczb zmiennoprzecinkowych | `assert 0.1 + 0.2 == 0.3` zawodzi | porównanie z tolerancją |
| Próg dopasowany do wyniku | każda drobna zmiana wywraca test | próg wynikający z wymagań, z zapasem |
| Zależność od czasu lub kolejności | test zawodzi po północy albo po zmianie kolejności | jawne dane wejściowe, brak stanu globalnego |

Test kruchy jest gorszy niż brak testu, bo uczy zespół ignorowania czerwonego wyniku. Jeżeli test bywa czerwony bez powodu, należy go naprawić albo usunąć — nie „uruchomić jeszcze raz”.

## 7. Testy własności

Wszystkie omawiane dotąd testy mają wspólną słabość: sprawdzają **przypadki, które przyszły komuś do głowy**. Defekt czeka zwykle tam, gdzie nikt nie pomyślał — przy wartości granicznej, przy jednym rekordzie, przy pustej partii.

Test własności odwraca perspektywę. Zamiast podawać dane, opisujemy **jakie dane są dopuszczalne**, a biblioteka generuje z tego opisu setki przypadków i sama szuka kontrprzykładu. Gdy go znajdzie, upraszcza go do najmniejszej postaci, która wciąż psuje test — dostajemy więc nie tylko informację o błędzie, ale i minimalny przypadek do debugowania.

Dobre własności dla usługi predykcyjnej:

| Własność | Treść |
|---|---|
| **zachowanie długości** | liczba odpowiedzi równa się liczbie żądań |
| **zgodność kontraktu** | każda odpowiedź ma dokładnie wymagane pola i typy |
| **determinizm** | to samo wejście dwa razy daje ten sam wynik |
| **niezależność od kolejności** | permutacja rekordów permutuje odpowiedzi, nic więcej |

Żadna z nich nie mówi, **co** model ma przewidzieć. Wszystkie mówią, jak system ma się zachowywać — i właśnie dlatego nie trzeba ich poprawiać po każdym ponownym treningu.

Kluczowa jest tu **zgodność zakresów z kontraktem danych**, a nie ze zbiorem uczącym. Jeżeli kontrakt dopuszcza wartości od 0,05, a w zbiorze uczącym najmniejsza to 0,1, to przedział między nimi jest obszarem, którego żaden test na prawdziwych danych nigdy nie dotknie. Generator wartości granicznych trafia tam natychmiast.

## 8. Ćwiczenie praktyczne

### Cel

Napisanie zestawu testów dla celowo wadliwego projektu, wykrycie czterech defektów, naprawa kodu i doprowadzenie zestawu do stanu zielonego.

Projekt zawiera cztery ukryte defekty:

1. wyciek etykiety do zbioru cech;
2. zbyt słaby kontrakt danych — przepuszcza błędny typ i kolumnę nadmiarową;
3. model nadmiernie regularyzowany, poniżej progu jakości;
4. niezgodny kontrakt odpowiedzi usługi.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_06.ipynb`. Testy uruchamiasz jedną komendą, dokładnie tak jak zrobi to CI na zajęciach 9.

### Punkty kontrolne

1. **Test kruchy.** Uruchom kilkakrotnie test bez ustalonego ziarna. Ile razy przeszedł i dlaczego taki test szkodzi bardziej, niż pomaga?
2. **Testy zachowania.** Napisz test niezmienniczości i test kierunkowy. Który z nich wykryłby model reagujący na kolumnę techniczną?
3. **Kontrprzykład z generatora.** Wprowadź cichy filtr odrzucający rekordy przy granicy kontraktu. Które testy pozostały zielone, które sczerwieniały i do jakiej postaci `hypothesis` uprosciła kontrprzykład?
4. **Czas wykonania.** Zmierz czas zestawu i wskaż najwolniejszy test. Co zrobisz, gdy zestaw przekroczy dwie minuty?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_06/
    └── projekt/
        ├── pytest.ini
        ├── src/{features.py,contract.py,model.py,service.py}
        └── tests/{test_pipeline.py,test_behaviour.py,test_properties.py}
```

## 9. Zadanie projektowe (po zajęciach)

Zbuduj we własnym projekcie zestaw testów obejmujący pięć warstw:

1. **kod** — co najmniej dwa testy jednostkowe transformacji cech, w tym jeden przypadek brzegowy;
2. **dane** — test sprawdzający, że kontrakt odrzuca błędny typ oraz kolumnę nadmiarową;
3. **model** — test progu jakości na ustalonym zbiorze kontrolnym oraz jeden test zachowania (niezmienniczość albo kierunkowość);
4. **kontrakt** — test formatu wyjścia predykcji;
5. **własności** — co najmniej dwa testy oparte na `hypothesis`, z zakresami wynikającymi z **kontraktu danych**, nie ze zbioru uczącego.

Dodatkowo:

- testy muszą uruchamiać się **jedną komendą** i kończyć poniżej dwóch minut;
- każdy test ma czytelny komunikat błędu mówiący, co jest nie tak;
- w `README.md` opisz, przed czym chroni każda grupa testów.

**Kryterium ukończenia:** wprowadzenie do kodu jednego z czterech defektów omawianych na zajęciach powoduje czerwony wynik zestawu.

## 10. Literatura

1. pytest, **dokumentacja**:
   <https://docs.pytest.org/>
2. E. Breck i in., **The ML Test Score: A Rubric for ML Production Readiness**:
   <https://research.google/pubs/pub46555/>
3. M. Ribeiro i in., **Beyond Accuracy: Behavioral Testing of NLP Models with CheckList**:
   <https://aclanthology.org/2020.acl-main.442/>
4. J. Zhang i in., **Machine Learning Testing: Survey of Landscapes and Horizons**:
   <https://arxiv.org/abs/1906.10742>
5. Hypothesis, **testy oparte na własnościach**:
   <https://hypothesis.readthedocs.io/>
