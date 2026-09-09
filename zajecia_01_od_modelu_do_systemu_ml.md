# Zajęcia 1. Od modelu w notebooku do systemu ML

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** organizacyjno-wprowadzający z krótkim ćwiczeniem praktycznym
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** podstawy Pythona i uczenia maszynowego
- **Środowisko:** Jupyter Notebook uruchamiany w przeglądarce albo z odtwarzalnego repozytorium
- **Rezultat:** notebook zawierający kontrolę danych, model bazowy, wytrenowany model, metryki i wykresy

Dokument składa się z dwóch niezależnych części:

1. **Część I — materiały dla studentów:** teoria i instrukcja ćwiczenia.
2. **Część II — materiały dla prowadzącego:** harmonogram, przygotowanie, demonstracja i rozwiązanie referencyjne.

---

# Część I. Teoria i instrukcje dla studentów

## 1. Organizacja przedmiotu

Zajęcia mają formę krótkiego wprowadzenia teoretycznego oraz indywidualnych ćwiczeń praktycznych. Efekty ćwiczeń i kolejne wersje projektu należy przechowywać w indywidualnym repozytorium Git.

### Projekt zaliczeniowy

Projekt końcowy wykonywany jest **indywidualnie**. Każdy student:

- samodzielnie wybiera publiczny zbiór danych, np. z Kaggle lub UCI Machine Learning Repository;
- przedstawia krótką charakterystykę danych, ich źródło, licencję i ograniczenia;
- dobiera model adekwatny do problemu oraz uzasadnia wybór;
- buduje powtarzalny proces przygotowania danych, treningu i ewaluacji;
- rozwija projekt o testy, wersjonowanie, CI, sposób predykcji i monitoring zgodnie z wybranym poziomem oceny;
- indywidualnie prezentuje i broni rozwiązanie.

Projekt nie może zależeć od plików przechowywanych tylko na komputerze w sali.

### Praca na komputerach bez trwałego stanu

Na kolejnych zajęciach można otrzymać inny komputer. Dlatego:

1. repozytorium jest podstawowym źródłem kodu i dokumentacji;
2. dane muszą być małe albo możliwe do ponownego pobrania;
3. zależności powinny być zapisane i przypięte do wersji;
4. modele oraz większe wyniki należy przechowywać jako artefakty CI, w rejestrze lub w wyznaczonym magazynie;
5. na koniec zajęć należy wysłać zmiany do repozytorium;
6. nie wolno zapisywać tokenów, haseł ani innych sekretów w projekcie;
7. przed odejściem od komputera należy wylogować się ze wszystkich usług.

## 2. Cele pierwszych zajęć

Po zakończeniu zajęć student:

1. odróżnia model od kompletnego systemu ML;
2. zna podstawowy cykl życia rozwiązania ML;
3. rozumie rolę wersjonowania, powtarzalności, testowania i monitoringu;
4. potrafi wczytać oraz zweryfikować podstawowe właściwości zbioru danych;
5. potrafi utworzyć funkcję walidującą dane;
6. trenuje model bazowy oraz prosty model klasyfikacyjny;
7. oblicza metryki i tworzy wykres macierzy pomyłek;
8. zapisuje model i wyniki jako osobne artefakty.

## 3. Model ML a system ML

**Model uczenia maszynowego** jest funkcją, która na podstawie wejścia generuje predykcję. Przykładem jest klasyfikator przypisujący obserwację do jednej z klas.

**System ML** obejmuje model oraz wszystkie elementy potrzebne do regularnego i bezpiecznego dostarczania użytecznej predykcji:

- pozyskanie i walidację danych;
- przygotowanie cech;
- kod treningu i ewaluacji;
- konfigurację oraz zależności;
- przechowywanie i wersjonowanie modelu;
- usługę online albo proces predykcji wsadowej;
- integrację z innymi aplikacjami;
- monitoring, alarmy i obsługę incydentów;
- informację zwrotną oraz ponowne trenowanie;
- dokumentację, kontrolę dostępu i odpowiedzialność.

Model może osiągać dobry wynik na historycznym zbiorze testowym, a mimo to nie nadawać się do użycia. Przykładowe przyczyny:

- dane produkcyjne mają inny format niż dane treningowe;
- model używa cechy niedostępnej podczas predykcji;
- aplikacja wymaga odpowiedzi szybszej, niż potrafi dostarczyć model;
- zachowanie użytkowników zmienia się z czasem;
- wynik modelu ma inny format niż oczekuje aplikacja;
- w logach zapisywane są dane osobowe;
- nie wiadomo, która wersja modelu działa w danym momencie;
- nie istnieje procedura wycofania wadliwej wersji.

> Jakość modelu jest konieczna, ale nie wystarcza do zbudowania wartościowego i niezawodnego systemu ML.

## 4. Czym jest MLOps?

MLOps to zbiór praktyk łączących uczenie maszynowe, inżynierię oprogramowania, pracę z danymi i utrzymanie systemów. Jego celem jest uporządkowanie drogi od eksperymentu do rozwiązania działającego w sposób powtarzalny, obserwowalny i bezpieczny.

MLOps nie jest pojedynczym narzędziem. Nie każdy projekt wymaga chmury, Kubernetes ani rozbudowanej platformy. Zakres automatyzacji należy dobrać do skali, kosztu i konsekwencji błędu.

### Podstawowe zasady

1. **Wersjonowanie** — trzeba znać wersję kodu, danych, konfiguracji i modelu.
2. **Powtarzalność** — projekt powinien działać również na czystym środowisku.
3. **Automatyzacja** — częste i podatne na pomyłki czynności powinien wykonywać potok.
4. **Testowanie** — kontroli podlegają kod, dane, cechy, model i kontrakt predykcji.
5. **Obserwowalność** — po wdrożeniu należy mierzyć stan usługi, danych, predykcji oraz wynik użytkowy.
6. **Kontrolowana zmiana** — nowa wersja modelu wymaga ewaluacji, zatwierdzenia i możliwości wycofania.
7. **Identyfikowalność** — każdą wdrożoną wersję należy powiązać z kodem, danymi i eksperymentem.
8. **Bezpieczeństwo** — sekrety, dane osobowe i artefakty wymagają właściwej ochrony.

## 5. Cykl życia systemu ML

Proces ML jest cykliczny. Wyniki monitoringu i nowe dane mogą prowadzić do zmiany danych, kodu, modelu albo celu rozwiązania.

```mermaid
flowchart LR
    A[Cel i wymagania] --> B[Dane]
    B --> C[Walidacja i cechy]
    C --> D[Trening]
    D --> E[Ewaluacja]
    E --> F[Rejestr modelu]
    F --> G[Wdrożenie]
    G --> H[Predykcje]
    H --> I[Monitoring]
    I --> J[Informacja zwrotna]
    J --> B
    J --> A
```

| Etap | Przykładowy artefakt | Przykładowa automatyczna kontrola |
|---|---|---|
| Dane | wersja lub manifest danych | walidacja schematu i braków |
| Przygotowanie cech | kod transformacji | test jednostkowy transformacji |
| Trening | konfiguracja i wytrenowany model | zapis parametrów i ziarna losowości |
| Ewaluacja | metryki i wykresy | próg minimalnej jakości |
| Rejestracja | wersja modelu i metadane | sprawdzenie sygnatury modelu |
| Wdrożenie | obraz lub pakiet | test kontraktu i test uruchomienia |
| Monitoring | logi, raport lub dashboard | alert dla błędów i zmian danych |

### Rodzaje metryk

System ML należy obserwować na kilku poziomach:

- **model:** np. accuracy, precision, recall, F1 albo MAE;
- **dane:** np. liczba braków, nowe kategorie i zmiana rozkładu;
- **system:** np. czas odpowiedzi, udział błędów i przepustowość;
- **wynik użytkowy:** np. czas obsługi, koszt procesu i liczba ręcznych poprawek.

Poprawa jednej metryki modelu nie gwarantuje poprawy całego systemu. Przykładowo wyższa accuracy może ukrywać bardzo słabą jakość dla rzadkiej, lecz ważnej klasy.

## 6. Artefakty i odtwarzalność

Artefakt to zapis wejścia, ustawienia albo wyniku procesu ML. Przykładowe artefakty:

- wersja kodu;
- wersja lub manifest danych;
- plik zależności;
- konfiguracja eksperymentu;
- raport jakości danych;
- metryki i wykresy;
- wytrenowany model;
- sygnatura modelu;
- konfiguracja wdrożenia;
- karta modelu.

Dobra identyfikowalność pozwala ustalić, z jakiej wersji modelu, kodu, konfiguracji i danych pochodziła konkretna predykcja. Plik nazwany `model_final_v2.pkl` nie zawiera wystarczających informacji o swoim pochodzeniu.

## 7. Dług techniczny w systemach ML

Dług techniczny to przyszły koszt wynikający z dzisiejszych skrótów. W systemach ML jest szczególnie istotny, ponieważ działanie rozwiązania zależy zarówno od kodu, jak i od zmieniających się danych.

Przykładowe źródła długu:

- zmienne lub nieudokumentowane źródła danych;
- cechy obliczane inaczej podczas treningu i predykcji;
- ręczne przekazywanie modeli;
- parametry zapisane bezpośrednio w notebooku;
- brak testów jakości danych;
- brak informacji o środowisku i zależnościach;
- brak monitoringu jakości po wdrożeniu;
- zależność innych aplikacji od nieudokumentowanego formatu predykcji.

Notebook przygotowany podczas ćwiczenia jest eksperymentem, a nie gotowym systemem. Na kolejnych zajęciach jego elementy zostaną przeniesione do funkcji, modułów, testów i zautomatyzowanego potoku.

## 8. Ćwiczenie praktyczne: pierwszy eksperyment ML

### Cel

Utwórz indywidualny notebook `notebooks/01_pierwszy_eksperyment.ipynb`. Każde polecenie wykonaj w **osobnej komórce**. Bezpośrednio przed komórką kodu dodaj komórkę Markdown z numerem i krótkim opisem wykonywanego kroku.

Kod napisz samodzielnie. Możesz korzystać z Chatu, dokumentacji i podpowiedzi IDE. Nie proś jednak o wygenerowanie całego notebooka naraz. Rozwiązuj po jednym małym problemie, uruchamiaj wynik i sprawdzaj, czy rzeczywiście wykonuje polecenie.

Ćwiczenie nie jest częścią projektu zaliczeniowego. Służy przygotowaniu środowiska i pokazaniu artefaktów, które powstają nawet w małym eksperymencie.

### 8.1. Rekomendowany zestaw narzędzi

- **Dane:** wbudowany zbiór Iris z `sklearn.datasets.load_iris`. Nie trzeba pobierać osobnego pliku. Biblioteka zwraca dane bez dostępu do internetu.
- **Tabele i kontrola danych:** `pandas`.
- **Podział danych, modele i metryki:** `scikit-learn`.
- **Wykresy:** `matplotlib` oraz narzędzia wizualizacyjne z `sklearn.metrics`.
- **Ścieżki i katalogi:** `pathlib`.
- **Zapis metryk:** standardowa biblioteka `json`.
- **Zapis modelu:** `joblib`.

Przygotuj środowisko:

1. utwórz je poleceniem `python3 -m venv .venv`;
2. aktywuj `.venv` zgodnie z systemem operacyjnym;
3. zainstaluj zależności poleceniem `python -m pip install -r requirements-zajecia-01.txt`;
4. wybierz interpreter z `.venv` jako kernel notebooka w IDE.

Notebook powinien być uruchamiany z katalogu głównego repozytorium, aby względne ścieżki do wyników były jednoznaczne.

### 8.2. Zasada pracy z Chatem

Dobre pytanie powinno zawierać:

1. nazwę biblioteki;
2. konkretny, niewielki cel;
3. nazwy zmiennych, które już istnieją;
4. oczekiwany typ wyniku;
5. prośbę o wyjaśnienie rozwiązania.

Przykład:

> Używam pandas. Mam DataFrame `X`. Jak policzyć liczbę brakujących wartości osobno dla każdej kolumny? Wyjaśnij wynik i nie dodawaj innych etapów analizy.

Po otrzymaniu odpowiedzi:

- przeczytaj kod przed uruchomieniem;
- dopasuj nazwy zmiennych do własnego notebooka;
- uruchom komórkę;
- sprawdź typ i sens wyniku;
- jeśli pojawi się błąd, przekaż Chatowi pełny komunikat oraz kod jednej problematycznej komórki.

Nie przekazuj do publicznego Chatu haseł, tokenów, danych osobowych ani niepublicznych zbiorów danych.

### 8.3. Mikroinstrukcje do notebooka

Każdy wiersz tabeli oznacza co najmniej jedną komórkę Markdown i następującą po niej komórkę kodu.

| Nr | Polecenie do wykonania | Rekomendowane API lub pojęcie | Przykładowe pytanie do Chatu |
|---:|---|---|---|
| 1 | Zaimportuj biblioteki potrzebne do pracy z danymi, wykresami, modelami i plikami. | `pandas`, `matplotlib.pyplot`, wybrane elementy `sklearn`, `pathlib`, `json`, `joblib` | „Jakie minimalne importy są potrzebne do klasyfikacji Iris regresją logistyczną, obliczenia accuracy i macro F1 oraz zapisania wykresu?” |
| 2 | Utwórz katalogi `artifacts/zajecia_01/reports` i `artifacts/zajecia_01/models`. | `pathlib.Path`, `mkdir` | „Jak w pathlib utworzyć katalog razem z brakującymi katalogami nadrzędnymi bez błędu, gdy już istnieje?” |
| 3 | Wczytaj Iris jako obiekt zawierający ramkę danych. Utwórz zmienne `X` i `y`. | `load_iris(as_frame=True)` | „Jak wczytać Iris przez scikit-learn jako pandas DataFrame i rozdzielić cechy od etykiety?” |
| 4 | Wyświetl pięć pierwszych wierszy cech. | `DataFrame.head` | „Jak wyświetlić pierwszych pięć wierszy DataFrame `X`?” |
| 5 | Wyświetl liczbę wierszy i kolumn. | `DataFrame.shape` | „Jak odczytać osobno liczbę wierszy i kolumn z `X.shape`?” |
| 6 | Wyświetl nazwy oraz typy kolumn. | `DataFrame.dtypes` | „Jak wyświetlić nazwy i typy wszystkich kolumn DataFrame?” |
| 7 | Policz braki osobno w każdej kolumnie. | `isna`, `sum` | „Jak policzyć liczbę braków dla każdej kolumny w pandas?” |
| 8 | Policz zduplikowane wiersze. | `duplicated`, `sum` | „Jak policzyć pełne duplikaty wierszy w DataFrame, bez usuwania ich?” |
| 9 | Wyświetl statystyki opisowe cech. | `DataFrame.describe` | „Jak wygenerować statystyki opisowe dla numerycznych kolumn DataFrame?” |
| 10 | Zamień numery etykiet na nazwy gatunków i policz liczebność klas. | `target_names`, `Series.map`, `value_counts` | „Mam etykiety 0, 1, 2 i tablicę nazw klas. Jak utworzyć serię nazw i policzyć liczebność każdej klasy?” |
| 11 | Utwórz wykres słupkowy liczebności klas i zapisz go jako `class_distribution.png`. | `Series.plot.bar`, `Figure.savefig` | „Jak utworzyć wykres słupkowy z `value_counts` i zapisać go do PNG przez matplotlib?” |
| 12 | Napisz funkcję `validate_data(features, target)`, która zgłasza czytelny błąd, gdy dane nie spełniają kontraktu. | funkcja, `assert` albo `ValueError`, typy pandas | „Jak zaprojektować funkcję walidującą DataFrame i Series, która sprawdza sześć warunków i zgłasza czytelne komunikaty?” |
| 13 | Dodaj kontrole: niepusty zbiór, jednakowa liczba wierszy, cztery cechy, brak wartości pustych, numeryczne cechy i klasy `0, 1, 2`. | `empty`, `len`, `shape`, `is_numeric_dtype`, `unique` | „Jak za pomocą pandas sprawdzić, czy wszystkie kolumny DataFrame są numeryczne?” |
| 14 | Uruchom walidację na poprawnych danych. Następnie usuń kolumnę z kopii `X` i potwierdź, że funkcja zgłasza błąd. | `DataFrame.drop`, `try/except` | „Jak przetestować, że funkcja walidująca zgłasza oczekiwany błąd po usunięciu kolumny?” |
| 15 | Podziel dane na zbiory treningowy i testowy w proporcji 80/20. Zachowaj proporcje klas i ustaw ziarno `42`. | `train_test_split`, `stratify`, `random_state` | „Jak podzielić `X` i `y` przez train_test_split 80/20, ze stratyfikacją i random_state=42?” |
| 16 | Utwórz i wytrenuj klasyfikator bazowy wybierający zawsze najczęstszą klasę. | `DummyClassifier(strategy="most_frequent")` | „Jak wytrenować DummyClassifier najczęstszej klasy i wygenerować predykcje dla `X_test`?” |
| 17 | Oblicz dla modelu bazowego accuracy oraz macro F1. | `accuracy_score`, `f1_score(average="macro")` | „Jak obliczyć accuracy i macro F1 dla `y_test` oraz predykcji modelu bazowego?” |
| 18 | Zbuduj potok zawierający standaryzację cech i regresję logistyczną. Ustaw ziarno `42`. | `Pipeline`, `StandardScaler`, `LogisticRegression` | „Jak zbudować scikit-learn Pipeline: StandardScaler, potem LogisticRegression z random_state=42?” |
| 19 | Wytrenuj potok na danych treningowych i wygeneruj predykcje dla danych testowych. | `fit`, `predict` | „Jak poprawnie wytrenować Pipeline i wykonać predykcję bez dopasowywania skalera do danych testowych?” |
| 20 | Oblicz accuracy, macro F1 i raport klasyfikacji modelu właściwego. | `accuracy_score`, `f1_score`, `classification_report` | „Jak utworzyć classification_report z nazwami klas Iris?” |
| 21 | Utwórz macierz pomyłek z nazwami klas i zapisz ją jako `confusion_matrix.png`. | `ConfusionMatrixDisplay.from_predictions` | „Jak narysować i zapisać macierz pomyłek z nazwami klas przez ConfusionMatrixDisplay?” |
| 22 | Zbuduj słownik z czterema metrykami obu modeli i zapisz go jako `metrics.json`. | typ `float`, `json.dump` | „Jak bezpiecznie zapisać słownik metryk NumPy/scikit-learn do czytelnego pliku JSON?” |
| 23 | Zapisz potok modelu razem z listą nazw cech i klas jako `model.joblib`. | słownik metadanych, `joblib.dump` | „Jak zapisać Pipeline scikit-learn i metadane w jednym artefakcie joblib?” |
| 24 | Sprawdź, czy wszystkie wymagane pliki istnieją i mają rozmiar większy od zera. | `Path.exists`, `Path.stat` | „Jak sprawdzić listę ścieżek w pathlib i zgłosić błąd dla brakującego lub pustego pliku?” |
| 25 | Dodaj krótkie podsumowanie wyników w ostatniej komórce Markdown. | porównanie macro F1 | „Jak zinterpretować różnicę macro F1 między DummyClassifier i regresją logistyczną na Iris?” |

### 8.4. Kontrakt funkcji walidującej

W Markdown wystarczy określić oczekiwaną strukturę, bez gotowej implementacji:

```text
validate_data(features: DataFrame, target: Series) -> None
    sprawdź warunek 1
    sprawdź warunek 2
    ...
    jeśli warunek nie jest spełniony:
        zgłoś błąd z czytelnym komunikatem
```

### 8.5. Oczekiwana struktura artefaktów

```text
notebooks/
└── 01_pierwszy_eksperyment.ipynb
artifacts/
└── zajecia_01/
    ├── reports/
    │   ├── class_distribution.png
    │   ├── confusion_matrix.png
    │   └── metrics.json
    └── models/
        └── model.joblib
```

Ostatnia komórka notebooka powinna zawierać:

- wynik modelu bazowego;
- wynik regresji logistycznej;
- informację, który model jest lepszy według macro F1;
- jedno zdanie wyjaśniające, dlaczego sam notebook nie jest jeszcze systemem produkcyjnym.

Jeżeli pliki binarne są wykluczone z repozytorium, zapisz je jako artefakty CI lub zgodnie z instrukcją prowadzącego. Nie dodawaj dużych plików bez sprawdzenia zasad repozytorium.

## 9. Lista kontrolna przed zakończeniem zajęć

- [ ] Notebook wykonuje się od pierwszej do ostatniej komórki.
- [ ] Funkcja `validate_data` zawiera co najmniej pięć kontroli.
- [ ] Walidacja odrzuca dane z usuniętą kolumną.
- [ ] Model bazowy i regresja logistyczna zostały wytrenowane.
- [ ] Zapisano `metrics.json`.
- [ ] Zapisano dwa wykresy.
- [ ] Zapisano model albo świadomie wykluczono go zgodnie z instrukcją.
- [ ] Notebook zawiera krótkie podsumowanie.
- [ ] Zmiany zostały wysłane do indywidualnego repozytorium.
- [ ] Student wylogował się z usług na komputerze współdzielonym.

## 10. Literatura

1. D. Sculley i in., **Hidden Technical Debt in Machine Learning Systems**, NeurIPS 2015:
   <https://papers.neurips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems>
2. Google Cloud, **MLOps: Continuous delivery and automation pipelines in machine learning**:
   <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning>
3. Google Cloud, **Practitioners Guide to MLOps**:
   <https://cloud.google.com/resources/mlops-whitepaper>
4. scikit-learn, **Iris dataset**:
   <https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html>

---

# Część II. Instrukcje dla prowadzącego

## 11. Cele organizacyjne

Pierwsze spotkanie powinno:

1. przedstawić zasady przedmiotu i indywidualnego projektu zaliczeniowego;
2. wyjaśnić sposób pracy na komputerach bez trwałego stanu;
3. zweryfikować dostęp studentów do repozytoriów oraz środowiska notebookowego;
4. zbudować wspólną intuicję dotyczącą różnicy między modelem i systemem ML;
5. uruchomić krótki eksperyment, ale nie obciążać studentów rozbudowanym zadaniem.

Ćwiczenie ma charakter wdrożeniowy i praktyczny. Nie należy wymagać od studentów tworzenia opisowych analiz ryzyka, diagramów ani odpowiedzi sprawdzających zapamiętanie teorii.

## 12. Przygotowanie przed zajęciami

Prowadzący powinien przygotować:

- repozytorium szablonowe z notebookiem `notebooks/01_pierwszy_eksperyment.ipynb`;
- plik `requirements-zajecia-01.txt` zawierający biblioteki używane przez notebook;
- krótką instrukcję odtworzenia środowiska;
- działające środowisko przeglądarkowe albo zapasowy wariant lokalny;
- możliwość tworzenia indywidualnego repozytorium przez każdego studenta;
- przykładowe repozytorium pokazujące oczekiwaną strukturę;
- rozwiązanie referencyjne `gotowe_notebooki/zajecia_01_pierwszy_eksperyment_rozwiazanie.ipynb`, niewidoczne dla studentów do czasu zakończenia ćwiczenia;
- awaryjną kopię danych Iris w repozytorium, jeśli środowisko nie zawiera `scikit-learn`.

Przed zajęciami należy sprawdzić proces na czystym środowisku, używając tych samych uprawnień co student.

## 13. Proponowany harmonogram 90 minut

| Czas | Etap | Działanie |
|---:|---|---|
| 0–15 min | Organizacja | Zasady przedmiotu, indywidualny projekt, oceny i komunikacja |
| 15–25 min | Środowisko | Logowanie, utworzenie repozytorium i wyjaśnienie pracy bez trwałego dysku |
| 25–40 min | Teoria | Model a system, cykl życia i podstawowe zasady MLOps |
| 40–50 min | Demonstracja | Model o dobrej accuracy, który nie spełnia wymagań systemu |
| 50–55 min | Instrukcja | Omówienie notebooka i wymaganych artefaktów |
| 55–82 min | Ćwiczenie | Indywidualna praca z notebookiem |
| 82–88 min | Weryfikacja | Uruchomienie całego notebooka i zapis wyników |
| 88–90 min | Zamknięcie | Wysłanie zmian, wylogowanie i zapowiedź kolejnych zajęć |

Jeśli część organizacyjna potrwa dłużej, minimalny wariant ćwiczenia obejmuje wczytanie danych, funkcję `validate_data`, model bazowy, regresję logistyczną i zapis `metrics.json`. Wykresy można dokończyć samodzielnie albo na początku kolejnych zajęć.

## 14. Wprowadzenie teoretyczne

Warto skoncentrować się na czterech tezach:

1. model stanowi tylko jeden element rozwiązania;
2. wynik offline nie gwarantuje działania po wdrożeniu;
3. kod, dane, konfiguracja i model muszą być identyfikowalne;
4. proces powinien być możliwy do odtworzenia na innym komputerze.

Nie ma potrzeby szczegółowego omawiania wszystkich narzędzi. Ich praktyczne zastosowanie pojawi się na kolejnych spotkaniach.

### Pytanie otwierające

> Czy model klasyfikacyjny osiągający accuracy równą 0,92 jest gotowy do wdrożenia?

Pytanie służy rozpoczęciu dyskusji. Nie jest zadaniem ocenianym.

## 15. Demonstracja prowadzącego

### Cel

Pokazać, że pojedyncza metryka modelu nie opisuje gotowości całego systemu.

### Przebieg

1. Pokaż wynik klasyfikatora: `accuracy = 0,92`.
2. Pokaż rozkład klas, w którym klasa krytyczna stanowi 2% danych.
3. Pokaż recall równy 0,35 dla klasy krytycznej.
4. Ujawnij, że jedna cecha jest dostępna dopiero po zdarzeniu przewidywanym przez model.
5. Pokaż wymaganie czasu odpowiedzi poniżej 200 ms i pomiar wynoszący 900 ms.
6. Pokaż przykład logu zawierającego dane osobowe.
7. Przypisz każdy problem do danych, modelu, integracji albo eksploatacji.

Demonstracja powinna trwać maksymalnie 10 minut. Jej celem jest zbudowanie intuicji, a nie sprawdzenie wiedzy studentów.

## 16. Wskazówki do ćwiczenia

### Zakres pomocy

Prowadzący może:

- pomóc uruchomić środowisko i notebook;
- wyjaśnić komunikat błędu;
- wskazać odpowiednią bibliotekę, klasę albo funkcję;
- wskazać dokumentację funkcji;
- pomóc studentowi podzielić problem na mniejsze pytania do Chatu;
- pomóc sprawdzić, czy artefakt został zapisany.

Student powinien samodzielnie:

- uzupełnić funkcję walidującą;
- uruchomić kontrolę danych;
- wytrenować oba modele;
- obliczyć metryki;
- wygenerować wykresy;
- zapisać i wysłać własny notebook.

### Typowe problemy

| Problem | Sposób reakcji |
|---|---|
| Brak pakietu | użyć przygotowanego pliku zależności lub środowiska zapasowego |
| Błędna ścieżka zapisu | sprawdzić katalog roboczy przez `Path.cwd()` |
| Notebook uruchomiono w złej kolejności | wykonać `Restart Kernel and Run All` |
| Wykres nie został zapisany | utworzyć katalog `reports` i wywołać `savefig` przed `close` |
| Walidacja nie zgłasza błędu | uruchomić funkcję na kopii danych bez jednej kolumny |
| Brak możliwości wysłania dużego modelu | zapisać model jako artefakt CI albo pominąć go zgodnie z instrukcją |

## 17. Rozwiązanie referencyjne

Pełne rozwiązanie znajduje się w pliku:

`gotowe_notebooki/zajecia_01_pierwszy_eksperyment_rozwiazanie.ipynb`

Notebook dla prowadzącego:

- ma osobną komórkę Markdown i osobną komórkę kodu dla każdej mikroinstrukcji;
- zawiera działającą funkcję `validate_data`;
- pokazuje zarówno poprawne, jak i niepoprawne wywołanie walidacji;
- trenuje model bazowy oraz potok regresji logistycznej;
- zapisuje oba wykresy, metryki i model;
- weryfikuje utworzone artefakty;
- kończy się interpretacją wyników.

Wyniki mogą nieznacznie różnić się między wersjami bibliotek, ale regresja logistyczna powinna wyraźnie przewyższać klasyfikator wybierający zawsze najczęstszą klasę.

Podczas sprawdzania należy zwrócić uwagę, czy:

- dane podzielono ze stałym `random_state` i `stratify=y`;
- model bazowy trenowano wyłącznie na danych treningowych;
- preprocessing znajduje się w tym samym `Pipeline` co model;
- macro F1 obliczono z parametrem `average="macro"`;
- model zapisano razem z nazwami cech i klas;
- wszystkie wymagane pliki istnieją i nie są puste;
- notebook wykonuje się od początku do końca po ponownym uruchomieniu kernela.

## 18. Kryteria ukończenia ćwiczenia

Ćwiczenie ma charakter formatywny. Nie sprawdza wiedzy opisowej.

| Element praktyczny | Warunek ukończenia |
|---|---|
| Kontrola danych | notebook pokazuje strukturę, braki, duplikaty i liczebność klas |
| Funkcja | `validate_data` wykonuje co najmniej pięć kontroli i odrzuca błędny zbiór |
| Modele | wytrenowano model bazowy i regresję logistyczną |
| Ewaluacja | obliczono accuracy, macro F1 i raport klasyfikacji |
| Wizualizacja | zapisano rozkład klas i macierz pomyłek |
| Artefakty | zapisano metryki oraz model z metadanymi |
| Powtarzalność | notebook wykonuje się od początku do końca |
| Trwałość pracy | wynik znajduje się w indywidualnym repozytorium |

Nie należy obniżać wyniku za niedokończone elementy, jeśli zabrakło czasu z powodu spraw organizacyjnych lub problemów ze wspólną infrastrukturą.

## 19. Po zajęciach

Prowadzący powinien:

1. potwierdzić, że każdy student ma indywidualne repozytorium;
2. zebrać problemy z odtwarzaniem środowiska przed drugim spotkaniem;
3. udostępnić rozwiązanie referencyjne po terminie oddania;
4. przypomnieć, że na drugich zajęciach notebook zostanie przekształcony w powtarzalny szkielet projektu;
5. upewnić się, że studenci wylogowali się z komputerów współdzielonych.
