# Zajęcia 5. Śledzenie eksperymentów i wybór modelu

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 4, działający potok we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_05.ipynb`, lokalny serwer śledzenia MLflow na bazie SQLite
- **Rezultat:** seria kontrolowanych eksperymentów, tabela porównawcza i udokumentowany wybór modelu

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. zapisuje parametry, metryki, tagi i artefakty każdego przebiegu;
2. wiąże przebieg z wersją kodu, danych i środowiska;
3. stosuje podział na trzy zbiory i wyjaśnia rolę każdego z nich;
4. definiuje kryterium wyboru modelu **przed** rozpoczęciem eksperymentów;
5. rozpoznaje optymistyczne obciążenie wynikające z wyboru modelu na zbiorze testowym;
6. porównuje przebiegi i uzasadnia decyzję na podstawie danych, a nie wrażenia.

## 2. Dlaczego notowanie wyników ręcznie nie działa

Typowy przebieg pracy bez narzędzia: uruchomienie notebooka, zapisanie wyniku w arkuszu, zmiana parametru, kolejne uruchomienie. Po tygodniu nikt nie potrafi odpowiedzieć na pytanie, którym kodem i na jakich danych powstał wynik z wiersza siódmego.

Konkretne braki:

- **brak kontekstu** — arkusz zawiera metrykę, ale nie wersję kodu, danych ani biblioteki;
- **brak artefaktów** — model, który dał najlepszy wynik, został nadpisany;
- **selektywne notowanie** — nieudane przebiegi znikają, więc obraz jest zafałszowany;
- **brak porównywalności** — dwa przebiegi różnią się trzema rzeczami naraz;
- **brak odtwarzalności** — nie da się powtórzyć przebiegu sprzed miesiąca.

Narzędzie do śledzenia eksperymentów rozwiązuje to jednym mechanizmem: **każde uruchomienie zostawia trwały, kompletny ślad**, niezależnie od tego, czy wynik był dobry.

## 3. Co zapisuje przebieg

| Element | Przykład | Po co |
|---|---|---|
| **Parametry** | `C=0.5`, `max_iter=500`, `test_size=0.2` | żeby wiedzieć, co zmieniono |
| **Metryki** | `f1_macro=0.94`, `accuracy=0.95`, `fit_seconds=0.8` | żeby porównać wyniki |
| **Tagi** | `data_version=1.0.0`, `git_commit=a1b2c3`, `author=...` | żeby odtworzyć kontekst |
| **Artefakty** | model, wykres, raport walidacji, plik metryk | żeby nie stracić wyniku |
| **Środowisko** | wersja Pythona i bibliotek | żeby wiedzieć, gdzie to działało |

Szczególne znaczenie ma powiązanie przebiegu z **wersją danych** (suma kontrolna z zajęć 3) i **wersją kodu** (identyfikator commita). Bez tych dwóch tagów nie da się zamknąć łańcucha identyfikowalności, którego wymaga ocena 5,0.

### Logowanie ręczne i automatyczne

Automatyczne logowanie zapisuje parametry i metryki bez pisania kodu. Jest wygodne na start, ale nie zna kontekstu biznesowego — nie zapisze wersji danych ani metryki, którą naprawdę mierzysz. W praktyce łączy się oba podejścia: automatyczne dla szczegółów technicznych, ręczne dla tego, co istotne dla decyzji.

## 4. Trzy zbiory, trzy różne role

| Zbiór | Kiedy używany | Rola |
|---|---|---|
| **treningowy** | wielokrotnie | dopasowanie parametrów modelu |
| **walidacyjny** | wielokrotnie | wybór modelu i hiperparametrów |
| **testowy** | **raz**, na końcu | oszacowanie jakości modelu, który już wybrano |

Zbiór testowy jest zasobem jednorazowym. Każde spojrzenie na niego w celu podjęcia decyzji zamienia go w kolejny zbiór walidacyjny, a jego wynik przestaje być bezstronnym oszacowaniem.

To najczęstszy błąd metodologiczny w projektach studenckich: dwadzieścia konfiguracji porównanych na zbiorze testowym i wybrana najlepsza. Wynik takiego wyboru jest **zawyżony**, bo najlepszy wynik z dwudziestu prób zawiera składnik szczęścia. Przy małych zbiorach różnica potrafi wynieść kilka punktów procentowych.

Alternatywą przy małych danych jest walidacja krzyżowa na zbiorze treningowo-walidacyjnym, z zachowaniem osobnego zbioru testowego.

## 5. Kryterium wyboru przed eksperymentem

Kryterium wyboru modelu należy zapisać **zanim** zobaczy się wyniki. Inaczej nieuchronnie zostanie dobrane do wyniku, który akurat wyszedł najlepiej.

Dobre kryterium jest jednoznaczne i rozstrzygalne, na przykład:

> Wybieram model o najwyższym macro F1 na zbiorze walidacyjnym. Przy różnicy mniejszej niż 0,01 wybieram model prostszy. Model musi przewidywać pojedynczy rekord poniżej 50 ms i przewyższać model bazowy o co najmniej 0,05 macro F1.

Zwróć uwagę na trzy elementy: **metrykę główną**, **regułę rozstrzygania remisów** i **warunki brzegowe** (koszt, opóźnienie, minimalna przewaga nad baseline).

### Metryki techniczne i biznesowe

Metryka techniczna mierzy model, metryka biznesowa mierzy wartość systemu. Accuracy 0,95 nic nie znaczy, jeżeli klasa krytyczna stanowi 2% danych, a jej pominięcie kosztuje tysiąc razy więcej niż fałszywy alarm. Warto zapisywać obie i decydować na podstawie tej, która odpowiada celowi projektu.

## 6. Porównywalność eksperymentów

Eksperyment jest **kontrolowany**, gdy między dwoma przebiegami zmienia się dokładnie jedna rzecz. Jeżeli zmieniasz jednocześnie model, sposób podziału danych i zestaw cech, wynik nie odpowiada na żadne pytanie.

Warunki porównywalności:

- ten sam podział danych (to samo ziarno);
- ta sama wersja danych;
- ta sama metryka liczona w ten sam sposób;
- zapisana informacja o tym, co zostało zmienione.

Do tego dochodzi **szum losowy**. Różnica 0,003 macro F1 między dwoma modelami na zbiorze 30 obserwacji nie jest różnicą, tylko wahaniem. Warto uruchomić ten sam wariant z kilkoma ziarnami i patrzeć na rozrzut, zamiast traktować pojedynczą liczbę jak wyrocznię.

## 7. Ćwiczenie praktyczne

### Cel

Wykonanie serii kontrolowanych eksperymentów z pełnym zapisem kontekstu, zbudowanie tabeli porównawczej i wybór modelu według kryterium zdefiniowanego wcześniej.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_05.ipynb`. Serwer śledzenia działa lokalnie, na bazie SQLite w katalogu artefaktów — nie wymaga konta ani połączenia z usługą zewnętrzną.

Interfejs graficzny możesz uruchomić poleceniem:

```bash
mlflow ui --backend-store-uri sqlite:///artifacts/zajecia_05/mlflow.db
```

### Punkty kontrolne

1. **Wybór na zbiorze testowym.** Porównaj model wybrany według zbioru walidacyjnego z modelem wybranym według testowego. O ile różni się deklarowana jakość od rzeczywistej?
2. **Powtarzalność przebiegu.** Uruchom tę samą konfigurację dwa razy, a następnie raz bez ustalonego ziarna. Jak duży jest rozrzut i co to oznacza dla porównywania modeli?
3. **Autologowanie.** Włącz automatyczne logowanie i sprawdź, ile parametrów zostało zapisanych bez twojego udziału. Czego wśród nich brakuje?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_05/
    ├── mlflow.db
    ├── mlartifacts/
    └── reports/
        ├── comparison.csv
        └── selection.md
```

## 8. Zadanie projektowe (po zajęciach)

1. Podłącz śledzenie eksperymentów do własnego potoku — każde uruchomienie treningu ma zostawiać ślad.
2. Zapisz w każdym przebiegu tagi: wersję danych (suma kontrolna z zajęć 3), identyfikator commita i wersje kluczowych bibliotek.
3. Wprowadź podział na trzy zbiory albo walidację krzyżową z osobnym zbiorem testowym.
4. Zapisz kryterium wyboru modelu w dokumentacji **przed** wykonaniem eksperymentów.
5. Wykonaj co najmniej trzy kontrolowane eksperymenty, w tym model bazowy.
6. Wygeneruj tabelę porównawczą i dołącz ją do repozytorium.
7. Napisz krótkie uzasadnienie wyboru odwołujące się do kryterium, a nie do wrażenia.

**Kryterium ukończenia:** dla wybranego modelu potrafisz wskazać przebieg, parametry, wersję danych i commit, z którego powstał.

## 9. Literatura

1. MLflow, **Tracking**:
   <https://mlflow.org/docs/latest/tracking.html>
2. MLflow, **Models — signatures i input examples**:
   <https://mlflow.org/docs/latest/models.html>
3. scikit-learn, **Cross-validation**:
   <https://scikit-learn.org/stable/modules/cross_validation.html>
4. C. Huyen, **Designing Machine Learning Systems**, rozdział o ewaluacji offline.
5. G. Varoquaux, **Cross-validation failure: small sample sizes lead to large error bars**:
   <https://doi.org/10.1016/j.neuroimage.2017.06.061>
