# Zajęcia 2. Powtarzalne środowisko i szkielet projektu

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 1, podstawy pracy w terminalu i z Git, konto na GitHubie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_02.ipynb` uruchamiany z katalogu głównego repozytorium; `uv`, `ruff`, `git`
- **Rezultat:** mały projekt uruchamiany jedną komendą, z konfiguracją poza kodem, przypiętymi zależnościami i wysłany do zdalnego repozytorium

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. wyjaśnia, dlaczego notebook nie nadaje się na jedyną formę kodu w projekcie;
2. projektuje strukturę repozytorium oddzielającą kod, konfigurację, dane i artefakty;
3. przypina zależności i rozumie różnicę między deklaracją a plikiem blokady;
4. wyprowadza parametry z kodu do pliku konfiguracyjnego i zmiennych środowiskowych;
5. ustala ziarna losowości i zna granice powtarzalności;
6. uruchamia przygotowanie danych, trening i ewaluację jedną komendą;
7. włącza automatyczną kontrolę stylu i hak uruchamiany przed commitem;
8. zakłada zdalne repozytorium i wysyła do niego projekt.

## 2. Dlaczego notebook nie wystarcza

Notebook jest znakomitym narzędziem eksploracji i złym nośnikiem kodu produkcyjnego. Główne problemy:

- **Stan ukryty.** Wynik zależy od kolejności wykonania komórek, a nie od treści pliku. Ten sam notebook może dać dwa różne wyniki.
- **Brak jednostki wielokrotnego użytku.** Kodu z komórki nie da się zaimportować ani przetestować bez kopiowania.
- **Trudny przegląd zmian.** Różnice w formacie JSON zawierają wyniki i metadane, przez co przegląd kodu staje się nieczytelny.
- **Brak jawnego wejścia i wyjścia.** Nie wiadomo, jakie parametry przyjmuje eksperyment ani jakie artefakty wytwarza.
- **Brak sposobu uruchomienia bez człowieka.** Potok CI albo harmonogram potrzebują komendy, a nie instrukcji „uruchom wszystkie komórki”.

Notebook zostaje w projekcie, ale w roli **prezentacji wyników i eksploracji**, a nie implementacji.

> Zasada praktyczna: jeżeli fragment kodu ma zostać uruchomiony po raz drugi, powinien być funkcją w module, a nie komórką.

## 3. Struktura repozytorium projektu ML

Struktura ma czytelnie rozdzielać cztery rzeczy o różnym cyklu życia: kod, konfigurację, dane i artefakty.

```text
projekt/
├── config/
│   └── config.yaml          # parametry eksperymentu
├── data/                    # dane wejściowe (nie trafiają do Git)
├── src/
│   ├── config.py            # wczytanie konfiguracji
│   ├── pipeline.py          # prepare / train / evaluate
│   └── cli.py               # interfejs wiersza poleceń
├── artifacts/               # wyniki (nie trafiają do Git)
│   ├── models/
│   └── reports/
├── notebooks/               # eksploracja i prezentacja wyników
├── tests/
├── requirements.txt         # zadeklarowane, przypięte zależności
├── Makefile                 # zadania projektowe
├── .gitignore
└── README.md
```

Reguły, które z tego wynikają:

- **kod** jest wersjonowany w Git i podlega przeglądowi;
- **konfiguracja** jest wersjonowana, ale zmienia się częściej niż kod;
- **dane** i **artefakty** nie trafiają do Git — są odtwarzalne albo przechowywane osobno;
- katalog wyników nigdy nie jest miejscem, z którego coś się importuje.

## 4. Zależności i przypinanie wersji

Rozróżniamy dwa poziomy:

| Poziom | Co zawiera | Przykład |
|---|---|---|
| **Deklaracja** | biblioteki, których projekt faktycznie używa, wraz z dopuszczalnym zakresem wersji | `pyproject.toml`, `requirements.in` |
| **Blokada (lock)** | dokładne wersje **wszystkich** zależności, także pośrednich | `uv.lock`, `requirements.txt` z pełnym przypięciem |

Deklaracja opisuje intencję, blokada gwarantuje powtarzalność. Bez blokady projekt zainstalowany dziś i za miesiąc to dwa różne projekty.

Do przypięcia potrzebna jest jeszcze **wersja interpretera**. Kod działający na Pythonie 3.12 może nie działać na 3.14.

W tym przedmiocie ścieżką referencyjną jest `uv` z plikami `pyproject.toml`, `uv.lock` i `.python-version`. Wariant minimalny, wystarczający na ocenę 3,0, to `requirements.txt` z pełnym przypięciem oraz zapisana wersja Pythona.

Cztery polecenia, które wystarczą do pracy z `uv`:

| Polecenie | Co robi |
|---|---|
| `uv init` | tworzy `pyproject.toml` i `.python-version` |
| `uv add pandas scikit-learn` | dopisuje zależność do deklaracji i aktualizuje blokadę |
| `uv lock` | rozwiązuje drzewo zależności i zapisuje `uv.lock` |
| `uv sync` | doprowadza środowisko do stanu opisanego w blokadzie |
| `uv run python -m src.cli all` | uruchamia polecenie w tym środowisku, synchronizując je w razie potrzeby |

Rzędu wielkości warto sobie uświadomić od razu: sześć zadeklarowanych bibliotek to zwykle kilkadziesiąt pakietów w blokadzie. Te kilkadziesiąt to jest realna powierzchnia twojego projektu — zarówno pod względem powtarzalności, jak i bezpieczeństwa (wrócimy do tego na zajęciach 9).

> Pytanie kontrolne: czy potrafisz odtworzyć środowisko sprzed trzech miesięcy, mając wyłącznie zawartość repozytorium?

## 5. Konfiguracja poza kodem

Parametr zapisany w kodzie jest niewidoczny i trudny do zmiany bez modyfikacji programu. Wyprowadzenie parametrów do konfiguracji daje trzy rzeczy: jawność, możliwość porównywania eksperymentów i możliwość uruchomienia tego samego kodu w innym środowisku.

Obowiązuje prosta hierarchia źródeł, od najsłabszego do najsilniejszego:

1. wartość domyślna w kodzie;
2. plik konfiguracyjny w repozytorium;
3. zmienna środowiskowa;
4. argument wiersza poleceń.

Zmienne środowiskowe są jedynym właściwym miejscem na **sekrety**. Sekret nigdy nie trafia do pliku konfiguracyjnego w repozytorium ani do notebooka. Plik `.env` może istnieć lokalnie, ale musi znaleźć się w `.gitignore`.

Warto rozdzielić dwa rodzaje ustawień:

- **parametry eksperymentu** (ziarno, podział danych, hiperparametry) — należą do repozytorium, bo bez nich wynik jest nieodtwarzalny;
- **ustawienia środowiska** (adresy usług, ścieżki, poświadczenia) — należą do zmiennych środowiskowych, bo różnią się między komputerami.

## 6. Ziarna losowości i granice powtarzalności

Ziarno losowości ustala się wszędzie tam, gdzie występuje losowość: podział danych, inicjalizacja modelu, tasowanie, próbkowanie. Bez tego dwa uruchomienia tego samego kodu dają różne metryki i nie da się stwierdzić, czy zmiana wyniku to efekt poprawki, czy przypadku.

Ziarno nie rozwiązuje jednak wszystkiego. Powtarzalność ograniczają między innymi:

- inna wersja biblioteki lub interpretera;
- inna kolejność operacji przy przetwarzaniu równoległym;
- różnice w arytmetyce zmiennoprzecinkowej między procesorami i akceleratorami;
- zmiana danych wejściowych, o której nikt nie wie, bo dane nie są wersjonowane.

Dlatego mówimy o **powtarzalności warunkowej**: „ten sam kod, ta sama konfiguracja, te same dane i to samo środowisko dają ten sam wynik”. Każdy z tych czterech elementów musi być identyfikowalny — do danych wrócimy na zajęciach 3.

## 7. Jedna komenda uruchamiająca projekt

Projekt powinien mieć jawny, krótki interfejs uruchomieniowy, na przykład:

```bash
make prepare     # przygotowanie danych
make train       # trening modelu
make evaluate    # ewaluacja i zapis metryk
make all         # całość
```

Zalety takiego podejścia:

- README nie musi opisywać sekwencji dziesięciu kroków;
- CI wywołuje dokładnie to samo, co człowiek;
- zmiana implementacji nie zmienia sposobu uruchomienia;
- łatwo sprawdzić, czy projekt działa po świeżym klonie.

Nie ma znaczenia, czy zadania opisuje `Makefile`, skrypt, `uv run`, czy inne narzędzie. Znaczenie ma to, że **istnieje jedna udokumentowana komenda**, która wykonuje całość.

## 8. Kontrola stylu i hak przed commitem

Spór o formatowanie jest najtańszym sposobem na zmarnowanie czasu zespołu. Rozstrzyga się go raz, konfiguracją w repozytorium, i więcej do niego nie wraca.

`ruff` łączy dwie role: wykrywa błędy (nieużywane importy, przesłonięte nazwy, martwy kod) i formatuje kod. Konfiguracja należy do repozytorium — plik `ruff.toml` albo sekcja w `pyproject.toml`. Bez niej wynik zależy od wersji narzędzia zainstalowanej na danej maszynie.

```bash
ruff check src tests      # wykrywanie problemów
ruff check --fix src      # automatyczna naprawa części z nich
ruff format src tests     # formatowanie
```

Drugi element to **hak uruchamiany przed commitem**. `pre-commit` uruchamia zestaw narzędzi na plikach objętych commitem i przerywa go, gdy coś jest nie tak:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Dlaczego hak, skoro to samo zrobi CI? Bo koszt naprawy rośnie z odległością od miejsca powstania błędu. Hak kosztuje sekundy, przebieg CI — minuty, a wykrycie po scaleniu — cudzy czas.

Hak instaluje się raz na repozytorium:

```bash
pre-commit install
pre-commit run --all-files
```

Ważne: hak jest **wygodą, nie zabezpieczeniem**. Da się go pominąć (`git commit --no-verify`), więc te same kontrole muszą dziać się w CI, gdzie pominąć ich nie można.

## 9. Repozytorium zdalne

Projekt, który istnieje tylko na jednym dysku, nie jest projektem. Zdalne repozytorium daje trzy rzeczy: kopię, historię dostępną dla innych i miejsce, w którym później zamieszka potok CI.

```bash
git init
git add .
git commit -m "Szkielet projektu"
git branch -M main
git remote add origin https://github.com/<uzytkownik>/<projekt>.git
git push -u origin main
```

Zanim wykonasz pierwszy commit, sprawdź `.gitignore`. Cztery kategorie **nie mogą** trafić do repozytorium:

| Kategoria | Dlaczego |
|---|---|
| dane (`data/`) | rozmiar, licencje, dane osobowe; wersjonujemy je inaczej (zajęcia 3) |
| artefakty (`artifacts/`, `*.joblib`) | są odtwarzalne z kodu i danych; w Git tylko puchną |
| środowisko (`.venv/`, `__pycache__/`) | zależy od maszyny, odtwarzane z blokady |
| sekrety (`.env`) | raz opublikowany sekret jest sekretem spalonym |

Plik `uv.lock` **trafia** do repozytorium — bez niego blokada nie pełni swojej roli.

## 10. Ćwiczenie praktyczne

### Cel

Przekształcenie eksperymentu z zajęć 1 w mały projekt: struktura katalogów, konfiguracja w pliku YAML, moduły `config.py`, `pipeline.py` i `cli.py`, blokada zależności wygenerowana przez `uv`, kontrola stylu i uruchomienie całości jedną komendą.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_02.ipynb`. W komórkach oznaczonych jako zadanie napisz kod samodzielnie; komórka poniżej zawiera rozwiązanie ukryte magią `%%skip True`. Zajrzyj do niego dopiero po własnej próbie.

Część dotycząca Gita i GitHuba wykonywana jest **poza notebookiem**, w terminalu — notebook przygotowuje pliki i sprawdza `.gitignore`, ale nie tworzy repozytorium za ciebie.

### Punkty kontrolne

Po przejściu notebooka wykonaj i opisz w komórce Markdown:

1. **Zmiana ziarna.** Ustaw zmienną środowiskową z innym ziarnem i uruchom potok ponownie. Które metryki się zmieniły i dlaczego?
2. **Deklaracja a blokada.** Porównaj liczbę bibliotek w `pyproject.toml` z liczbą pakietów w `uv.lock`. Skąd ta różnica i co z niej wynika?
3. **Usunięcie przypięcia.** Zamień w deklaracji jedno dokładne przypięcie na zakres i wyjaśnij, jakie ryzyko wprowadzasz.
4. **Świeży klon.** Usuń katalogi `data/` i `artifacts/` projektu demonstracyjnego, a następnie uruchom jedną komendę. Czy projekt się odbudował?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_02/
    └── projekt/
        ├── config/config.yaml
        ├── src/{config.py,pipeline.py,cli.py}
        ├── data/iris.csv
        ├── artifacts/models/model.joblib
        ├── artifacts/reports/metrics.json
        ├── pyproject.toml
        ├── uv.lock
        ├── .python-version
        ├── .pre-commit-config.yaml
        ├── .gitignore
        ├── Makefile
        └── README.md
```

### Co wymaga sprawdzenia przed zajęciami

- `uv --version`, `ruff --version`, `git --version` odpowiadają na maszynach studenckich;
- studenci mają konta na GitHubie i skonfigurowany sposób uwierzytelniania (klucz SSH albo token).

## 11. Zadanie projektowe (po zajęciach)

Załóż indywidualne repozytorium projektu zaliczeniowego i doprowadź je do stanu opisanego w kamieniu milowym po zajęciach 2:

- opisany problem, użytkownik systemu i metryka sukcesu w `README.md`;
- struktura katalogów rozdzielająca kod, konfigurację, dane i artefakty;
- przypięte zależności (`pyproject.toml` + `uv.lock`) oraz zapisana wersja Pythona;
- parametry eksperymentu w pliku konfiguracyjnym, nie w kodzie;
- ustalone ziarna losowości;
- jedna udokumentowana komenda uruchamiająca przygotowanie danych, trening i ewaluację;
- `.gitignore` wykluczający dane, artefakty, środowisko i pliki `.env`;
- konfiguracja `ruff` w repozytorium i zainstalowany hak `pre-commit`;
- **projekt wysłany na GitHub**, gotowy do sklonowania.

**Kryterium ukończenia:** inna osoba klonuje repozytorium, wykonuje instrukcję z `README.md` i otrzymuje plik z metrykami bez zadawania pytań.

## 12. Literatura

1. Python Packaging Authority, **Packaging Python Projects**:
   <https://packaging.python.org/en/latest/tutorials/packaging-projects/>
2. Astral, **uv — dokumentacja**:
   <https://docs.astral.sh/uv/>
3. Astral, **ruff — dokumentacja**:
   <https://docs.astral.sh/ruff/>
4. **pre-commit — dokumentacja**:
   <https://pre-commit.com/>
5. GitHub Docs, **Adding locally hosted code to GitHub**:
   <https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github>
6. Development Containers, **specyfikacja środowiska deweloperskiego**:
   <https://containers.dev/>
7. The Twelve-Factor App, **III. Config**:
   <https://12factor.net/config>
8. scikit-learn, **Controlling randomness**:
   <https://scikit-learn.org/stable/common_pitfalls.html#controlling-randomness>
