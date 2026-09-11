# Plan tematyczny przedmiotu „Techniki MLOps”

## 1. Założenia organizacyjne

- **Wymiar zajęć:** 13 spotkań po 90 minut.
- **Forma zaliczenia:** indywidualny projekt końcowy z krótką prezentacją i obroną.
- **Założenia wstępne:** podstawowa znajomość Pythona, Git, uczenia maszynowego i pracy w terminalu.
- **Stan aktualności planu:** wrzesień 2026 r. Narzędzia są przykładami realizacji praktyk, a nie celem przedmiotu.

### Czteroetapowy przebieg pracy

Każde spotkanie ma tę samą, powtarzalną strukturę. Studenci wiedzą, czego się spodziewać, a materiał każdego tygodnia przechodzi tę samą drogę: od pojęcia, przez przykład referencyjny, do zastosowania we własnym projekcie.

| Etap | Kiedy | Kto pracuje | Opis |
|---|---|---|---|
| **1. Teoria** | na zajęciach | prowadzący | Omówienie zagadnień, pojęć i decyzji projektowych |
| **2. Demonstracja** | na zajęciach | prowadzący | Przejście przez przygotowany materiał referencyjny i pokazanie kluczowych fragmentów |
| **3. Ćwiczenie prowadzone** | na zajęciach | student | Samodzielne przejście przez ten sam materiał: uruchamianie, modyfikowanie, sprawdzanie hipotez |
| **4. Własny projekt** | po zajęciach | student | Przeniesienie techniki na własne dane i własne repozytorium |

**Etap 3 nie polega na pisaniu kodu od zera.** Materiał referencyjny zawiera kompletne, działające rozwiązanie wraz z komentarzem. Zadaniem studenta jest je uruchomić, zrozumieć i celowo zepsuć w wyznaczonych miejscach, aby zobaczyć, co dany mechanizm faktycznie wykrywa. Każdy materiał zawiera 2–4 oznaczone punkty kontrolne typu „zmień to i wyjaśnij, dlaczego test przestał przechodzić”.

**Etap 4 realizowany jest po zajęciach** i to on decyduje o ocenie końcowej. Student pracuje na własnym zbiorze danych, nie na przykładowym. Realistyczny nakład pracy własnej to 1–3 godziny tygodniowo, rosnący wraz z deklarowanym poziomem oceny.

Student, który dany temat zna albo szybko opanuje materiał referencyjny, **może za zgodą prowadzącego zamienić etap 3 na etap 4** i pracować na zajęciach nad własnym projektem. Warunkiem jest wykonanie punktów kontrolnych materiału referencyjnego we własnym zakresie. Jest to opcja, a nie domyślny tryb pracy — czas na zajęciach służy przede wszystkim wspólnemu przejściu przez przykład referencyjny i zadawaniu pytań.

### Odstępstwa od schematu

- **Spotkanie 1** ma rozszerzoną część organizacyjną kosztem etapu 3. Ćwiczenie ma charakter wdrożeniowy, a wybór tematu projektu następuje dopiero po zajęciach.
- **Spotkanie 13** jest w całości poświęcone prezentacjom i przeglądowi projektów.
- W spotkaniach 9–12 materiałem referencyjnym nie jest wyłącznie notebook — szczegóły w sekcji 4.

## 2. Efekty uczenia się

Po ukończeniu przedmiotu student:

1. wyjaśnia różnicę między eksperymentem ML a utrzymywanym systemem ML;
2. wersjonuje kod, konfigurację, dane, modele i metadane eksperymentów;
3. buduje powtarzalny potok przygotowania danych, trenowania i ewaluacji;
4. testuje dane, kod ML, model i kontrakt usługi;
5. pakuje model i udostępnia go w trybie wsadowym lub jako usługę;
6. automatyzuje kontrolę jakości oraz budowanie artefaktów w CI;
7. projektuje bezpieczne wdrożenie, monitoring i procedurę wycofania modelu;
8. rozpoznaje dryf, planuje ciągłe trenowanie i analizuje incydenty;
9. dokumentuje ograniczenia, ryzyko, pochodzenie artefaktów i odpowiedzialność za model;
10. dobiera techniki MLOps do skali, ryzyka i kosztu konkretnego rozwiązania.

### Mapowanie efektów na spotkania i sposób weryfikacji

| Efekt | Spotkania | Weryfikacja |
|---:|---|---|
| 1 | 1, 13 | dyskusja, obrona projektu |
| 2 | 2, 3, 5, 7 | manifest danych, historia eksperymentów, rejestr modeli |
| 3 | 2, 4 | uruchomienie potoku jedną komendą po świeżym klonie |
| 4 | 3, 6, 8 | zestaw testów przechodzący w CI |
| 5 | 7, 8, 9 | wersjonowany artefakt modelu i działający sposób predykcji |
| 6 | 6, 9 | udany przebieg CI na czystym runnerze |
| 7 | 10, 11 | manifest wdrożenia, kryteria promocji, procedura rollbacku |
| 8 | 11, 12 | raport dryfu i przebieg ponownego treningu |
| 9 | 3, 7, 10, 12 | karta modelu, rejestr ryzyk, lineage |
| 10 | wszystkie | uzasadnienie decyzji podczas obrony |

## 3. Organizacja pracy bez trwałego stanu komputera

Na żadnych zajęciach nie należy zakładać, że student otrzyma ten sam komputer ani że pliki lokalne przetrwają do kolejnego tygodnia.

### Zalecany model pracy

1. **Repozytorium Git jest źródłem prawdy.** Kod, konfiguracja, małe dane przykładowe, testy i dokumentacja trafiają do repozytorium na GitHubie. Zdalne repozytorium zakładamy już na spotkaniu 2 — to na nim od spotkania 9 zamieszka potok CI.
2. **Środowisko jest odtwarzalne.** Repozytorium zawiera przypięte zależności (`pyproject.toml` i plik blokady albo `requirements.txt`) oraz pojedynczą komendę przygotowującą projekt.
3. **Dane są odtwarzalne.** Większe zbiory są pobierane skryptem z niezmiennego adresu, weryfikowane sumą kontrolną lub pobierane z magazynu DVC.
4. **Wyniki nie zależą od lokalnego katalogu.** Metryki i małe raporty trafiają do repozytorium, a modele do rejestru, magazynu artefaktów albo artefaktów CI.
5. **Obliczenia są krótkie i tanie.** Ćwiczenia używają małych danych oraz modeli działających na CPU w kilka minut.
6. **CI pełni rolę czystej maszyny referencyjnej.** Student sprawdza, czy projekt działa od zera poza jego bieżącym komputerem.
7. **Sekrety nie trafiają do repozytorium.** Tokeny przekazuje się jako zmienne środowiskowe lub sekrety CI. Po zajęciach student wylogowuje się z usług.

Preferowane jest przeglądarkowe środowisko programistyczne powiązane z repozytorium. Najprostszą realizacją tego wymagania jest **kontener deweloperski** (`.devcontainer/`) uruchamiany w przeglądarce lub lokalnie — opis środowiska jest wtedy częścią repozytorium i nie zależy od stanu komputera w sali. W wariancie lokalnym każde zajęcia rozpoczynają się od sklonowania repozytorium i odtworzenia środowiska, a kończą zatwierdzeniem oraz wysłaniem zmian.

**Docker jest wymagany od spotkania 9** — na spotkaniach 9–11 budujemy obraz, uruchamiamy kontener i stawiamy stos monitorujący. Jeżeli maszyny w sali nie mają działającego demona, część kontenerowa odbywa się na maszynie demonstracyjnej prowadzącego; materiały wykrywają brak Dockera i wypisują komendy zamiast zgłaszać błąd. **Kubernetes i GPU nie są wymagane w żadnym momencie.**

## 4. Materiały dydaktyczne i ich forma

### Skład materiału na jedno spotkanie

Każde spotkanie ma stały komplet materiałów:

1. **Dokument spotkania** `zajecia_NN_temat.md` — podzielony na część dla studentów (teoria i instrukcja) oraz część dla prowadzącego (harmonogram, demonstracja, typowe problemy).
2. **Materiał referencyjny** z kompletnym rozwiązaniem — wykorzystywany zarówno w etapie 2 (demonstracja), jak i w etapie 3 (ćwiczenie prowadzone).
3. **Punkty kontrolne** — 2–4 oznaczone miejsca, w których student ma celowo wprowadzić błąd i opisać, co się stało.
4. **Zadanie projektowe** — lista kontrolna przeniesienia techniki na własny zbiór danych, z jednoznacznym kryterium ukończenia.

### Forma materiału referencyjnego

Notebook jest dobrym nośnikiem tylko dla części tematu. Konteneryzacji, ciagłej integracji ani wdrożenia nie da się w całości pokazać w notebooku, dlatego od spotkania 9 notebook **przygotowuje projekt i pliki konfiguracyjne**, a część wykonawcza dzieje się poza nim: w Dockerze i na GitHubie. Komórki wymagające Dockera są oznaczone i degradują się łagodnie przy jego braku, a kroki wykonywane na GitHubie opisane są jako osobna sekcja „poza notebookiem".

| Spotkania | Forma materiału referencyjnego |
|---|---|
| 1–7 | Notebook z rozwiązaniem (`gotowe_notebooki/zajecia_NN.ipynb`) |
| 8 | Notebook uruchamiający usługę w tle plus katalog `src/` z kodem serwera |
| 9–10 | Notebook generujący projekt, `Dockerfile`, `compose.yaml` i workflow; część wykonawcza w Dockerze i na GitHubie |
| 11–12 | Notebook z usługą eksportującą metryki, stosem monitorującym w `docker compose` i danymi z zasymulowanym dryfem |
| 13 | Automatyczna lista kontrolna, lista dowodów do sprawdzenia na GitHubie, scenariusze awarii i protokół demonstracji |

W spotkaniach 9–12 etap 3 polega na uruchomieniu gotowego przebiegu we własnym forku i doprowadzeniu go do zielonego stanu, a nie na pisaniu konfiguracji od zera.

### Zasada „działa po świeżym klonie”

Każdy materiał referencyjny musi przechodzić automatyczną weryfikację przed zajęciami: świeży klon, odtworzenie środowiska jedną komendą, wykonanie całości bez interakcji, na CPU, w czasie liczonym w minutach. Notebooki należy uruchamiać nieinteraktywnie w CI, aby wykryć rozjazd wersji bibliotek przed spotkaniem, a nie w jego trakcie.

## 5. Referencyjny zestaw narzędzi

Przedmiot ocenia praktykę, nie znajomość składni konkretnej platformy. Aby jednak zajęcia nie zamieniły się w przegląd narzędzi, obowiązuje **jedna ścieżka referencyjna**. Student może użyć zamiennika, jeśli uzasadni wybór i osiągnie ten sam efekt.

| Obszar | Ścieżka referencyjna | Dopuszczalne zamienniki |
|---|---|---|
| Środowisko i zależności | `uv` + `pyproject.toml` + `uv.lock` + `.python-version` | Poetry, pip-tools, conda |
| Jakość kodu | `ruff` + `pre-commit` | black + flake8 + isort |
| Zadania projektowe | `Makefile` lub `uv run` | `just`, `task`, `nox` |
| Repozytorium zdalne | GitHub | GitLab |
| Wersjonowanie danych | DVC z magazynem zdalnym + manifest z sumą kontrolną | Git LFS, sam manifest |
| Walidacja danych | `pandera` | Great Expectations, Soda, własne asercje |
| Śledzenie eksperymentów | MLflow 3 (Tracking + Model Registry) | Weights & Biases, Neptune, DVCLive |
| Potok | `dvc.yaml` + `dvc repro` | Prefect, Dagster, Airflow 3 |
| Testy | `pytest` + `hypothesis` (testy własności) | — |
| Kontrakt i API | FastAPI + Pydantic v2 | Litestar, Flask + Pydantic |
| Kontener | Docker, budowanie wieloetapowe, użytkownik bez uprawnień administratora | Podman, Buildah |
| Rejestr obrazów | `ghcr.io` (GitHub Container Registry) | Docker Hub, rejestr uczelniany |
| CI | GitHub Actions | GitLab CI |
| Dostarczanie | GitHub Environments + self-hosted runner + `docker compose` | GitLab Environments, Argo CD (przy klastrze) |
| Metryki i ślady | `prometheus-client`, Prometheus, Grafana, OpenTelemetry, Jaeger | własny raport, Grafana Cloud |
| Dryf i jakość bez etykiet | Evidently + NannyML (CBPE) | własne wskaźniki PSI/KS |
| Bezpieczeństwo | `pip-audit`, `gitleaks`, `trivy`, SBOM z `docker buildx` | `grype`, `syft`, `cosign` |

Platformę CI wybiera prowadzący przed rozpoczęciem semestru. Utrzymywanie dwóch wariantów podwaja pracę przy materiałach i jest najczęstszą przyczyną problemów na spotkaniach 9–10. Materiały referencyjne przygotowano dla **GitHub Actions**.

### Czego świadomie nie ma w zestawie

- **Kubernetes.** Klaster wprowadza własną, obszerną warstwę pojęciową, która przesłania temat przedmiotu. Wszystkie mechanizmy dostarczania — promocja artefaktu po digeście, wdrożenie etapowe, wycofanie, bramka zatwierdzenia — pokażemy na `docker compose`. Kubernetes, KServe i Argo pojawiają się jako **odniesienie do skali**, bez wymagania klastra.
- **Chmura publiczna.** Konta, limity i koszty są barierą organizacyjną, a nie dydaktyczną. Magazyn DVC i rejestr obrazów działają lokalnie albo na GitHubie.
- **Model językowy od dostawcy.** Blok LLMOps używa deterministycznej atrapy ukrytej za jedną funkcją `call_llm`. Uczymy mechaniki procesu — wersjonowania promptu, zbioru ewaluacyjnego, kosztu i obrony przed wstrzyknięciem polecenia — a nie API konkretnego dostawcy. Podmiana atrapy na prawdziwego dostawcę jest zmianą w jednym miejscu.

## 6. Program 13 spotkań

### Spotkanie 1. Od modelu w notebooku do systemu ML

> Spotkanie organizacyjno-wprowadzające. Odstępuje od standardowego schematu: znaczącą część czasu zajmują sprawy organizacyjne, dostępy i przygotowanie środowiska, a etapu 4 jeszcze nie ma — temat projektu student wybiera dopiero po zajęciach.

**Zagadnienia**

- cele MLOps i problemy występujące po zakończeniu eksperymentu;
- cykl życia systemu ML: dane, trening, walidacja, rejestr, wdrożenie, obserwacja i ponowne trenowanie;
- role zaangażowane w utrzymanie systemu ML oraz ich odpowiedzialność;
- poziomy dojrzałości MLOps;
- przykład długu technicznego i sprzężeń zwrotnych w systemie ML;
- krótka informacja o ramach zewnętrznych, które narzucają część wymagań na systemy ML.

**Zadanie**

Po części organizacyjnej studenci tworzą własny notebook według mikroinstrukcji: wczytują mały zbiór danych, wykonują podstawową kontrolę jakości, trenują model bazowy i model referencyjny, obliczają metryki oraz zapisują model, metryki i wykres macierzy pomyłek jako osobne artefakty.

Jest to jedyne spotkanie, na którym student pisze kod od zera, a nie przechodzi przez gotowe rozwiązanie. Notebook referencyjny prowadzący udostępnia po zajęciach.

**Praca własna po zajęciach:** wybór publicznego zbioru danych i sformułowanie problemu ML. Propozycja tematu podlega akceptacji przed spotkaniem 2.

**Rezultat w repozytorium:** indywidualny notebook z uruchomionymi komórkami, zapisanymi artefaktami i krótkim podsumowaniem wyniku.

### Spotkanie 2. Powtarzalne środowisko i szkielet projektu

**Zagadnienia**

- struktura repozytorium ML i oddzielenie kodu od danych oraz artefaktów;
- deklarowanie i przypinanie zależności: `pyproject.toml`, plik blokady i przypięcie wersji Pythona;
- środowisko jako element repozytorium: kontener deweloperski i instalacja jedną komendą;
- konfiguracja przez pliki i zmienne środowiskowe, oddzielenie sekretów od konfiguracji;
- automatyczna kontrola stylu i podstawowych błędów przed commitem (`ruff`, `pre-commit`);
- determinizm, ziarna losowości i granice reprodukowalności;
- skrypt uruchomieniowy, `Makefile` lub równoważne zadania projektowe;
- założenie zdalnego repozytorium i pierwszy `push`; co **nie może** trafić do historii.

**Materiał referencyjny**

Notebook pokazuje ten sam eksperyment co na spotkaniu 1, ale w formie wywołań kodu z katalogu `src/`. Prowadzący demonstruje przekształcenie notebooka w pakiet z komendami `prepare`, `train` i `evaluate`, wygenerowanie blokady zależności przez `uv lock` oraz uruchomienie całości jedną komendą w świeżym środowisku.

Część wykonywana **poza notebookiem**: `git init`, kontrola `git status` przed pierwszym commitem, założenie repozytorium na GitHubie, `push`, instalacja haka `pre-commit` i sprawdzenie przez sklonowanie do innego katalogu.

**Punkty kontrolne:** zmień ziarno losowości i porównaj metryki; porównaj liczbę bibliotek w deklaracji z liczbą pakietów w blokadzie i wyjaśnij różnicę; usuń przypięcie wersji i pokaż skutek; usuń dane oraz artefakty i sprawdź, czy projekt odbuduje się jedną komendą.

**Zadanie projektowe (po zajęciach)**

Założenie własnego repozytorium projektu z opisanym problemem, przypiętymi zależnościami, konfiguracją poza kodem, kontrolą stylu i instrukcją uruchomienia działającą po świeżym klonie — **wysłanego na GitHub**.

**Rezultat w repozytorium:** odtwarzalny szkielet projektu, `pyproject.toml`, `uv.lock`, `.python-version`, `ruff.toml`, `.pre-commit-config.yaml`, `.gitignore` i README pozwalające odtworzyć wynik.

### Spotkanie 3. Dane: wersjonowanie, kontrakt i governance

**Zagadnienia**

- wersjonowanie kodu, danych i metadanych — dlaczego są to trzy różne problemy;
- manifest zbioru z adresem, wersją, rozmiarem i sumą kontrolną albo DVC z magazynem zdalnym;
- kontrakt danych: schemat, typy, zakresy, dopuszczalne braki i kategorie;
- automatyczna walidacja schematu oraz test wykrywający zmianę kontraktu;
- wyciek danych: wyciek etykiety, wyciek przez czas i wyciek przez preprocessing;
- jakość etykiet i błąd anotacji jako górna granica jakości modelu;
- pochodzenie danych, licencja, dane osobowe, minimalizacja i retencja;
- kiedy zmiana danych oznacza nową wersję modelu.

**Materiał referencyjny**

Notebook pobiera zbiór **ze zdalnego źródła**, buduje manifest z sumą kontrolną, obejmuje dane kontrolą DVC z magazynem lokalnym, definiuje schemat `pandera` i generuje metryczkę zbioru. Prowadzący pokazuje trzy scenariusze awarii: podmieniony plik danych, skasowany plik odtworzony przez `dvc pull` oraz dostawę łamiącą kontrakt.

**Punkty kontrolne:** zepsuj sumę kontrolną; usuń dane i pamięć podręczną, a następnie odtwórz je z magazynu; dodaj wartość spoza dozwolonego zbioru kategorii; wprowadź cechę powstałą po zdarzeniu przewidywanym przez model i pokaż, jak nierealistycznie rosną metryki.

**Zadanie projektowe (po zajęciach)**

Skrypt pobierający dane, manifest własnego zbioru, objęcie danych kontrolą DVC z magazynem zdalnym, schemat, raport walidacji oraz metryczka ze źródłem, licencją i ograniczeniami.

**Rezultat w repozytorium:** skrypt pobierania, manifest danych, wskaźnik `.dvc`, definicja schematu, raport walidacji, test kontraktu i metryczka zbioru.

### Spotkanie 4. Cechy i potok przetwarzania

**Zagadnienia**

- jedna transformacja cech używana w treningu i w predykcji;
- training-serving skew: skąd się bierze i jak go wykryć testem;
- poprawność czasowa cech i podział danych w zadaniach z czasem;
- kroki potoku, graf zależności, idempotencja, pamięć podręczna i przetwarzanie przyrostowe;
- lineage: powiązanie artefaktu wyjściowego z danymi wejściowymi i kodem;
- retry, timeout, backfill i obsługa częściowej awarii;
- cechy wsadowe i online — kiedy feature store jest potrzebny, a kiedy jest zbędną komplikacją;
- kiedy lokalny graf zadań wystarcza, a kiedy potrzebny jest orkiestrator.

**Materiał referencyjny**

Notebook buduje potok dwa razy: najpierw jako własną pamięć podręczną opartą na sumach kontrolnych, potem jako prawdziwy projekt `dvc.yaml` uruchamiany przez `dvc repro`. Etapy: `prepare → validate → split → train → evaluate`, przy czym podział zależy od **raportu walidacji**, więc kontrakt danych staje się bramką potoku.

**Punkty kontrolne:** zastosuj inną kolejność kolumn w predykcji i sprawdź, który test to wykrył; wywołaj awarię etapu treningu i ustal, co trzeba powtórzyć; uruchom `dvc repro` dwa razy bez zmian; zmień jeden parametr i porównaj zasięg unieważnienia dla parametru modelu i parametru podziału.

**Zadanie projektowe (po zajęciach)**

Rozbicie własnego projektu na jawne etapy `dvc.yaml` i wydzielenie wspólnej transformacji cech wraz z testem zgodności obu ścieżek.

**Rezultat w repozytorium:** `dvc.yaml`, `dvc.lock`, `params.yaml`, wspólny etap cech, test zgodności oraz zapis udanego i nieudanego przebiegu.

### Spotkanie 5. Śledzenie eksperymentów i wybór modelu

**Zagadnienia**

- parametry, metryki, tagi, artefakty i kontekst uruchomienia;
- serwer śledzenia eksperymentów, automatyczne logowanie i powiązanie przebiegu z wersją kodu oraz danych;
- model bazowy, poprawny podział danych i unikanie wybierania modelu na zbiorze testowym;
- walidacja krzyżowa, przedziały niepewności i istotność różnic między modelami;
- metryki techniczne, metryki biznesowe i koszt błędu;
- porównywalność eksperymentów oraz ręczne notowanie wyników jako antywzorzec;
- kryterium wyboru modelu zdefiniowane **przed** eksperymentami.

**Materiał referencyjny**

Notebook uruchamiający lokalny serwer śledzenia i wykonujący serię kontrolowanych eksperymentów z tego samego kodu. Prowadzący pokazuje porównanie przebiegów, artefakty przypisane do przebiegu oraz powiązanie modelu z kodem i danymi, na których powstał.

**Punkty kontrolne:** uruchom ten sam eksperyment dwa razy i wyjaśnij różnicę w metrykach; wybierz model na zbiorze testowym i pokaż, dlaczego wynik jest zawyżony; dodaj tag pozwalający odróżnić serię eksperymentów.

**Zadanie projektowe (po zajęciach)**

Co najmniej trzy kontrolowane eksperymenty we własnym projekcie, zapisane parametry, metryki i artefakty oraz uzasadniony wybór modelu według wcześniej zdefiniowanego kryterium.

**Rezultat w repozytorium:** kod eksperymentu, tabela porównawcza i udokumentowany wybór modelu.

### Spotkanie 6. Testowanie systemów ML

**Zagadnienia**

- piramida testów w projekcie ML: kod, dane, model, kontrakt;
- testy jednostkowe transformacji i testy integracyjne potoku;
- testy danych, niezmienników oraz oczekiwań statystycznych;
- testy zachowania modelu: niezmienniczość, kierunkowość i przypadki brzegowe;
- próg jakości, stabilność wyniku i wydajność predykcji;
- testy kontraktu wejścia i wyjścia;
- testy własności: opis dopuszczalnych danych zamiast listy przypadków, generowanie kontrprzykładów i ich upraszczanie;
- testy odporne na losowość, tolerancje numeryczne i typowe przykłady testów kruchych;
- czas wykonania zestawu testów jako wymaganie projektowe.

**Materiał referencyjny**

Notebook oraz katalog `tests/` dla celowo wadliwego potoku. Materiał zawiera cztery ukryte defekty: wyciek etykiety, błędny typ kolumny, spadek jakości poniżej progu i zmianę kontraktu predykcji. Prowadzący pokazuje, który rodzaj testu wykrywa który defekt, a następnie wprowadza defekt na granicy kontraktu, którego żaden test na prawdziwych danych nie wykrywa — i który `hypothesis` znajduje natychmiast.

**Punkty kontrolne:** napraw jeden defekt i sprawdź, które testy zmieniły stan; napisz test kruchy i pokaż, dlaczego jest bezużyteczny; obniż próg jakości i uzasadnij, czy to jest dopuszczalna reakcja; wprowadź filtr odrzucający rekordy przy granicy kontraktu i porównaj reakcję testów przykładowych i testów własności.

**Zadanie projektowe (po zajęciach)**

Zestaw testów dla własnego projektu obejmujący transformację cech, walidację danych, próg jakości modelu, kontrakt odpowiedzi i co najmniej dwa testy własności, uruchamiany jedną komendą.

**Rezultat w repozytorium:** zestaw testów uruchamiany jedną komendą wraz z opisem, co każdy z nich chroni.

### Spotkanie 7. Pakowanie modelu, rejestr i karta modelu

**Zagadnienia**

- model jako artefakt: wagi, kod, zależności i sygnatura wejścia oraz wyjścia;
- egzekwowanie sygnatury i przykład wejścia jako część artefaktu;
- formaty serializacji i ryzyko uruchamiania niezaufanych artefaktów; bezpieczniejsze alternatywy dla surowego `pickle`;
- rejestr modeli: wersje, **aliasy i tagi** zamiast wycofanych etapów cyklu życia;
- bramki jakości i promocja `candidate → challenger → champion` realizowana aliasami;
- karta modelu: przeznaczenie, dane, wyniki, ograniczenia i sytuacje niezalecanego użycia;
- identyfikowalność: przejście od wersji modelu do kodu, konfiguracji, danych i eksperymentu;
- decyzja o zatwierdzeniu i kto ją podejmuje.

**Materiał referencyjny**

Notebook pakujący model razem z sygnaturą, przykładem wejścia i metrykami, rejestrujący wersję, nadający alias oraz generujący kartę modelu z metadanych przebiegu. Prowadzący pokazuje również ładowanie modelu wyłącznie po aliasie, bez odwołania do numeru wersji.

**Punkty kontrolne:** podaj do modelu dane o złym typie i pokaż, jak reaguje sygnatura; zarejestruj model poniżej progu jakości i sprawdź, czy bramka blokuje promocję; przenieś alias na inną wersję i prześledź skutek po stronie klienta.

**Zadanie projektowe (po zajęciach)**

Wersjonowany artefakt własnego modelu z sygnaturą, wpis w rejestrze z aliasem, reguła promocji oraz karta modelu.

**Rezultat w repozytorium:** wersjonowany model, karta modelu, reguła promocji i opis powiązania wersji z eksperymentem.

### Spotkanie 8. Udostępnianie modelu: predykcja wsadowa i usługa

**Zagadnienia**

- wybór między predykcją wsadową, request-response i strumieniową — kryteria decyzji;
- API predykcyjne, walidacja żądania i jawny, wersjonowany kontrakt;
- zgodność wsteczna kontraktu i koszt jej złamania;
- opóźnienie w percentylach, przepustowość, dostępność i koszt jednostkowy predykcji;
- obsługa błędów, limity, health check i readiness;
- bezpieczne logowanie, identyfikator żądania i brak danych osobowych w logach;
- niezawodne zadanie wsadowe: idempotencja, ponowne uruchomienie i raport wykonania.

**Materiał referencyjny**

Notebook uruchamiający w tle usługę predykcyjną opartą o model z rejestru oraz katalog `src/` z kodem serwera. Materiał zawiera klienta, test kontraktu, pomiar opóźnienia i wariant wsadowy tej samej logiki.

**Punkty kontrolne:** wyślij żądanie niezgodne z kontraktem i sprawdź odpowiedź; usuń pole z odpowiedzi i pokaż, który test to wykryje; porównaj opóźnienie dla pojedynczego żądania i dla żądania zbiorczego.

**Zadanie projektowe (po zajęciach)**

Udostępnienie własnego modelu jako usługi HTTP albo niezawodnego zadania wsadowego, wraz z jawnym kontraktem i jego testem.

**Rezultat w repozytorium:** kod predykcji, definicja kontraktu, test kontraktu i pomiar opóźnienia.

### Spotkanie 9. Kontenery, ciągła integracja i łańcuch dostaw

**Zagadnienia**

- obraz kontenera, warstwy, niezmienność i minimalizacja obrazu;
- budowanie wieloetapowe, uruchamianie bez uprawnień administratora, obraz bez zbędnych narzędzi;
- CI dla kodu ML: kontrola stylu, testy, walidacja danych, trening próbny i budowa obrazu;
- cache, artefakty CI, budżet czasu i kosztu przebiegu;
- zagrożenia łańcucha dostaw: zależności, obrazy bazowe, dane i modele z zewnątrz;
- SBOM oraz jego rozszerzenie o modele i zbiory danych;
- skanowanie zależności i obrazu, wykrywanie sekretów w historii repozytorium;
- atestacja pochodzenia artefaktu i podpisywanie — poziom rozszerzenia.

**Materiał referencyjny**

Projekt z `Dockerfile`, workflow GitHub Actions i pełnym łańcuchem kontroli. Prowadzący buduje obraz z atestacjami, uruchamia test dymny kontenera, pokazuje przebieg zielony i czerwony, wygenerowany SBOM oraz wynik `pip-audit` z realną podatnością.

Część wykonywana **poza notebookiem**: wysłanie repozytorium na GitHub, obserwacja przebiegu w zakładce Actions, publikacja obrazu do `ghcr.io` oraz włączenie ochrony gałęzi `main` z wymaganym przebiegiem `quality`.

**Punkty kontrolne:** dodaj zależność z podatnością i pokaż reakcję skanera; wprowadź sekret do repozytorium i sprawdź, czy zostanie wykryty; zepsuj test i prześledź, który krok zatrzymał przebieg oraz dlaczego obraz w ogóle nie powstał.

**Zadanie projektowe (po zajęciach)**

Własny kontener i potok CI uruchamiający testy oraz trening na próbce danych przy każdej zmianie. Budowa obrazu wykonywana wyłącznie na runnerze CI, publikacja do `ghcr.io`, ochrona gałęzi `main` wymagająca zielonego przebiegu.

**Rezultat w repozytorium:** `Dockerfile`, `.dockerignore`, workflow, `.pre-commit-config.yaml`, SBOM, wynik skanu oraz odnośnik do udanego przebiegu wraz z digestem obrazu.

### Spotkanie 10. Dostarczanie i strategie wdrożeń

**Zagadnienia**

- różnica między CI, CD i CT;
- środowiska dev, staging i production; promocja tego samego artefaktu zamiast ponownej budowy;
- wdrożenie **po digeście**, nie po znaczniku — i dlaczego to jest różnica jakościowa;
- deklaratywny opis stanu docelowego i proces uzgadniający;
- dwa środowiska w `docker compose` z routerem rozdzielającym ruch według wag;
- bramka zatwierdzenia: GitHub Environments z regułą *required reviewers*;
- self-hosted runner — dlaczego to maszyna docelowa łączy się z CI, a nie odwrotnie;
- wdrożenia rolling, blue-green, canary, shadow i A/B; przełączniki funkcji;
- automatyczna analiza metryk i wstrzymanie wdrożenia; minimalna liczba obserwacji;
- zgodność wsteczna, migracja cech, rollback modelu a rollback kodu;
- infrastruktura jako kod — przegląd;
- model zagrożeń dla wdrożonej usługi: nadużycie endpointu, kradzież modelu, dane trujące;
- Kubernetes, KServe i Argo jako odniesienie do skali, bez wymagania klastra.

**Materiał referencyjny**

Projekt z rejestrem artefaktów, uzgadnianiem odmawiającym działania przy niezgodnej sumie kontrolnej, dwoma środowiskami w `docker compose` oraz warstwą decyzyjną z automatyczną analizą canary. Prowadzący kieruje część ruchu do nowej wersji, pokazuje automatyczną decyzję o promocji, a następnie wymusza wycofanie i mierzy jego czas.

Część wykonywana **poza notebookiem**: utworzenie środowisk `staging` i `production` w ustawieniach repozytorium, włączenie reguły zatwierdzania, rejestracja self-hosted runnera i przejście pełnej ścieżki od scalenia do wdrożenia.

**Punkty kontrolne:** wprowadź gorszy model jako kandydata i sprawdź, po ilu żądaniach kryterium go zatrzyma; złam zgodność wsteczną kontraktu i opisz, dlaczego przełączenie wersji nie wystarcza; wykonaj wycofanie i **zmierz** czas powrotu do stanu poprawnego.

**Zadanie projektowe (po zajęciach)**

Automatyczne dostarczenie własnego projektu na staging i wdrożenie produkcyjne za bramką zatwierdzenia, kryteria promocji oraz przetestowana procedura wycofania.

**Rezultat w repozytorium:** deklaratywny opis wdrożenia, workflow dostarczania, kryteria promocji, procedura wycofania, zmierzony czas jej wykonania i model zagrożeń.

### Spotkanie 11. Obserwowalność i monitoring modeli

**Zagadnienia**

- logi, metryki i ślady jako trzy uzupełniające się sygnały; wspólny standard instrumentacji;
- identyfikator żądania i korelacja zdarzeń między usługami;
- model *pull*: usługa wystawia `/metrics`, a system monitorujący sam po nie przychodzi;
- typy metryk — licznik, histogram, miernik — i liczenie percentyli po stronie systemu monitorującego;
- cztery warstwy monitoringu: system, dane wejściowe, predykcje oraz jakość i wartość biznesowa;
- opóźnione etykiety i monitoring w okresie ich braku;
- SLI, SLO i budżet błędu dla usługi albo zadania wsadowego;
- progi alertów, zmęczenie alertami i ograniczanie fałszywych alarmów;
- prywatność, próbkowanie danych wejściowych i retencja logów;
- dashboard a cykliczny raport — co wystarcza przy jakiej skali.

**Materiał referencyjny**

Strumień logów działającego modelu wraz z instrumentacją usługi ze spotkania 8 oraz usługa wystawiająca `/metrics` przez `prometheus-client`. Do tego stos w `docker compose`: Prometheus, Grafana i Jaeger. Prowadzący pokazuje ślad pojedynczego żądania, odczyt spod `/metrics`, definicje wskaźników i wygenerowany raport.

**Punkty kontrolne:** zwiększ udział błędów w strumieniu i sprawdź, który alert zadziałał; ustaw próg zbyt czuły i policz fałszywe alarmy; znajdź w logach pola, których nie powinno tam być; wskaż, która z czterech warstw jest najtrudniejsza do zmierzenia i dlaczego.

**Zadanie projektowe (po zajęciach)**

Monitoring własnego projektu obejmujący endpoint `/metrics` z metrykami czterech warstw, Prometheusa zbierającego te metryki oraz reguły alertów i raport.

**Rezultat w repozytorium:** instrumentacja usługi, konfiguracja stosu monitorującego, definicje metryk, SLI/SLO, reguły alertów i raport.

### Spotkanie 12. Dryf, ciągłe trenowanie, incydent i wprowadzenie do LLMOps

**Zagadnienia**

- data drift, concept drift, quality drift i training-serving skew;
- detekcja zmian rozkładu: wskaźniki odległości rozkładów i testy statystyczne oraz ich ograniczenia przy dużych próbkach;
- dobór okna referencyjnego i bieżącego;
- estymacja jakości modelu bez etykiet metodą CBPE, jej założenia i granice stosowalności;
- wyzwalacze ponownego treningu: czas (`schedule` w CI), dane, wynik monitoringu i decyzja człowieka;
- walidacja challengera względem championa oraz automatyczne bramki jakości;
- runbook, analiza przyczyn źródłowych i przegląd incydentu bez wskazywania winnych;
- fairness i jakość w podgrupach jako osobny wymiar monitoringu;
- **blok LLMOps:** wersjonowanie promptów jako artefaktów, stały zestaw ewaluacyjny, ocena modelem sędziowskim i jej ograniczenia, tracing oraz koszt w przeliczeniu na token, wstrzykiwanie poleceń i pozostałe typowe zagrożenia aplikacji LLM;
- co pozostaje wspólne dla klasycznego MLOps i systemów generatywnych.

**Materiał referencyjny**

Dane z zasymulowanym dryfem w trzech scenariuszach, raport Evidently, estymacja jakości bez etykiet przez NannyML, automatyczne porównanie championa z challengerem oraz zestaw ewaluacyjny dla dwóch wersji promptu. Blok LLMOps używa deterministycznej atrapy ukrytej za funkcją `call_llm` — podmiana na prawdziwego dostawcę jest zmianą w jednym miejscu.

**Punkty kontrolne:** zmień rozmiar okna i pokaż, jak zmienia się wykryty dryf; porównaj szacunek CBPE z rzeczywistą jakością i wskaż scenariusz, w którym estymator myli się o pół punktu; wywołaj dryf, który nie pogarsza jakości, i uzasadnij reakcję; zmień prompt i sprawdź, które przypadki testowe przestały przechodzić.

**Zadanie projektowe (po zajęciach)**

Detekcja dryfu we własnym projekcie, raport, przebieg ponownego treningu z automatyczną decyzją o promocji lub odrzuceniu oraz rejestr ryzyk i krótki runbook.

**Rezultat w repozytorium:** kod detekcji dryfu, raport, przebieg ponownego treningu, wynik porównania modeli oraz rejestr ryzyk.

### Spotkanie 13. Prezentacje projektów i przegląd produkcyjny

**Zagadnienia**

- demonstracja projektu od świeżego klonu lub przez przebieg CI;
- obrona decyzji architektonicznych;
- „game day”: indywidualna reakcja autora projektu na wylosowaną awarię;
- wzajemny przegląd projektów i retrospektywa.

**Zadanie**

Każdy student ma 6–8 minut na prezentację, demonstrację powtarzalności i reakcję na scenariusz awarii. Prowadzący zadaje pytanie dotyczące działania całego systemu.

Prowadzący przygotowuje wcześniej listę 8–10 scenariuszy awarii, aby losowanie było powtarzalne i porównywalne między studentami. Przykłady: podmieniony plik danych, zmieniony typ kolumny w źródle, model poniżej progu jakości promowany przez pomyłkę, niedostępny rejestr modeli, przeterminowany sekret, nagły wzrost opóźnienia, dryf rozkładu wejścia bez spadku metryki, brak etykiet przez dwa okresy raportowe.

**Rezultat:** wersja projektu oznaczona tagiem, krótka prezentacja i protokół demonstracji.

### Governance rozproszone w programie

Wymagania dotyczące bezpieczeństwa, zgodności i odpowiedzialności nie tworzą osobnego spotkania. Są wprowadzane tam, gdzie realnie występują w cyklu życia systemu:

| Zagadnienie | Spotkanie |
|---|---|
| Sekrety, konfiguracja, brak danych wrażliwych w repozytorium | 2, 9 |
| Licencje, dane osobowe, minimalizacja i retencja | 3 |
| Karta modelu, identyfikowalność, decyzja o zatwierdzeniu | 7 |
| Bezpieczne logowanie i ochrona endpointu | 8, 11 |
| Łańcuch dostaw, SBOM, skanowanie, atestacje | 9 |
| Model zagrożeń dla wdrożenia | 10 |
| Rejestr ryzyk, fairness, nadzór człowieka, bezpieczeństwo aplikacji LLM | 12 |

Zewnętrzne ramy (zarządzanie ryzykiem AI, wymagania regulacyjne dla systemów wysokiego ryzyka, systemy zarządzania AI) omawiane są skrótowo na spotkaniu 1 jako uzasadnienie tych praktyk i wracają na spotkaniu 12 przy rejestrze ryzyk. Celem nie jest wykład z prawa, lecz pokazanie, że karta modelu, audytowalność i nadzór człowieka mają umocowanie poza projektem.

## 7. Projekt zaliczeniowy

### Cel

Każdy student samodzielnie buduje mały, lecz kompletny i możliwy do odtworzenia system ML. Projekt, repozytorium, implementacja, dokumentacja i obrona mają charakter indywidualny. Ocenie podlega przede wszystkim jakość procesu, automatyzacja, niezawodność i uzasadnienie decyzji, a nie maksymalna wartość metryki modelu.

Studenci samodzielnie wybierają zbiór danych, na przykład z platformy Kaggle, repozytorium UCI Machine Learning Repository lub innego publicznego źródła, a następnie przygotowują adekwatny do problemu model. Dokumentacja projektu musi zawierać:

- krótką charakterystykę zbioru danych, w tym jego źródło, licencję, rozmiar, strukturę, zmienną objaśnianą oraz najważniejsze ograniczenia jakościowe;
- opis problemu ML i sposobu przygotowania danych;
- opis wybranego modelu oraz uzasadnienie, dlaczego jest odpowiedni dla danych i celu projektu;
- porównanie modelu z prostym rozwiązaniem bazowym;
- wskazanie ograniczeń modelu i sytuacji, w których jego predykcje mogą być niewiarygodne.

Projekt rozwijany jest przyrostowo. Każdy kamień milowy jest sumą zadań projektowych z poprzedzających go spotkań:

1. **po spotkaniu 2:** repozytorium, opisany problem, przypięte zależności i instrukcja uruchomienia;
2. **po spotkaniu 5:** manifest i walidacja danych, potok, model bazowy oraz zapisane eksperymenty;
3. **po spotkaniu 8:** testy, wersjonowany model z kartą modelu, sposób predykcji i kontrakt;
4. **po spotkaniu 10:** CI, kontener, sposób dostarczania i procedura wycofania;
5. **po spotkaniu 12:** monitoring, detekcja dryfu, rejestr ryzyk i kompletna dokumentacja.

### Pomysły na projekty

1. **Predykcja rezygnacji klienta** — model tabelaryczny, predykcja wsadowa, monitorowanie zmiany udziału klas i jakości po otrzymaniu etykiet.
2. **Prognozowanie zapotrzebowania** — szeregi czasowe, harmonogram predykcji, backtesting, opóźnione dane i reguła ponownego treningu.
3. **Klasyfikacja zgłoszeń pomocy technicznej** — tekst, endpoint API, kolejka do ręcznej obsługi przypadków o niskiej pewności i monitoring nowych kategorii.
4. **Wykrywanie anomalii w telemetrii** — przetwarzanie wsadowe lub strumieniowe, alerty, kontrola ich częstości i procedura obsługi incydentu.
5. **Ocena ryzyka kredytowego na danych publicznych** — walidacja danych, explainability, analiza jakości w podgrupach i udokumentowane ograniczenia użycia.
6. **Klasyfikacja obrazów na małym zbiorze** — wersjonowanie modelu, test wejścia, pomiar opóźnienia i wykrywanie obrazów spoza oczekiwanej domeny.
7. **System rekomendacji treści** — trening offline, generowanie rekomendacji batch, metryki rankingowe i monitoring popularności oraz pokrycia katalogu.
8. **Mały system RAG** — wersjonowanie dokumentów i promptów, zestaw ewaluacyjny, pomiar jakości odpowiedzi, kosztu i opóźnienia oraz tracing zapytań.

Student samodzielnie wybiera publiczny albo syntetyczny zbiór danych. Zbiór udostępniony przez prowadzącego może zostać wykorzystany wyłącznie po wcześniejszym uzgodnieniu. Projekt nie może wymagać płatnej infrastruktury ani przechowywania danych wyłącznie na komputerze w sali.

## 8. Poziomy projektu odpowiadające ocenom

Poziomy są **kumulatywne**. Aby otrzymać daną ocenę, projekt musi spełnić wymagania tej oceny oraz wszystkich ocen niższych. Samo dodanie narzędzia bez wykazania jego roli nie spełnia wymagania.

### Ocena 3,0 — powtarzalny eksperyment

- jasno opisany problem, użytkownik systemu, dane i metryka sukcesu;
- samodzielnie wybrany publiczny zbiór danych wraz z krótką charakterystyką, źródłem i licencją;
- model adekwatny do problemu wraz z opisem i uzasadnieniem jego wyboru;
- indywidualne repozytorium z historią pracy studenta;
- jedna komenda uruchamia przygotowanie danych, trening i ewaluację;
- przypięte zależności wraz z plikiem blokady, przypięta wersja Pythona, konfiguracja poza kodem i ustalone ziarna losowości;
- wersja danych lub manifest z sumą kontrolną;
- model bazowy oraz poprawny podział danych;
- zapis metryk i modelu jako artefaktów;
- README pozwalające odtworzyć wynik po świeżym klonie.

### Ocena 3,5 — kontrolowany i testowany potok

Wszystko z poziomu 3,0 oraz:

- potok składający się z jawnych, powtarzalnych etapów;
- śledzenie parametrów, metryk i artefaktów eksperymentów;
- automatyczna walidacja schematu i jakości danych;
- testy jednostkowe transformacji oraz test progu jakości modelu;
- wspólna transformacja cech używana w treningu i predykcji wraz z testem zgodności;
- porównanie co najmniej trzech kontrolowanych eksperymentów;
- karta modelu opisująca przeznaczenie, dane, wyniki i ograniczenia.

### Ocena 4,0 — automatyczne budowanie i udostępnianie

Wszystko z poziomu 3,5 oraz:

- CI uruchamiające testy, walidację i krótki trening kontrolny na czystym runnerze;
- model udostępniony jako usługa API albo niezawodne zadanie wsadowe;
- jawny, wersjonowany kontrakt wejścia i wyjścia oraz jego test;
- kontener lub równoważny przenośny artefakt wykonawczy budowany automatycznie;
- rejestr wersji modeli z metadanymi, aliasem wskazującym wersję używaną oraz regułą promocji;
- skan zależności lub obrazu, wygenerowany SBOM oraz brak sekretów w historii repozytorium.

### Ocena 4,5 — wdrożenie obserwowalne

Wszystko z poziomu 4,0 oraz:

- automatyczne dostarczenie co najmniej do środowiska demonstracyjnego lub staging;
- strategia bezpiecznej zmiany wersji, np. canary, shadow lub blue-green, może być zrealizowana na symulatorze;
- automatyczny rollback albo jednoznaczna, przetestowana procedura wycofania;
- monitoring co najmniej jednej metryki systemowej, jednej metryki danych i jednej metryki modelu;
- sensowne progi alertów oraz dashboard lub cykliczny raport;
- wykrycie zasymulowanego dryfu i udokumentowana reakcja;
- model zagrożeń oraz podstawowy rejestr ryzyk.

### Ocena 5,0 — zarządzany cykl życia

Wszystko z poziomu 4,5 oraz:

- wiarygodny mechanizm wyboru championa i challengera;
- kontrolowane ponowne trenowanie wyzwalane harmonogramem, nowymi danymi lub sygnałem z monitoringu;
- automatyczne bramki jakości blokujące promocję gorszego lub niespełniającego zasad modelu;
- lineage pozwalający przejść od wdrożonej wersji do kodu, konfiguracji, danych i eksperymentu;
- SLI/SLO dla usługi lub zadania oraz krótki runbook incydentowy;
- test scenariusza awarii obejmujący wykrycie, diagnozę i odtworzenie działania;
- co najmniej **jedno uzasadnione rozszerzenie**, np.:
  - analiza jakości i fairness w podgrupach;
  - podpisywanie artefaktów, SBOM i weryfikacja pochodzenia;
  - test obciążeniowy i optymalizacja kosztu lub opóźnienia;
  - point-in-time correct feature pipeline;
  - ewaluacja, tracing i zabezpieczenia dla projektu RAG/LLM;
  - infrastruktura jako kod dla środowiska demonstracyjnego.

## 9. Wspólne warunki zaliczenia i sposób oceny

Niezależnie od deklarowanego poziomu:

- projekt musi działać z repozytorium lub przez CI bez dostępu do poprzedniego komputera studenta;
- instrukcja odtworzenia musi zostać sprawdzona przez inną osobę;
- dane i wykorzystane komponenty muszą mieć wskazane źródło oraz licencję;
- sekrety, dane osobowe i duże binarne artefakty nie mogą znaleźć się w historii Git;
- student musi samodzielnie zaprezentować projekt i rozumieć cały przepływ;
- niedziałająca demonstracja może zostać zastąpiona pełnym zapisem udanego przebiegu CI, jeśli awaria nie wynika z projektu;
- poważny błąd metodologiczny, wyciek danych albo brak możliwości odtworzenia wyniku ogranicza ocenę do 3,0 do czasu poprawy.

### Korzystanie z asystentów AI

Korzystanie z asystentów programistycznych jest **dozwolone i traktowane jako normalne narzędzie pracy**. Obowiązują jednak trzy zasady:

1. Student odpowiada za każdą linijkę w repozytorium i musi umieć wyjaśnić jej działanie oraz uzasadnić wybór podczas obrony.
2. Do publicznych usług nie wolno przekazywać sekretów, danych osobowych ani niepublicznych zbiorów danych.
3. Dokumentacja projektu zawiera krótką notę o zakresie użycia asystenta — do czego był wykorzystany i gdzie jego propozycja została odrzucona lub poprawiona.

Niemożność wyjaśnienia własnego kodu podczas obrony jest traktowana jak brak samodzielności, niezależnie od jakości rozwiązania.

### Automatyczna weryfikacja wstępna

Przed obroną projekt przechodzi automatyczną kontrolę na czystym runnerze: świeży klon, odtworzenie środowiska jedną komendą, uruchomienie potoku i testów, sprawdzenie obecności sekretów oraz przypięcia zależności. Kontrola nie ocenia jakości rozwiązań — odsiewa jedynie projekty, których nie da się uruchomić.

Proponowane wagi pomocnicze:

| Obszar | Waga |
|---|---:|
| Powtarzalność, dane i eksperymenty | 20% |
| Potok, testy i jakość kodu | 20% |
| CI, pakowanie i sposób udostępnienia | 20% |
| Monitoring, niezawodność i bezpieczeństwo | 20% |
| Dokumentacja, decyzje architektoniczne i obrona | 20% |

Poziom funkcjonalny określa najwyższą możliwą ocenę, a jakość realizacji obszarów z tabeli pozwala ją potwierdzić lub obniżyć.

## 10. Minimalna infrastruktura dla prowadzącego

- szablon repozytorium z małym przykładowym zbiorem, konfiguracją kontenera deweloperskiego i skryptem bootstrap;
- **jedna** platforma CI z runnerem oraz oszacowany budżet minut na grupę;
- automatyczne uruchamianie wszystkich notebooków referencyjnych przed każdą edycją przedmiotu;
- współdzielony serwer śledzenia eksperymentów i rejestr artefaktów albo wariant lokalny uruchamiany w CI;
- rejestr obrazów kontenerowych (`ghcr.io` wystarcza);
- **maszyna demonstracyjna z działającym Dockerem** oraz zarejestrowanym self-hosted runnerem z etykietą `demo`;
- środowiska `staging` i `production` w ustawieniach repozytorium, z regułą zatwierdzania dla produkcji;
- obrazy `prom/prometheus`, `grafana/grafana`, `jaegertracing/all-in-one` i `nginx` **pobrane przed zajęciami** — pobieranie na miejscu zajmie cały slot;
- przygotowany strumień logów oraz zbiór z zasymulowanym dryfem dla spotkań 11–12;
- wariant zapasowy na wypadek braku Dockera w sali: materiały wykrywają jego brak i wypisują komendy, a część kontenerową wykonuje prowadzący;
- lista 8–10 scenariuszy awarii na spotkanie 13;
- krótkotrwałe dane uwierzytelniające i instrukcja bezpiecznego wylogowania;
- niewielkie, wersjonowane zestawy danych przygotowane przed semestrem.

### Co sprawdzić przed pierwszym uruchomieniem przedmiotu

| Sprawdzenie | Dlaczego |
|---|---|
| `docker info` na maszynie demonstracyjnej | najczęstsza przyczyna zablokowanych zajęć 9–11 |
| przebieg workflow na czystym repozytorium | wersje akcji (`rev`, `@v4`) starzeją się między edycjami |
| `uv lock` i `dvc pull` z sieci uczelnianej | zapory potrafią blokować rejestry pakietów |
| `host.docker.internal` z kontenera | na niektórych konfiguracjach wymaga dodatkowego wpisu |
| aktualność `rev` w `.pre-commit-config.yaml` | nieaktualna wersja zatrzymuje pierwszy commit studenta |

## 11. Rekomendowane źródła i dokumentacja

### Podstawa — do przeczytania w trakcie semestru

- Google Cloud, **MLOps: Continuous delivery and automation pipelines in machine learning**:
  <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning>
- MLflow, **Tracking, Model Registry, Evaluation i Tracing**:
  <https://mlflow.org/docs/latest/>
- DVC, **Data Versioning i Data Pipelines**:
  <https://dvc.org/doc>
- Evidently, **ewaluacja i monitoring systemów ML**:
  <https://docs.evidentlyai.com/>
- C. Huyen, **Designing Machine Learning Systems** — narracja, której dokumentacja narzędzi nie daje.

### Narzędzia ścieżki referencyjnej

- uv, **zarządzanie środowiskiem i zależnościami**: <https://docs.astral.sh/uv/>
- Ruff, **kontrola stylu i błędów**: <https://docs.astral.sh/ruff/>
- Pandera, **walidacja danych**: <https://pandera.readthedocs.io/>
- pytest, **testy**: <https://docs.pytest.org/>
- FastAPI i Pydantic, **kontrakt usługi**: <https://fastapi.tiangolo.com/> oraz <https://docs.pydantic.dev/>
- OpenTelemetry, **standard logów, metryk i śladów**: <https://opentelemetry.io/docs/>
- Development Containers, **środowisko jako część repozytorium**: <https://containers.dev/>

### Uzupełnienie — dla wybranych tematów i rozszerzeń

- OpenLineage, **standard metadanych o pochodzeniu danych i zadań**: <https://openlineage.io/docs/>
- Feast, **feature store**: <https://docs.feast.dev/>
- KServe, **model serving na Kubernetes**: <https://kserve.github.io/website/>
- NannyML, **estymacja jakości modelu bez etykiet**: <https://nannyml.readthedocs.io/>
- Argo Rollouts, **progressive delivery**: <https://argo-rollouts.readthedocs.io/>
- SLSA, **bezpieczeństwo łańcucha dostaw oprogramowania**: <https://slsa.dev/>
- CycloneDX, **SBOM oraz ML-BOM**: <https://cyclonedx.org/>
- Sigstore, **podpisywanie artefaktów**: <https://docs.sigstore.dev/>

### Ryzyko, bezpieczeństwo i governance

- NIST, **AI Risk Management Framework** wraz z profilem dla AI generatywnej:
  <https://www.nist.gov/itl/ai-risk-management-framework>
- ISO/IEC 42001, **system zarządzania sztuczną inteligencją** — poziom świadomości istnienia normy.
- Akt o sztucznej inteligencji (EU AI Act), **klasyfikacja ryzyka i obowiązki dokumentacyjne**:
  <https://artificialintelligenceact.eu/>
- OWASP, **Top 10 dla aplikacji LLM** oraz **Machine Learning Security Top 10**:
  <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- MITRE ATLAS, **taksonomia ataków na systemy ML**: <https://atlas.mitre.org/>

Dokumentację narzędzi i stan regulacji należy weryfikować przed każdą edycją przedmiotu. W ćwiczeniach warto konsekwentnie oceniać praktykę MLOps, a nie znajomość składni konkretnej platformy.
