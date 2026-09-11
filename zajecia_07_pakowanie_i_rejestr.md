# Zajęcia 7. Pakowanie modelu, rejestr i karta modelu

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 6, śledzenie eksperymentów i testy we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_07.ipynb`, lokalny rejestr modeli MLflow na bazie SQLite
- **Rezultat:** wersjonowany artefakt modelu z sygnaturą, wpis w rejestrze z aliasem, bramka jakości i karta modelu

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. wyjaśnia, z czego składa się model jako artefakt;
2. zapisuje sygnaturę wejścia i wyjścia oraz rozumie, przed czym chroni;
3. ocenia ryzyko formatów serializacji i zna bezpieczniejsze alternatywy;
4. rejestruje wersję modelu i zarządza nią przy pomocy aliasów;
5. implementuje bramkę jakości blokującą promocję gorszego modelu;
6. tworzy kartę modelu i potrafi przejść od wdrożonej wersji do kodu, danych i eksperymentu.

## 2. Model to nie plik z wagami

Plik `model.pkl` sam w sobie jest bezużyteczny. Żeby model dało się uruchomić w innym miejscu i innym czasie, artefakt musi zawierać cztery rzeczy:

| Element | Bez niego | Przykład |
|---|---|---|
| **Wagi / struktura** | nie ma czego uruchomić | wytrenowany estymator |
| **Kod transformacji** | wejście trzeba przygotować „na czuja” | `Pipeline` z `ColumnTransformer` |
| **Zależności** | model nie wczyta się w innym środowisku | lista bibliotek i wersja Pythona |
| **Sygnatura** | nie wiadomo, co podać na wejściu i co przyjdzie na wyjściu | nazwy kolumn, typy, kształt wyjścia |

Dodatkowo artefakt powinien nieść **metadane**: metryki, wersję danych, identyfikator przebiegu i commita. To one zamieniają plik w coś, o czym da się prowadzić sensowną rozmowę.

## 3. Sygnatura modelu

Sygnatura to kontrakt modelu zapisany razem z nim. Deklaruje nazwy i typy kolumn wejściowych oraz typ i kształt wyjścia.

Chroni przed trzema klasami błędów:

- **brakująca kolumna** — model dostaje trzy cechy zamiast czterech;
- **zły typ** — liczba przyszła jako tekst, bo pośrednik zserializował ją przez JSON;
- **zła kolejność** — jeżeli model operuje pozycyjnie, kolejność decyduje o wyniku (zajęcia 4).

Bez sygnatury każdy z tych błędów kończy się **cichą, błędną predykcją**. Z sygnaturą kończy się czytelnym wyjątkiem w momencie wywołania. To jest różnica między incydentem wykrytym w pierwszej minucie a wykrytym po miesiącu.

Do artefaktu warto dołączyć też **przykład wejścia** — kilka rzeczywistych wierszy. Służy jako dokumentacja i jako dane do testu dymnego po wdrożeniu.

## 4. Ryzyko formatów serializacji

Domyślny format zapisu modeli w Pythonie — `pickle`, a pod spodem także `joblib` — nie jest formatem danych. Jest **formatem programu**. Wczytanie pliku pickle oznacza wykonanie zapisanego w nim kodu.

Praktyczne konsekwencje:

- artefakt pobrany z niezaufanego źródła to to samo co uruchomienie cudzego skryptu z pełnymi uprawnieniami;
- podmiana artefaktu w magazynie jest atakiem na łańcuch dostaw, a nie „psuciem modelu”;
- skanowanie zależności nie wykryje złośliwego artefaktu, bo to nie jest pakiet.

Warianty bezpieczniejsze:

| Format | Zastosowanie | Uwaga |
|---|---|---|
| **skops** | modele scikit-learn | ładuje wyłącznie typy zadeklarowane jako zaufane |
| **ONNX** | modele przenoszone między środowiskami | graf obliczeń, bez wykonywania kodu |
| **safetensors** | wagi sieci neuronowych | wyłącznie tensory, bez kodu |

Nie chodzi o to, żeby zakazać `joblib` w projekcie studenckim. Chodzi o to, żeby **wiedzieć**, jakie ryzyko się przyjmuje, i kontrolować pochodzenie artefaktów.

## 5. Rejestr modeli

Rejestr jest katalogiem modeli oddzielonym od katalogu eksperymentów. Eksperyment odpowiada na pytanie „co próbowaliśmy”, rejestr — „co jest używane”.

Rejestr dostarcza:

- **nazwę modelu** — stabilny identyfikator dla konsumentów;
- **wersje** — kolejne numery, niezmienne po utworzeniu;
- **aliasy** — ruchome wskaźniki na wersję, np. `champion`, `challenger`;
- **tagi i opis** — metadane wersji;
- **historię zmian** — kto i kiedy przesunął alias.

### Aliasy zamiast etapów cyklu życia

Starsze wersje narzędzi używały sztywnych etapów (`Staging`, `Production`). Mechanizm ten został wycofany na rzecz **aliasów**, które są zwykłymi, dowolnie nazwanymi wskaźnikami. Powody są praktyczne: etapy były niezmiennym zbiorem, nie pozwalały na dwa modele produkcyjne obok siebie ani na własne nazewnictwo procesu.

Wzorzec, którego używamy w tym przedmiocie:

```text
candidate   → nowo zarejestrowana wersja, jeszcze nieoceniona
challenger  → wersja porównywana z obecną produkcyjną
champion    → wersja aktualnie używana przez konsumentów
```

Konsument ładuje model **po aliasie**, nie po numerze wersji. Dzięki temu zmiana wersji nie wymaga zmiany w kodzie klienta, a wycofanie sprowadza się do przesunięcia aliasu z powrotem.

## 6. Bramka jakości

Bramka jakości to warunek, który wersja musi spełnić, żeby dostać alias produkcyjny. Minimalny zestaw reguł:

1. metryka główna nie gorsza niż obecny champion (albo lepsza o zadany margines);
2. metryka nie niższa niż bezwzględny próg akceptacji;
3. komplet wymaganych metadanych: sygnatura, wersja danych, commit, metryki;
4. zielony wynik testów kontraktu.

Bramka ma być **kodem**, a nie ustaleniem. Reguła zapisana w dokumentacji zostanie ominięta w piątek o siedemnastej; reguła zapisana w funkcji, która zgłasza wyjątek, nie zostanie.

## 7. Karta modelu

Karta modelu to krótki dokument opisujący, do czego model służy i gdzie przestaje być wiarygodny. Powinna zawierać:

- **przeznaczenie** i zamierzonych użytkowników;
- **dane treningowe** — źródło, wersja, zakres czasowy;
- **wyniki** — metryki globalne oraz w istotnych podgrupach;
- **ograniczenia** — sytuacje, w których model działa źle;
- **zastosowania niezalecane** — do czego modelu używać nie wolno;
- **identyfikowalność** — wersja, przebieg, commit, suma kontrolna danych;
- **osoba odpowiedzialna** i data przeglądu.

Karta nie jest formalnością. To jedyne miejsce, w którym zapisuje się wiedzę o **granicach** modelu — a właśnie ta wiedza znika najszybciej po zakończeniu projektu.

## 8. Identyfikowalność

Zamykamy łańcuch rozpoczęty na zajęciach 3 i 5:

```text
alias champion → wersja 4 → przebieg 8f2c… → commit a1b2c3 + dane sha256:9d4e…
```

Wymaganie na ocenę 5,0 brzmi: mając wdrożoną wersję modelu, potrafisz w skończonej liczbie kroków dojść do kodu, konfiguracji, danych i eksperymentu, z których powstała. Jeżeli któreś ogniwo nie jest zapisane automatycznie, łańcuch pęknie przy pierwszym incydencie.

## 9. Ćwiczenie praktyczne

### Cel

Spakowanie modelu wraz z sygnaturą, zarejestrowanie wersji, wdrożenie bramki jakości opartej na aliasach oraz wygenerowanie karty modelu z metadanych przebiegu.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_07.ipynb`. Rejestr działa lokalnie, na bazie SQLite.

### Punkty kontrolne

1. **Sygnatura.** Podaj do modelu dane z brakującą kolumną i z błędnym typem. Jaki komunikat otrzymujesz i w którym momencie?
2. **Bramka jakości.** Zarejestruj model poniżej progu i spróbuj go promować. Co dokładnie zablokowało promocję?
3. **Przeniesienie aliasu.** Przesuń alias `champion` na inną wersję i ponownie wczytaj model po aliasie. Ile zmian trzeba było wprowadzić po stronie konsumenta?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_07/
    ├── mlflow.db
    ├── mlartifacts/
    └── reports/
        ├── model_card.md
        └── lineage.json
```

## 10. Zadanie projektowe (po zajęciach)

1. Zapisz model swojego projektu jako artefakt z **sygnaturą** i przykładem wejścia.
2. Zarejestruj wersję modelu pod stabilną nazwą.
3. Wprowadź aliasy `champion` i `challenger`; kod konsumenta ma ładować model wyłącznie po aliasie.
4. Zaimplementuj **bramkę jakości** jako funkcję zgłaszającą wyjątek przy próbie promocji modelu, który nie spełnia reguł.
5. Wygeneruj **kartę modelu** z metadanych przebiegu, a nie ręcznie.
6. Zapisz **lineage**: alias → wersja → przebieg → commit → suma kontrolna danych.
7. Opisz w dokumentacji, jakiego formatu serializacji używasz i jakie ryzyko z tym wiążesz.

**Kryterium ukończenia:** potrafisz w trzech krokach pokazać, z jakiego kodu i jakich danych powstał model wskazywany aliasem `champion`.

## 11. Literatura

1. MLflow, **Model Registry**:
   <https://mlflow.org/docs/latest/model-registry.html>
2. MLflow, **Model signatures and input examples**:
   <https://mlflow.org/docs/latest/models.html#model-signature-and-input-example>
3. skops, **bezpieczna serializacja modeli scikit-learn**:
   <https://skops.readthedocs.io/>
4. M. Mitchell i in., **Model Cards for Model Reporting**:
   <https://arxiv.org/abs/1810.03993>
5. Python, **ostrzeżenie bezpieczeństwa modułu `pickle`**:
   <https://docs.python.org/3/library/pickle.html>
