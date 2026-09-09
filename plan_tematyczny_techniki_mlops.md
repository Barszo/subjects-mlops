# Plan tematyczny przedmiotu „Techniki MLOps”

## 1. Założenia organizacyjne

- **Wymiar zajęć:** 13 spotkań po 90 minut.
- **Forma:** krótkie wprowadzenie, demonstracja prowadzącego i ćwiczenie praktyczne.
- **Proponowany podział spotkania:**
  - 10 minut — przypomnienie, cel zajęć i uruchomienie środowiska;
  - 25 minut — omówienie zagadnień;
  - 15 minut — demonstracja;
  - 35 minut — indywidualne zadanie praktyczne;
  - 5 minut — zapis wyników w repozytorium i podsumowanie.
- **Forma zaliczenia:** indywidualny projekt końcowy z krótką prezentacją i obroną.
- **Założenia wstępne:** podstawowa znajomość Pythona, Git, uczenia maszynowego i pracy w terminalu.
- **Stan aktualności planu:** wrzesień 2026 r. Narzędzia są przykładami realizacji praktyk, a nie celem przedmiotu.

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

## 3. Organizacja pracy bez trwałego stanu komputera

Na żadnych zajęciach nie należy zakładać, że student otrzyma ten sam komputer ani że pliki lokalne przetrwają do kolejnego tygodnia.

### Zalecany model pracy

1. **Repozytorium Git jest źródłem prawdy.** Kod, konfiguracja, małe dane przykładowe, testy i dokumentacja trafiają do uczelnianego GitLaba lub GitHuba.
2. **Środowisko jest odtwarzalne.** Repozytorium zawiera przypięte zależności (`pyproject.toml` i plik blokady albo `requirements.txt`) oraz pojedynczą komendę przygotowującą projekt.
3. **Dane są odtwarzalne.** Większe zbiory są pobierane skryptem z niezmiennego adresu, weryfikowane sumą kontrolną lub pobierane z magazynu DVC.
4. **Wyniki nie zależą od lokalnego katalogu.** Metryki i małe raporty trafiają do repozytorium, a modele do rejestru, magazynu artefaktów albo artefaktów CI.
5. **Obliczenia są krótkie i tanie.** Ćwiczenia używają małych danych oraz modeli działających na CPU w kilka minut.
6. **CI pełni rolę czystej maszyny referencyjnej.** Student sprawdza, czy projekt działa od zera poza jego bieżącym komputerem.
7. **Sekrety nie trafiają do repozytorium.** Tokeny przekazuje się jako zmienne środowiskowe lub sekrety CI. Po zajęciach student wylogowuje się z usług.

Preferowane jest przeglądarkowe środowisko programistyczne powiązane z repozytorium. W wariancie lokalnym każde zajęcia rozpoczynają się od sklonowania repozytorium i odtworzenia środowiska, a kończą zatwierdzeniem oraz wysłaniem zmian. Docker, Kubernetes i GPU nie powinny być wymagane na komputerze w sali. Odpowiednie ćwiczenia można wykonać na współdzielonym runnerze CI lub udostępnionym przez prowadzącego środowisku demonstracyjnym.

## 4. Program 13 spotkań

### Spotkanie 1. Od modelu w notebooku do systemu ML

**Zagadnienia**

- cele MLOps i problemy występujące po zakończeniu eksperymentu;
- cykl życia systemu ML: dane, trening, walidacja, rejestr, wdrożenie, obserwacja i ponowne trenowanie;
- role zaangażowane w utrzymanie systemu ML oraz ich odpowiedzialność;
- poziomy dojrzałości MLOps;
- przykład długu technicznego i sprzężeń zwrotnych w systemie ML.

**Zadanie**

Po części organizacyjnej studenci uruchamiają przygotowany notebook: wczytują mały zbiór danych, wykonują podstawową kontrolę jakości, trenują model bazowy, obliczają metryki i zapisują wykres macierzy pomyłek.

**Rezultat w repozytorium:** indywidualny notebook z uruchomionymi komórkami i krótkim podsumowaniem wyniku.

### Spotkanie 2. Powtarzalne środowisko i szkielet projektu

**Zagadnienia**

- struktura repozytorium ML i oddzielenie kodu od danych oraz artefaktów;
- deklarowanie i przypinanie zależności;
- konfiguracja przez pliki i zmienne środowiskowe;
- deterministyczność, ziarna losowości i ograniczenia reprodukowalności;
- skrypt uruchomieniowy, `Makefile` lub równoważne zadania projektowe.

**Zadanie**

Studenci przekształcają prosty notebook w pakiet z komendami `prepare`, `train` i `evaluate`, a następnie uruchamiają własny projekt w czystym środowisku.

**Rezultat w repozytorium:** odtwarzalny szkielet projektu i instrukcja uruchomienia.

### Spotkanie 3. Wersjonowanie, walidacja, kontrakty danych i cechy

**Zagadnienia**

- wersjonowanie kodu, danych i metadanych;
- DVC lub prosty manifest danych z adresem, wersją i sumą kontrolną;
- schemat danych, testy jakości, brakujące wartości i wycieki danych;
- pochodzenie danych, licencje, dane osobowe i retencja;
- różnica między zmianą danych a zmianą kodu;
- kroki potoku i graf zależności;
- idempotencja, pamięć podręczna i przyrostowe przetwarzanie;
- cechy obliczane w trybie wsadowym i online;
- training-serving skew oraz point-in-time correctness;
- kiedy potrzebny jest feature store, a kiedy jest zbędną komplikacją.

**Zadanie**

Studenci tworzą manifest zbioru, automatyczną walidację jego schematu oraz wspólną transformację cech używaną podczas treningu i predykcji. Test ma wykryć zmianę kontraktu oraz rozbieżność między obiema ścieżkami.

**Rezultat w repozytorium:** manifest danych, raport walidacji, etap cech i test zgodności.

### Spotkanie 4. Śledzenie eksperymentów i wybór modelu

**Zagadnienia**

- parametry, metryki, tagi, artefakty i kontekst uruchomienia;
- MLflow Tracking lub równoważne narzędzie;
- model bazowy, poprawny podział danych i unikanie wybierania modelu na zbiorze testowym;
- metryki techniczne i biznesowe;
- porównywalność eksperymentów i błędy „ręcznego” notowania wyników.

**Zadanie**

Studenci wykonują kilka kontrolowanych eksperymentów, zapisują parametry i artefakty, a następnie wybierają model według wcześniej zdefiniowanego kryterium.

**Rezultat w repozytorium:** kod eksperymentu, tabela porównawcza i uzasadniony wybór modelu.

### Spotkanie 5. Testowanie systemów ML

**Zagadnienia**

- testy jednostkowe transformacji i testy integracyjne potoku;
- testy danych, niezmienników oraz oczekiwań statystycznych;
- testy modelu: próg jakości, stabilność, wydajność i przypadki brzegowe;
- testy kontraktu wejścia i wyjścia;
- testy odporne na losowość oraz typowe przykłady testów kruchych.

**Zadanie**

Studenci uzupełniają zestaw testów dla celowo wadliwego potoku. Testy mają wykryć wyciek etykiety, błędny typ kolumny, spadek jakości i zmianę kontraktu predykcji.

**Rezultat w repozytorium:** zestaw testów uruchamiany jedną komendą.

### Spotkanie 6. Orkiestracja potoków treningowych

**Zagadnienia**

- zależności, harmonogram, stan i ponawianie zadań;
- rozdzielenie logiki ML od logiki orkiestratora;
- lokalny DAG w DVC, Prefect, Dagster, Airflow lub narzędziu uczelnianym;
- retry, timeout, backfill i obsługa częściowej awarii;
- artefakty i lineage pomiędzy krokami.

**Zadanie**

Studenci składają etapy `validate → featurize → train → evaluate` w DAG. Celowo wywołują awarię jednego etapu i sprawdzają, które kroki trzeba wykonać ponownie.

**Rezultat w repozytorium:** definicja potoku i zapis udanego oraz nieudanego przebiegu.

### Spotkanie 7. Pakowanie, rejestr i udostępnianie modelu

**Zagadnienia**

- model jako artefakt: wagi, kod, zależności i sygnatura;
- formaty serializacji oraz ryzyko uruchamiania niezaufanych artefaktów;
- rejestr modeli, wersje, aliasy i metadane;
- bramki jakości i przejście `candidate → staging → production`;
- karta modelu i decyzja o zatwierdzeniu;
- wybór między batch, request-response i streamingiem;
- API predykcyjne, walidacja żądania i wersjonowanie kontraktu;
- opóźnienie, przepustowość, koszt i dostępność;
- obsługa błędów, health check i bezpieczne logowanie;
- prosty serwer FastAPI lub równoważny.

**Zadanie**

Studenci pakują model razem z sygnaturą i metrykami, rejestrują jego wersję, a następnie udostępniają go jako endpoint HTTP albo komendę wsadową. Tworzą test kontraktu i regułę odrzucającą model niespełniający progu jakości.

**Rezultat w repozytorium:** wersjonowany model, kod predykcji, test kontraktu i reguła promocji.

### Spotkanie 8. Kontenery i ciągła integracja

**Zagadnienia**

- obraz kontenera, warstwy, niezmienność i minimalizacja obrazu;
- wieloetapowe budowanie oraz uruchamianie bez uprawnień administratora;
- CI dla kodu ML: lint, testy, walidacja danych, trening próbny i budowa obrazu;
- cache, artefakty CI oraz koszt wykonania;
- software bill of materials i skanowanie zależności.

**Zadanie**

Studenci przygotowują kontener usługi i potok CI. Każdy merge request ma uruchomić szybkie testy oraz trening na próbce danych. Budowę obrazu można wykonać wyłącznie na runnerze CI.

**Rezultat w repozytorium:** `Dockerfile`, konfiguracja CI i odnośnik do udanego przebiegu.

### Spotkanie 9. Dostarczanie i strategie wdrożeń

**Zagadnienia**

- różnica między CI, CD i CT;
- środowiska dev, staging i production;
- wdrożenia rolling, blue-green, canary, shadow i A/B;
- zgodność wsteczna, migracja cech i rollback;
- infrastruktura jako kod oraz deklaratywna konfiguracja — przegląd;
- Kubernetes/KServe jako przykład, bez wymagania lokalnego klastra.

**Zadanie**

Na symulatorze lub współdzielonym środowisku studenci kierują część ruchu do nowej wersji modelu, porównują metryki i podejmują automatyczną decyzję o promocji albo wycofaniu.

**Rezultat w repozytorium:** manifest wdrożenia, kryteria promocji i procedura rollbacku.

### Spotkanie 10. Obserwowalność i monitoring modeli

**Zagadnienia**

- logi, metryki, ślady i identyfikatory żądań;
- metryki systemowe, danych, predykcji, jakości i wartości biznesowej;
- opóźnione etykiety i monitoring bez etykiet;
- dashboard, SLI/SLO, alerty i ograniczanie liczby fałszywych alarmów;
- prywatność oraz bezpieczne próbkowanie danych wejściowych.

**Zadanie**

Studenci analizują strumień logów z działającego modelu, definiują wskaźniki i budują prosty dashboard lub raport. Konfigurują alert dla wzrostu błędów i zmiany rozkładu wejścia.

**Rezultat w repozytorium:** definicje metryk, raport i reguły alertów.

### Spotkanie 11. Dryf, ciągłe trenowanie i reakcja na incydent

**Zagadnienia**

- data drift, concept drift, quality drift i training-serving skew;
- detekcja zmian rozkładu oraz ograniczenia testów statystycznych;
- wyzwalacze ponownego treningu: czas, dane, wynik i decyzja człowieka;
- walidacja challengera względem championa;
- runbook, analiza przyczyn źródłowych i pętla informacji zwrotnej.

**Zadanie**

Studenci implementują wykrywanie dryfu dla danych referencyjnych i bieżących, generują raport, a następnie uruchamiają ponowny trening. Skrypt porównuje nowy model z dotychczasowym i automatycznie zapisuje decyzję o promocji albo odrzuceniu.

**Rezultat w repozytorium:** kod detekcji dryfu, raport, przebieg ponownego treningu i wynik automatycznego porównania modeli.

### Spotkanie 12. Bezpieczeństwo, governance i nowe obszary MLOps

**Zagadnienia**

- zagrożenia łańcucha dostaw, dane trujące, kradzież modelu i nadużycie endpointu;
- kontrola dostępu, zarządzanie sekretami, pochodzenie i podpisywanie artefaktów;
- rejestr ryzyk, karta modelu, audytowalność, fairness i nadzór człowieka;
- podstawy LLMOps: wersjonowanie promptów, ewaluacja jakości, tracing, koszt i bezpieczeństwo RAG;
- co pozostaje wspólne dla klasycznego MLOps i systemów generatywnych.

**Zadanie**

Każdy student dodaje do własnego projektu automatyczną kontrolę bezpieczeństwa lub governance, np. skan zależności, test obecności sekretów albo bramkę jakości. W krótkim ćwiczeniu porównuje też dwie wersje promptu na stałym zestawie przypadków testowych.

**Rezultat w repozytorium:** konfiguracja automatycznej kontroli, jej wynik oraz raport porównania promptów.

### Spotkanie 13. Prezentacje projektów i przegląd produkcyjny

**Zagadnienia**

- demonstracja projektu od świeżego klonu lub przez przebieg CI;
- obrona decyzji architektonicznych;
- „game day”: indywidualna reakcja autora projektu na wylosowaną awarię;
- wzajemny przegląd projektów i retrospektywa.

**Zadanie**

Każdy student ma 6–8 minut na prezentację, demonstrację powtarzalności i reakcję na scenariusz awarii. Prowadzący zadaje pytanie dotyczące działania całego systemu.

**Rezultat:** wersja projektu oznaczona tagiem, krótka prezentacja i protokół demonstracji.

## 5. Projekt zaliczeniowy

### Cel

Każdy student samodzielnie buduje mały, lecz kompletny i możliwy do odtworzenia system ML. Projekt, repozytorium, implementacja, dokumentacja i obrona mają charakter indywidualny. Ocenie podlega przede wszystkim jakość procesu, automatyzacja, niezawodność i uzasadnienie decyzji, a nie maksymalna wartość metryki modelu.

Studenci samodzielnie wybierają zbiór danych, na przykład z platformy Kaggle, repozytorium UCI Machine Learning Repository lub innego publicznego źródła, a następnie przygotowują adekwatny do problemu model. Dokumentacja projektu musi zawierać:

- krótką charakterystykę zbioru danych, w tym jego źródło, licencję, rozmiar, strukturę, zmienną objaśnianą oraz najważniejsze ograniczenia jakościowe;
- opis problemu ML i sposobu przygotowania danych;
- opis wybranego modelu oraz uzasadnienie, dlaczego jest odpowiedni dla danych i celu projektu;
- porównanie modelu z prostym rozwiązaniem bazowym;
- wskazanie ograniczeń modelu i sytuacji, w których jego predykcje mogą być niewiarygodne.

Projekt rozwijany jest przyrostowo:

1. **po spotkaniu 2:** repozytorium, problem i instrukcja uruchomienia;
2. **po spotkaniu 4:** dane, model bazowy i zapisane eksperymenty;
3. **po spotkaniu 7:** testowalny potok, wersjonowany model i sposób predykcji;
4. **po spotkaniu 9:** CI, sposób dostarczania i procedura wycofania;
5. **po spotkaniu 12:** monitoring, ryzyka i kompletna dokumentacja.

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

## 6. Poziomy projektu odpowiadające ocenom

Poziomy są **kumulatywne**. Aby otrzymać daną ocenę, projekt musi spełnić wymagania tej oceny oraz wszystkich ocen niższych. Samo dodanie narzędzia bez wykazania jego roli nie spełnia wymagania.

### Ocena 3,0 — powtarzalny eksperyment

- jasno opisany problem, użytkownik systemu, dane i metryka sukcesu;
- samodzielnie wybrany publiczny zbiór danych wraz z krótką charakterystyką, źródłem i licencją;
- model adekwatny do problemu wraz z opisem i uzasadnieniem jego wyboru;
- indywidualne repozytorium z historią pracy studenta;
- jedna komenda uruchamia przygotowanie danych, trening i ewaluację;
- przypięte zależności, konfiguracja poza kodem i ustalone ziarna losowości;
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
- porównanie co najmniej trzech kontrolowanych eksperymentów;
- karta modelu opisująca przeznaczenie, dane, wyniki i ograniczenia.

### Ocena 4,0 — automatyczne budowanie i udostępnianie

Wszystko z poziomu 3,5 oraz:

- CI uruchamiające testy, walidację i krótki trening kontrolny na czystym runnerze;
- model udostępniony jako usługa API albo niezawodne zadanie wsadowe;
- jawny, wersjonowany kontrakt wejścia i wyjścia oraz jego test;
- kontener lub równoważny przenośny artefakt wykonawczy budowany automatycznie;
- rejestr wersji modeli z metadanymi i regułą promocji;
- skan zależności lub obrazu oraz brak sekretów w repozytorium.

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

## 7. Wspólne warunki zaliczenia i sposób oceny

Niezależnie od deklarowanego poziomu:

- projekt musi działać z repozytorium lub przez CI bez dostępu do poprzedniego komputera studenta;
- instrukcja odtworzenia musi zostać sprawdzona przez inną osobę;
- dane i wykorzystane komponenty muszą mieć wskazane źródło oraz licencję;
- sekrety, dane osobowe i duże binarne artefakty nie mogą znaleźć się w historii Git;
- student musi samodzielnie zaprezentować projekt i rozumieć cały przepływ;
- niedziałająca demonstracja może zostać zastąpiona pełnym zapisem udanego przebiegu CI, jeśli awaria nie wynika z projektu;
- poważny błąd metodologiczny, wyciek danych albo brak możliwości odtworzenia wyniku ogranicza ocenę do 3,0 do czasu poprawy.

Proponowane wagi pomocnicze:

| Obszar | Waga |
|---|---:|
| Powtarzalność, dane i eksperymenty | 20% |
| Potok, testy i jakość kodu | 20% |
| CI, pakowanie i sposób udostępnienia | 20% |
| Monitoring, niezawodność i bezpieczeństwo | 20% |
| Dokumentacja, decyzje architektoniczne i obrona | 20% |

Poziom funkcjonalny określa najwyższą możliwą ocenę, a jakość realizacji obszarów z tabeli pozwala ją potwierdzić lub obniżyć.

## 8. Minimalna infrastruktura dla prowadzącego

- szablon repozytorium z małym przykładowym zbiorem i skryptem bootstrap;
- uczelniany GitLab/GitHub z runnerem CI;
- współdzielony serwer śledzenia eksperymentów i rejestr artefaktów albo wariant lokalny uruchamiany w CI;
- rejestr obrazów kontenerowych;
- jedno demonstracyjne środowisko wdrożeniowe lub symulator ruchu i wdrożeń;
- zapasowy wariant ćwiczeń niewymagający Dockera ani usług chmurowych;
- krótkotrwałe dane uwierzytelniające i instrukcja bezpiecznego wylogowania;
- niewielkie, wersjonowane zestawy danych przygotowane przed semestrem.

## 9. Rekomendowane źródła i dokumentacja

- Google Cloud, **MLOps: Continuous delivery and automation pipelines in machine learning**:
  <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning>
- MLflow, **Tracking, Model Registry, Evaluation i Tracing**:
  <https://mlflow.org/docs/latest/>
- DVC, **Data Versioning i Data Pipelines**:
  <https://doc.dvc.org/>
- OpenLineage, **standard metadanych o pochodzeniu danych i zadań**:
  <https://openlineage.io/docs/>
- Feast, **feature store**:
  <https://docs.feast.dev/>
- KServe, **model serving na Kubernetes**:
  <https://kserve.github.io/website/>
- Evidently, **ewaluacja i monitoring systemów ML**:
  <https://docs.evidentlyai.com/>
- NIST, **AI Risk Management Framework**:
  <https://www.nist.gov/itl/ai-risk-management-framework>
- SLSA, **bezpieczeństwo łańcucha dostaw oprogramowania**:
  <https://slsa.dev/>

Dokumentację narzędzi należy weryfikować przed każdą edycją przedmiotu. W ćwiczeniach warto konsekwentnie oceniać praktykę MLOps, a nie znajomość składni konkretnej platformy.
