# Zajęcia 13. Prezentacje projektów i przegląd produkcyjny

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** prezentacje, demonstracja i wzajemny przegląd
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończony projekt zaliczeniowy, wersja oznaczona tagiem
- **Środowisko:** notebook `gotowe_notebooki/zajecia_13.ipynb` z listą kontrolną i losowaniem scenariusza awarii
- **Rezultat:** wersja projektu z tagiem, prezentacja, protokół demonstracji i przegląd cudzego projektu

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. demonstruje działanie projektu od świeżego klonu albo przez przebieg CI;
2. uzasadnia decyzje architektoniczne i wskazuje ich koszt;
3. reaguje na nieznany wcześniej scenariusz awarii;
4. przeprowadza rzeczowy przegląd cudzego projektu;
5. formułuje wnioski z całego przedmiotu.

## 2. Przed zajęciami

Na tydzień przed prezentacją każdy student:

1. oznacza wersję projektu tagiem (`v1.0` albo równoważnym) — od tego momentu prezentowana jest **ta** wersja;
2. uruchamia listę kontrolną z notebooka i naprawia to, co się da;
3. przygotowuje prezentację na 6–8 minut;
4. sprawdza, że demonstracja działa **na innym komputerze** albo w przebiegu CI.

Niedziałająca demonstracja może zostać zastąpiona pełnym zapisem udanego przebiegu CI, jeżeli awaria nie wynika z projektu. Dotyczy to problemów ze sprzętem albo siecią, nie błędów w kodzie.

## 3. Przebieg prezentacji

Na jednego studenta przypada około 12 minut.

| Czas | Element | Na czym się skupić |
|---|---:|---|
| Prezentacja | 6–8 min | problem, dane, decyzje, kompromisy |
| Demonstracja | 2 min | świeży klon albo przebieg CI |
| Scenariusz awarii | 2 min | wykrycie, diagnoza, reakcja |
| Pytanie prowadzącego | 1–2 min | zrozumienie całości przepływu |

### Czego oczekujemy w prezentacji

- **problem i użytkownik** — kto i po co używa systemu, jaka jest metryka sukcesu;
- **dane** — źródło, licencja, ograniczenia, największa trudność;
- **decyzje** — co wybrałeś i **czego świadomie nie zrobiłeś**;
- **koszt** — co ta architektura kosztuje w utrzymaniu;
- **ograniczenia** — kiedy model nie jest wiarygodny.

Nie oczekujemy: przeglądu użytych bibliotek, listy commitów ani przechwalania się metryką. Rozwiązanie proste i uzasadnione jest oceniane wyżej niż rozbudowane i nieuzasadnione.

> Zdanie „nie użyłem feature store, bo mam jeden model i predykcję wsadową" jest lepszą odpowiedzią niż wdrożony i nieużywany feature store.

## 4. Demonstracja powtarzalności

Demonstracja odpowiada na jedno pytanie: **czy to działa poza twoim komputerem**. Dopuszczalne warianty:

1. świeży klon repozytorium i uruchomienie jedną komendą;
2. przebieg CI wykonany na czystym runnerze, pokazany od początku do końca;
3. uruchomienie kontenera zbudowanego z repozytorium.

Nie jest demonstracją: notebook z zapisanymi wynikami sprzed tygodnia ani „u mnie działa, pokażę na swoim".

## 5. Game day — scenariusz awarii

Każdy student losuje jeden scenariusz. Losowanie jest jawne i powtarzalne — notebook wyznacza scenariusz na podstawie identyfikatora studenta, więc nikt nie może zarzucić stronniczości.

Oceniamy trzy rzeczy, w tej kolejności:

1. **Wykrycie** — po czym poznałbyś, że to się dzieje? Czy twój monitoring by to pokazał?
2. **Diagnoza** — jak ustaliłbyś przyczynę? Które artefakty sprawdzisz i w jakiej kolejności?
3. **Reakcja** — co robisz natychmiast, a co dopiero po ustaleniu przyczyny?

Nie oceniamy tego, czy scenariusz został wcześniej przewidziany. Oceniamy, czy zbudowany system daje **narzędzia do reakcji**.

### Pula scenariuszy

1. Plik z danymi wejściowymi został podmieniony i ma inną liczbę kolumn.
2. Jedna kolumna zmieniła jednostkę — wartości są dziesięciokrotnie większe.
3. Model poniżej progu jakości został promowany przez pomyłkę.
4. Rejestr modeli jest niedostępny w momencie startu usługi.
5. Sekret używany przez usługę wygasł.
6. Opóźnienie p99 wzrosło pięciokrotnie bez zmiany w kodzie.
7. Rozkład danych wejściowych przesunął się, ale metryka jakości nie spadła.
8. Etykiety nie napłynęły przez dwa okresy raportowe.
9. Konsument zgłasza, że odpowiedź ma inny format niż w dokumentacji.
10. Ponowny trening wytrenował model na danych z okresu awarii.

## 6. Wzajemny przegląd

Każdy student ocenia jeden cudzy projekt według tej samej listy. Przegląd ma być **konkretny**: zamiast „dokumentacja mogłaby być lepsza" — „w README brakuje informacji, skąd pobrać dane".

Zakres przeglądu:

- czy udało się odtworzyć wynik wyłącznie na podstawie `README.md`;
- czy da się wskazać, z jakich danych i kodu powstał wdrożony model;
- czy testy chronią przed czymś realnym;
- czy w repozytorium nie ma danych ani sekretów, których być nie powinno;
- jedna rzecz zrobiona dobrze i jedna do poprawy.

Wynik przeglądu trafia do repozytorium ocenianego projektu jako plik albo zgłoszenie.

## 7. Retrospektywa przedmiotu

Na koniec wracamy do pytania z pierwszych zajęć: *czy model o accuracy 0,92 jest gotowy do wdrożenia?*

Warto zebrać odpowiedzi na trzy pytania:

- **Co okazało się trudniejsze, niż wyglądało?** Zwykle: kontrakty danych i wycofanie zmiany.
- **Co dało największy zwrot przy najmniejszym nakładzie?** Zwykle: uruchomienie jedną komendą, testy progu jakości i manifest danych.
- **Czego nie zrobiłbyś ponownie?** Zwykle: narzędzie wdrożone, bo „tak się robi", bez roli w projekcie.

## 8. Ćwiczenie praktyczne

### Cel

Przygotowanie się do obrony: automatyczna lista kontrolna projektu, lista dowodów do sprawdzenia na GitHubie, wylosowanie scenariusza awarii, protokół demonstracji i formularz przeglądu.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_13.ipynb`. Listę kontrolną uruchamiasz na **swoim** repozytorium — notebook przyjmuje ścieżkę jako parametr.

Lista obejmuje dziewięć obszarów odpowiadających kolejnym spotkaniom: podstawy, środowisko, dane, CI, kontener, wdrożenie, obserwowalność, governance i stan repozytorium Git.

### Czego automat nie sprawdzi

Automat potrafi stwierdzić, że plik **istnieje**. Nie potrafi stwierdzić, że jest **prawdziwy**. `Dockerfile` może istnieć i się nie budować; workflow może istnieć i nigdy nie przejść; runbook może opisywać procedurę, której nikt nie wykonał.

Dlatego druga część listy to **dowody** sprawdzane w przeglądarce:

| Dowód | Gdzie szukać |
|---|---|
| reguła ochrony `main` z wymaganym przebiegiem | Settings → Branches |
| ostatni przebieg CI na `main` zakończony powodzeniem | Actions |
| zgłoszenie zmiany zablokowane przez czerwony przebieg | Pull requests |
| opublikowany obraz wraz z digestem | Packages |
| wdrożenie produkcyjne za bramką zatwierdzenia | Actions → `cd` |
| zmierzony czas wycofania | sprawozdanie |

Ostatni wiersz jest najważniejszy. Procedura wycofania, której nigdy nie wykonano, jest wypracowaniem, nie procedurą.

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_13/
    └── reports/
        ├── project_checklist.csv
        ├── evidence_checklist.csv
        ├── demo_protocol.md
        └── peer_review.md
```

## 9. Warunki zaliczenia — przypomnienie

- projekt działa z repozytorium albo przez CI, bez dostępu do poprzedniego komputera;
- instrukcja odtworzenia została sprawdzona przez inną osobę;
- dane i komponenty mają wskazane źródło oraz licencję;
- w historii Git nie ma sekretów, danych osobowych ani dużych plików binarnych;
- student samodzielnie prezentuje projekt i rozumie cały przepływ;
- korzystanie z asystentów AI jest dozwolone, ale każdą linijkę trzeba umieć wyjaśnić;
- poważny błąd metodologiczny, wyciek danych albo brak możliwości odtworzenia wyniku ogranicza ocenę do 3,0 do czasu poprawy.

## 10. Literatura

1. Google SRE Workbook, **Disaster Role Playing** — ćwiczenia typu game day:
   <https://sre.google/workbook/incident-response/>
2. Google SRE Book, **Postmortem Culture**:
   <https://sre.google/sre-book/postmortem-culture/>
3. E. Breck i in., **The ML Test Score** — lista kontrolna gotowości produkcyjnej:
   <https://research.google/pubs/pub46555/>
4. M. Mitchell i in., **Model Cards for Model Reporting**:
   <https://arxiv.org/abs/1810.03993>
