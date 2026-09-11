# Zajęcia 4. Cechy i potok przetwarzania

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 3, manifest i kontrakt danych we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_04.ipynb` uruchamiany z katalogu głównego repozytorium
- **Rezultat:** wspólna transformacja cech, test zgodności ścieżek, potok z pamięcią podręczną i definicja DAG

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. wydziela transformację cech używaną zarówno w treningu, jak i w predykcji;
2. rozpoznaje training-serving skew i pisze test, który go wykrywa;
3. wyjaśnia, dlaczego preprocessing wykonany przed podziałem danych jest wyciekiem;
4. stosuje podział czasowy tam, gdzie problem ma wymiar czasu;
5. rozbija projekt na etapy potoku z jawnymi wejściami i wyjściami;
6. rozumie idempotencję, pamięć podręczną i skutki awarii pojedynczego etapu.

## 2. Jedna transformacja, dwie ścieżki

Model widzi dane dwa razy w zupełnie innych okolicznościach:

- **podczas treningu** — cały zbiór naraz, w postaci ramki danych, offline, bez presji czasu;
- **podczas predykcji** — pojedynczy rekord albo mała paczka, często z innego systemu, w innym formacie i innej kolejności kolumn.

Jeżeli te dwie ścieżki mają dwie implementacje przygotowania cech, prędzej czy później się rozjadą. To zjawisko nazywa się **training-serving skew** i jest jedną z najczęstszych przyczyn tego, że model dobry offline zachowuje się źle po wdrożeniu.

Typowe źródła rozjazdu:

| Objaw | Przyczyna |
|---|---|
| Inne wartości cech dla tych samych danych | dwie implementacje tej samej transformacji |
| Model działa dobrze tylko dla części żądań | inna kolejność albo inne nazwy kolumn |
| Nagły spadek jakości po wdrożeniu | statystyki skalowania policzone na innym zbiorze |
| Błąd dopiero przy rzadkiej kategorii | inne kodowanie kategorii nieznanych |

Rozwiązanie jest proste w opisie i wymagające w dyscyplinie: **transformacja cech jest jednym obiektem, wersjonowanym razem z modelem**. W scikit-learn realizuje to `Pipeline` i `ColumnTransformer`, które stają się częścią artefaktu modelu. Do serwowania wrócimy na zajęciach 8, ale decyzja zapada tutaj.

> Test, który to chroni, jest krótki: weź te same dane, przepuść je ścieżką treningową i ścieżką predykcyjną, porównaj wynik. Brak takiego testu oznacza, że rozjazd wykryjesz dopiero na produkcji.

## 3. Wyciek przez przetwarzanie

Skalowanie, imputacja braków, kodowanie kategorii i selekcja cech używają **statystyk policzonych na danych**. Jeżeli policzysz je przed podziałem zbioru, informacja ze zbioru testowego przenika do treningowego, a ocena modelu przestaje być uczciwa.

Kolejność ma znaczenie:

```text
BŁĄD:      skalowanie całego zbioru → podział → trening → ewaluacja
POPRAWNIE: podział → dopasowanie transformacji na treningu → zastosowanie na teście
```

`Pipeline` rozwiązuje to automatycznie: `fit` dotyka wyłącznie danych treningowych, a `transform` stosuje zapamiętane statystyki. To kolejny powód, dla którego transformacja powinna być częścią modelu, a nie osobnym krokiem w notebooku.

## 4. Poprawność czasowa

Jeżeli problem ma wymiar czasu — prognoza, rezygnacja klienta, wykrywanie awarii — losowy podział zbioru jest błędem metodologicznym. Model uczy się na danych z przyszłości i ocenia na danych z przeszłości, czego w praktyce nigdy nie zrobi.

Poprawnie:

- **podział czasowy** — zbiór treningowy kończy się przed początkiem zbioru testowego;
- **cechy liczone wyłącznie z przeszłości** względem momentu predykcji (*point-in-time correctness*);
- **uwzględnienie opóźnienia danych** — jeżeli wartość jest znana dopiero po trzech dniach, model nie może jej użyć wcześniej.

Praktyczne pytanie kontrolne dla każdej cechy: **czy w momencie predykcji ta wartość jest już znana?** Jeżeli odpowiedź brzmi „zwykle tak”, to znaczy „czasem nie” — i trzeba to obsłużyć jawnie.

## 5. Feature store — kiedy naprawdę jest potrzebny

Feature store to system przechowujący i udostępniający cechy dwiema ścieżkami: wsadową (do treningu) i online (do predykcji o niskim opóźnieniu). Rozwiązuje realne problemy: ponowne użycie cech między zespołami, spójność obu ścieżek i poprawność czasową.

Jest potrzebny, gdy **jednocześnie** spełnione jest kilka warunków:

- kilka zespołów używa tych samych cech;
- cechy muszą być dostępne online w kilkanaście milisekund;
- cechy są kosztowne w obliczeniu i nie da się ich policzyć w locie;
- wymagana jest ścisła poprawność czasowa na dużą skalę.

W projekcie z jednym modelem, jednym autorem i predykcją wsadową feature store jest **zbędną komplikacją**. Ten sam efekt daje wspólna funkcja transformująca, wersjonowana razem z modelem. Umiejętność powiedzenia „tego nie potrzebuję i oto dlaczego” jest w tym przedmiocie oceniana tak samo wysoko jak wdrożenie narzędzia.

## 6. Potok jako graf etapów

Kod z zajęć 2 miał już etapy, ale nie miał między nimi jawnych zależności. Potok opisuje je wprost: każdy etap deklaruje, **co czyta** i **co produkuje**. Z tych deklaracji powstaje graf skierowany (DAG), który daje cztery rzeczy:

1. **kolejność wykonania** wynika z danych, a nie z pamięci autora;
2. **pamięć podręczna** — etap, którego wejścia się nie zmieniły, nie musi być liczony ponownie;
3. **lineage** — dla każdego artefaktu wiadomo, z czego powstał;
4. **kontrolowana awaria** — wiadomo dokładnie, które etapy trzeba powtórzyć.

### Idempotencja

Etap jest idempotentny, gdy powtórne uruchomienie z tymi samymi wejściami daje ten sam wynik i nie psuje stanu. To warunek, żeby ponawianie zadań (retry) miało sens. Typowe naruszenia: dopisywanie do pliku zamiast nadpisywania, użycie bieżącego czasu jako części wyniku, generowanie identyfikatorów losowych bez ziarna.

### Pamięć podręczna

Decyzja „liczyć czy pominąć” opiera się na odcisku wejść: sumach kontrolnych plików wejściowych i wartościach parametrów. Zmiana pliku danych albo parametru unieważnia wynik etapu i wszystkich etapów zależnych. To bezpośrednie zastosowanie sum kontrolnych z zajęć 3.
### DVC jako implementacja tego grafu

W przedmiocie używamy `dvc.yaml`. Każdy etap deklaruje cztery rzeczy:

| Pole | Znaczenie |
|---|---|
| `cmd` | polecenie do wykonania |
| `deps` | pliki wejściowe — ich zmiana unieważnia etap |
| `params` | konkretne klucze z `params.yaml`, nie cały plik |
| `outs` / `metrics` | pliki wyjściowe; `metrics` są dodatkowo zbierane przez `dvc metrics show` |

Rozróżnienie `deps` i `params` jest istotne: zmiana `model.max_iter` przelicza tylko trening, a zmiana `split.test_size` — podział i wszystko po nim. Gdyby cały `params.yaml` był zwykłą zależnością, każda drobna zmiana przeliczałaby wszystko.

Wynik pracy zapisuje się w **`dvc.lock`** — pliku z sumami kontrolnymi wszystkich wejść i wyjść każdego etapu. To on trafia do repozytorium obok `dvc.yaml` i to on odpowiada na pytanie, z jakich dokładnie danych i parametrów powstał dany model.

Warto też ustawić zależność etapu podziału od **raportu walidacji**. Kontrakt danych przestaje wtedy być osobnym rytuałem, a staje się bramką: dopóki walidacja nie przejdzie, dalsze etapy się nie wykonają.
### Kiedy potrzebny jest orkiestrator

Lokalny graf (np. `dvc.yaml`) wystarcza, dopóki potok uruchamia człowiek albo CI. Orkiestrator — Airflow, Dagster, Prefect — dokłada harmonogram, historię przebiegów, ponawianie, limity czasu, backfill i obsługę wielu równoległych zadań. Dla projektu zaliczeniowego lokalny graf jest właściwym wyborem; orkiestrator warto znać jako kolejny krok skali.

## 7. Ćwiczenie praktyczne

### Cel

Wydzielenie wspólnej transformacji cech wraz z testem zgodności obu ścieżek oraz zbudowanie potoku `prepare → validate → split → train → evaluate` — najpierw jako własnej pamięci podręcznej, potem jako prawdziwego projektu DVC uruchamianego przez `dvc repro`.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_04.ipynb`.

W notebooku DVC uruchamiamy z przełącznikiem `--no-scm`, żeby nie tworzyć zagnieżdżonego repozytorium. **We własnym projekcie użyj zwykłego `dvc init`.**

### Punkty kontrolne

1. **Rozjazd ścieżek.** Zmień kolejność kolumn w danych wejściowych ścieżki predykcyjnej. Który test to wykrył i dlaczego sam model nie zgłosił błędu?
2. **Awaria etapu.** Wywołaj błąd w etapie treningu. Które artefakty pozostały aktualne, a które trzeba odtworzyć po naprawie?
3. **Powtórne `dvc repro` bez zmian.** Ile etapów wykonało się ponownie i na jakiej podstawie DVC podjął tę decyzję?
4. **Zmiana parametru.** Porównaj zasięg unieważnienia po zmianie `model.max_iter` i po zmianie `split.test_size`. Dlaczego etap `prepare` nie wykonał się w żadnym z tych przypadków?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_04/
    ├── data/{iris.csv,train.csv,test.csv}
    ├── models/model.joblib
    ├── reports/{validation.json,metrics.json}
    ├── .pipeline_cache.json          # wlasna pamiec podreczna
    └── potok/                        # ten sam potok w DVC
        ├── params.yaml
        ├── dvc.yaml
        ├── dvc.lock
        ├── src/{prepare,validate,split,train,evaluate}.py
        ├── data/{iris.csv,train.csv,test.csv}
        ├── models/model.joblib
        └── reports/{validation.json,metrics.json}
```

### Co wymaga sprawdzenia przed zajęciami

- `dvc --version` odpowiada na maszynach studenckich;
- polecenie `python` w środowisku studenta wskazuje interpreter z zainstalowanymi zależnościami — to od niego zależą polecenia `cmd` w `dvc.yaml`.

## 8. Zadanie projektowe (po zajęciach)

1. Wydziel w swoim projekcie **jedną** funkcję lub obiekt budujący cechy i użyj go zarówno w treningu, jak i w ścieżce predykcyjnej.
2. Napisz **test zgodności**: te same dane wejściowe muszą dać identyczny wynik w obu ścieżkach.
3. Sprawdź, czy w twoim potoku nie ma wycieku przez przetwarzanie — czy jakakolwiek statystyka jest liczona przed podziałem zbioru.
4. Jeżeli twój problem ma wymiar czasu, zamień podział losowy na czasowy i opisz, jak zmieniły się metryki.
5. Rozbij projekt na jawne etapy opisane w `dvc.yaml`, z zadeklarowanymi `deps`, `outs`, `params` i `metrics`.
6. Ustaw walidację danych jako etap, od którego zależą etapy dalsze.
7. Wykaż działanie pamięci podręcznej: powtórne `dvc repro` bez zmian nie przelicza niczego.
8. Wykaż zasięg unieważnienia: zmiana jednego parametru przelicza wyłącznie etapy zależne.
9. Zapisz w repozytorium `dvc.lock` oraz ślad **udanego i nieudanego** przebiegu potoku.
10. Odpowiedz w dokumentacji na pytanie: czy twój projekt potrzebuje feature store? Uzasadnij decyzję.

**Kryterium ukończenia:** po zmianie jednego parametru ponowne `dvc repro` przelicza wyłącznie etapy zależne od tej zmiany, a bez żadnej zmiany nie przelicza nic.

## 9. Literatura

1. scikit-learn, **Pipelines and composite estimators**:
   <https://scikit-learn.org/stable/modules/compose.html>
2. DVC, **Data Pipelines**:
   <https://dvc.org/doc/user-guide/pipelines>
3. Google, **Rules of Machine Learning** — reguły dotyczące cech i skew:
   <https://developers.google.com/machine-learning/guides/rules-of-ml>
4. Feast, **When to use a feature store**:
   <https://docs.feast.dev/>
5. scikit-learn, **Common pitfalls — inconsistent preprocessing**:
   <https://scikit-learn.org/stable/common_pitfalls.html>
