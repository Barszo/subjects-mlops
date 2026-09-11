# Zajęcia 3. Dane: wersjonowanie, kontrakt i governance

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 2, własne repozytorium projektu
- **Środowisko:** notebook `gotowe_notebooki/zajecia_03.ipynb` uruchamiany z katalogu głównego repozytorium; wymagany dostęp do sieci i `dvc`
- **Rezultat:** dane pobrane ze źródła i objęte kontrolą wersji, manifest z sumą kontrolną, schemat kontraktu, raport walidacji i metryczka pochodzenia

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. wyjaśnia, dlaczego wersjonowanie kodu nie wystarcza do odtworzenia wyniku;
2. pobiera dane ze źródła skryptem i tworzy manifest z sumą kontrolną;
3. obejmuje dane kontrolą wersji przy użyciu DVC i odtwarza je po skasowaniu;
4. definiuje kontrakt danych i automatycznie go weryfikuje;
5. rozpoznaje trzy typowe rodzaje wycieku danych;
6. ocenia jakość etykiet jako górną granicę jakości modelu;
7. dokumentuje pochodzenie, licencję i ograniczenia użycia zbioru.

## 2. Trzy rzeczy, które trzeba wersjonować

Git wersjonuje kod. To za mało, ponieważ wynik modelu zależy od trzech niezależnie zmieniających się elementów:

| Co | Zmienia się | Typowy mechanizm |
|---|---|---|
| **Kod** | przy każdej zmianie logiki | Git |
| **Dane** | poza repozytorium, często bez powiadomienia | manifest z sumą kontrolną albo DVC |
| **Metadane przebiegu** | przy każdym uruchomieniu | narzędzie do śledzenia eksperymentów (zajęcia 5) |

Klasyczny objaw braku wersjonowania danych: „u mnie działało, a metryka spadła o pięć punktów i nikt nie wie dlaczego”. Kod jest ten sam, commit ten sam, ale plik wejściowy został po cichu podmieniony.

Duże pliki nie powinny trafiać do Git — historia repozytorium rośnie nieodwracalnie. W praktyce mamy dwa warianty:

- **Manifest** — plik JSON w repozytorium z adresem źródła, wersją i sumą kontrolną. Dane pobiera skrypt. Wariant minimalny, wystarczający dla większości projektów studenckich.
- **DVC lub odpowiednik** — narzędzie przechowujące dane w magazynie zdalnym i wersjonujące je równolegle do Git. Wariant właściwy, gdy dane zmieniają się często albo są duże.

W obu przypadkach kluczowa jest **suma kontrolna**. Bez niej nie wiadomo, czy plik pod tym samym adresem to nadal ten sam plik.

## 3. Jak działa DVC

DVC rozdziela dwie rzeczy, które Git łączy: **wskaźnik** i **zawartość**.

```text
repozytorium Git              magazyn DVC (S3, dysk, SSH)
  data/surowe.csv.dvc   ───▶   obiekt o sumie 9cc1c345…
  (kilkaset bajtów)             (właściwy plik, dowolnie duży)
```

Plik `.dvc` zawiera sumę kontrolną, rozmiar i ścieżkę — i to on podlega przeglądowi kodu oraz historii Git. Sam plik danych trafia do `.gitignore`, dopisywany tam automatycznie przez `dvc add`.

Cztery polecenia wystarczają do pełnego cyklu:

| Polecenie | Co robi |
|---|---|
| `dvc init` | tworzy katalog `.dvc` wewnątrz repozytorium Git |
| `dvc add data/surowe.csv` | przenosi plik do pamięci podręcznej i tworzy wskaźnik |
| `dvc remote add -d magazyn <adres>` | wskazuje magazyn zdalny |
| `dvc push` / `dvc pull` | wysyła zawartość do magazynu i pobiera ją z powrotem |

Sprawdzianem poprawności jest **świeży klon**: `git clone` plus `dvc pull` musi dać komplet danych. Jeżeli na tym etapie ktoś musi przesłać plik ręcznie, wersjonowanie nie działa.

Poświadczenia do magazynu **nie są wersjonowane** — trafiają do `.dvc/config.local`, który DVC sam dopisuje do `.gitignore`.

## 4. Kontrakt danych

Kontrakt danych to jawna, wykonywalna deklaracja tego, czego kod oczekuje od wejścia. Zawiera co najmniej:

- **zbiór kolumn** — także informację, że kolumn nadmiarowych być nie może;
- **typy** — z rozróżnieniem liczby, kategorii, tekstu i daty;
- **zakresy i wartości dopuszczalne** — np. wiek z przedziału 0–120, kategoria z zamkniętej listy;
- **dopuszczalność braków** — osobno dla każdej kolumny;
- **niezmienniki na poziomie zbioru** — np. minimalna liczba wierszy, unikalność klucza, rozsądny udział klas.

Kontrakt pełni trzy funkcje naraz: jest dokumentacją, testem i sygnałem alarmowym po wdrożeniu. Jego złamanie oznacza, że **zmieniło się źródło danych**, a nie że kod ma błąd. To zupełnie inna klasa incydentu i wymaga innej reakcji.

> Ta sama definicja schematu powinna działać na danych treningowych i na żądaniach przychodzących do usługi. Do tego wrócimy na zajęciach 8.

Warto rozróżnić dwa pytania, które łatwo pomylić:

| Pytanie | Odpowiada | Kiedy sygnalizuje problem |
|---|---|---|
| Czy to **ten sam plik**? | suma kontrolna | gdy ktoś podmienił dane bez uprzedzenia |
| Czy to **sensowne dane**? | kontrakt | gdy zmieniło się źródło albo sposób ich wytwarzania |

Nowa dostawa danych **ma** mieć inną sumę kontrolną, ale **musi** spełniać ten sam kontrakt. Mylenie tych dwóch kontroli prowadzi albo do fałszywych alarmów przy każdej aktualizacji, albo do przepuszczania uszkodzonych danych.

## 5. Wyciek danych

Wyciek (data leakage) występuje wtedy, gdy model podczas treningu widzi informację, której nie będzie miał w momencie predykcji. Efekt jest zawsze ten sam: znakomite metryki offline i bezużyteczny model w praktyce.

Trzy najczęstsze odmiany:

1. **Wyciek etykiety.** Cecha jest funkcją zmiennej objaśnianej albo jej bezpośrednim skutkiem. Przykłady: kolumna `data_zamknięcia_reklamacji` w modelu przewidującym reklamację, `kwota_wypłaconego_odszkodowania` w modelu ryzyka.
2. **Wyciek przez czas.** Do treningu trafiają dane z przyszłości względem momentu predykcji. Typowy błąd to losowy podział zbioru w problemie z czasem.
3. **Wyciek przez przetwarzanie.** Statystyki użyte do transformacji policzono na całym zbiorze, przed podziałem. Skalowanie, imputacja albo kodowanie kategorii wykonane przed `train_test_split` przenoszą informację ze zbioru testowego do treningowego.

Praktyczna heurystyka: **jeżeli wynik jest zaskakująco dobry, najpierw szukaj wycieku, a dopiero potem świętuj.** Model o accuracy 0,999 na realnym problemie jest podejrzany, a nie znakomity.

## 6. Jakość etykiet

Model nie może być lepszy niż etykiety, na których się uczy. Etykieta jest wynikiem czyjejś decyzji, a decyzje bywają niespójne, spóźnione albo obarczone błędem systematycznym.

Pytania, które trzeba zadać przed treningiem:

- Kto i jak nadał etykiety? Czy istniała instrukcja?
- Jaka jest zgodność między anotatorami? Jeżeli dwie osoby zgadzają się w 80% przypadków, model powyżej 80% zaczyna uczyć się szumu.
- Czy etykieta jest tym, co naprawdę nas interesuje, czy tylko jej przybliżeniem? („Kliknięcie” to nie „zadowolenie użytkownika”.)
- Ile czasu mija między zdarzeniem a nadaniem etykiety? To ograniczy monitoring po wdrożeniu (zajęcia 11–12).

## 7. Pochodzenie, licencja i dane osobowe

Każdy zbiór używany w projekcie wymaga udokumentowania:

- **źródło** — dokładny adres i data pobrania;
- **licencja** — czy wolno używać komercyjnie, czy wymagane jest wskazanie autorstwa;
- **zakres danych osobowych** — czy zbiór zawiera dane pozwalające zidentyfikować osobę, także pośrednio;
- **minimalizacja** — czy wszystkie kolumny są rzeczywiście potrzebne; kolumny zbędne należy usunąć na etapie przygotowania, a nie ignorować w modelu;
- **retencja** — jak długo dane mogą być przechowywane i co się z nimi dzieje później;
- **ograniczenia użycia** — do czego zbiór nie powinien być używany.

Wygodną formą zapisu jest **metryczka zbioru** (dataset card) — krótki plik Markdown w repozytorium. Na zajęciach 7 dołożymy do niej analogiczną kartę modelu.

## 8. Kiedy zmiana danych oznacza nową wersję modelu

Zmiana danych bywa traktowana jako „drobiazg”, bo nie widać jej w historii Git. Tymczasem konsekwencje bywają większe niż przy zmianie kodu.

Prosta reguła: **nowa wersja danych to nowa wersja modelu**, nawet jeśli kod jest bit w bit identyczny. Model musi być powiązany z konkretną wersją zbioru, inaczej nie da się odtworzyć wyniku ani wyjaśnić spadku jakości.

## 9. Ćwiczenie praktyczne

### Cel

Zbudowanie kompletnej warstwy kontroli danych: pobranie zbioru ze zdalnego źródła, manifest z sumą kontrolną, wersjonowanie przez DVC, schemat kontraktu, automatyczny raport walidacji oraz metryczka pochodzenia.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_03.ipynb`.

W notebooku DVC uruchamiamy z przełącznikiem `--no-scm`, żeby nie tworzyć zagnieżdżonego repozytorium wewnątrz repozytorium zajęć. **We własnym projekcie użyj zwykłego `dvc init`** — dopiero wtedy pliki `.dvc` są wersjonowane razem z kodem.

### Punkty kontrolne

1. **Podmieniony plik.** Zmodyfikuj jedną wartość i uruchom weryfikację manifestu. Jaki komunikat otrzymujesz i dlaczego jest to sytuacja inna niż błąd kodu?
2. **Utrata danych.** Usuń plik danych i pamięć podręczną DVC, a następnie wykonaj `dvc pull`. Czy odtworzony plik jest tym samym plikiem, czy tylko podobnym? Po czym to poznajesz?
3. **Złamany kontrakt.** Wprowadź braki, wartość poza zakresem, nową kategorię i dodatkową kolumnę. Które z tych naruszeń wykryłby zwykły `read_csv`, a które przeszłyby niezauważone aż do wyników modelu?
4. **Wyciek etykiety.** Dodaj kolumnę wyliczoną z etykiety i porównaj metryki. Który mechanizm wykrył problem szybciej: kontrakt danych czy metryka modelu?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_03/
    ├── projekt/
    │   ├── .dvc/
    │   └── data/
    │       ├── iris.csv
    │       ├── iris.csv.dvc          # wskaźnik trafiający do repozytorium
    │       └── iris.manifest.json
    ├── magazyn/                      # zdalny magazyn DVC (tu: katalog lokalny)
    └── reports/
        ├── validation_produkcyjny.json
        ├── validation_uszkodzony.json
        └── dataset_card.md
```

### Co wymaga sprawdzenia przed zajęciami

- dostęp do sieci z maszyn studenckich (pobranie zbioru po HTTPS);
- `dvc --version` odpowiada; notebook ma ścieżkę zapasową, gdy źródło zdalne jest niedostępne.

## 10. Zadanie projektowe (po zajęciach)

Dla własnego zbioru danych przygotuj:

1. **skrypt pobierający dane** ze źródła, z ponowieniem próby i czytelnym błędem przy trwałym niepowodzeniu;
2. **manifest** — źródło, data pobrania, rozmiar, liczba wierszy i kolumn, suma kontrolna;
3. **weryfikację manifestu jako pierwszy krok potoku**, zatrzymującą pracę przy niezgodności;
4. **dane pod kontrolą DVC** — `dvc init` w repozytorium, `dvc add`, skonfigurowany magazyn, wykonany `dvc push`;
5. **dowód odtwarzalności** — świeży klon repozytorium plus `dvc pull` daje komplet danych;
6. **schemat kontraktu** obejmujący wszystkie kolumny wejściowe, ich typy, zakresy, dopuszczalność braków oraz co najmniej jeden niezmiennik na poziomie zbioru;
7. **raport walidacji** zapisywany jako artefakt;
8. **metryczkę zbioru** ze źródłem, licencją, opisem kolumn, ograniczeniami jakościowymi i informacją o danych osobowych;
9. **krótką notatkę o wycieku** — wskaż co najmniej jedną kolumnę, która mogłaby być wyciekiem, i uzasadnij decyzję o jej zachowaniu albo usunięciu.

**Kryterium ukończenia:** celowa zmiana jednej wartości w pliku danych zatrzymuje potok z czytelnym komunikatem, a `dvc pull` po skasowaniu katalogu `data/` przywraca zbiór o tej samej sumie kontrolnej.

## 11. Literatura

1. Pandera, **dokumentacja walidacji danych**:
   <https://pandera.readthedocs.io/>
2. DVC, **Data Versioning**:
   <https://dvc.org/doc/use-cases/versioning-data-and-models>
3. DVC, **Remote storage**:
   <https://dvc.org/doc/user-guide/data-management/remote-storage>
4. T. Gebru i in., **Datasheets for Datasets**:
   <https://arxiv.org/abs/1803.09010>
5. S. Kaufman i in., **Leakage in Data Mining: Formulation, Detection, and Avoidance**:
   <https://dl.acm.org/doi/10.1145/2382577.2382579>
6. scikit-learn, **Common pitfalls — data leakage**:
   <https://scikit-learn.org/stable/common_pitfalls.html#data-leakage>
