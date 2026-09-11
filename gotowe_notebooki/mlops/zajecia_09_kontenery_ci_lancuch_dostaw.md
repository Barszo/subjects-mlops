# Zajęcia 9. Kontenery, ciągła integracja i łańcuch dostaw

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 8, testy i usługa predykcyjna we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_09.ipynb`, Docker Desktop oraz konto GitHub
- **Rezultat:** `Dockerfile`, zbudowany obraz, workflow GitHub Actions, SBOM, skan zależności i skan sekretów

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. buduje obraz kontenera zgodnie z podstawowymi zasadami bezpieczeństwa i rozmiaru;
2. projektuje potok CI dla projektu ML i zna kolejność jego kroków;
3. panuje nad czasem i kosztem przebiegu CI;
4. rozpoznaje zagrożenia łańcucha dostaw w projekcie ML;
5. generuje SBOM i wie, czym różni się od niego ML-BOM;
6. wykrywa podatne zależności i sekrety w repozytorium.

## 2. Po co kontener

Kontener rozwiązuje jeden problem: **przenosi środowisko razem z kodem**. Zamiast instrukcji „zainstaluj Pythona 3.12, te biblioteki i ustaw te zmienne”, dostajemy niezmienny artefakt, który uruchomi się tak samo na komputerze studenta, na runnerze CI i na serwerze.

Cechy dobrego obrazu:

| Zasada | Dlaczego |
|---|---|
| **Niezmienność** | ten sam obraz w dev, staging i produkcji; zmiana = nowy obraz |
| **Minimalizacja** | mniejsza powierzchnia ataku i krótszy czas pobierania |
| **Budowanie wieloetapowe** | narzędzia kompilacji zostają w etapie budowania, nie trafiają do obrazu wynikowego |
| **Brak uprawnień administratora** | proces działa jako zwykły użytkownik |
| **Przypięty obraz bazowy** | `python:3.12-slim`, nie `python:latest` |
| **Uporządkowana kolejność warstw** | najpierw zależności, potem kod — cache działa wtedy naprawdę |
| **`.dockerignore`** | do obrazu nie trafiają dane, artefakty, `.venv` ani `.git` |

Typowy błąd w projektach ML: kopiowanie całego katalogu projektu razem z danymi i modelami. Obraz rośnie do gigabajtów, a przy okazji wynosi na zewnątrz dane, których wynosić nie wolno.

### Model w obrazie czy obok obrazu?

Dwa podejścia, oba poprawne, ale trzeba wybrać świadomie:

- **model w obrazie** — jeden artefakt, prosty rollback, ale każda nowa wersja modelu wymaga przebudowy;
- **model pobierany przy starcie** z rejestru — obraz jest stabilny, ale wdrożenie zależy od dostępności rejestru i trudniej odtworzyć stan sprzed tygodnia.

## 3. Potok CI dla projektu ML

CI jest **czystą maszyną referencyjną**. Jego zadaniem nie jest przyspieszenie pracy, tylko odpowiedź na pytanie „czy to działa poza komputerem autora”.

Kolejność kroków wynika z kosztu: najpierw to, co szybkie i najczęściej zawodzi.

```text
1. instalacja zależności z pliku blokady
2. kontrola stylu i statyczna analiza kodu
3. testy jednostkowe i testy kontraktu
4. walidacja danych na małej próbce
5. trening kontrolny na próbce
6. skan zależności i wykrywanie sekretów
7. budowa obrazu i wygenerowanie SBOM
```

Zasady:

- **każdy krok kończy się jednoznacznym wynikiem** — zielony albo czerwony, bez „ostrzeżeń do przejrzenia”;
- **trening w CI jest kontrolny**, na próbce danych, liczony w sekundach; pełny trening należy do potoku, nie do CI;
- **cache zależności** jest obowiązkowy, inaczej każdy przebieg kosztuje kilka minut samej instalacji;
- **artefakty przebiegu** (raport testów, metryki, SBOM) zapisujemy, bo bez nich nie da się zdiagnozować czerwonego przebiegu.

### Budżet czasu i kosztu

Przebieg CI powyżej dziesięciu minut przestaje być używany do weryfikacji zmian — ludzie przełączają się na inne zadanie i tracą kontekst. W projekcie studenckim rozsądny cel to **poniżej trzech minut**. Osiąga się to próbką danych, cache i podziałem na przebieg szybki (każda zmiana) i pełny (przed wydaniem).

GitHub Actions rozlicza czas działania. Dla repozytoriów publicznych jest darmowy, dla prywatnych ma miesięczny limit minut — warto to sprawdzić przed semestrem, bo dwadzieścia projektów po kilka przebiegów dziennie potrafi ten limit wyczerpać.

### Konkrety GitHub Actions

| Element | Do czego służy |
|---|---|
| `on: [push, pull_request]` | przebieg przy każdej zmianie i przy każdym zgłoszeniu zmiany |
| `actions/setup-python` z `cache: pip` | pamięć podręczna zależności między przebiegami |
| `actions/upload-artifact` | zapis raportów, SBOM i metryk, dostępnych po przebiegu |
| `timeout-minutes` | ochrona przed zawieszonym zadaniem, które zjada limit |
| `permissions` | najwęższe uprawnienia tokenu; do publikacji obrazu potrzebne `packages: write` |
| **Ochrona gałęzi** | scalenie do `main` możliwe dopiero po zielonym przebiegu |

Ostatni punkt jest najważniejszy organizacyjnie. Potok CI, który można zignorować, nie chroni przed niczym. Wymaganie zielonego przebiegu przed scaleniem zamienia go w rzeczywistą bramkę.

### Rejestr obrazów

Zbudowany obraz trafia do rejestru — dla repozytoriów GitHub jest to `ghcr.io`, dostępny bez dodatkowej konfiguracji poza uprawnieniem `packages: write`. Obraz identyfikujemy **digestem**, nie tagiem: tag można przenieść, digest jest niezmienny. Do tego rozróżnienia wracamy na zajęciach 10, bo od niego zależy sensowność wycofania.

## 4. Łańcuch dostaw w projekcie ML

Projekt ML ma szerszy łańcuch dostaw niż zwykła aplikacja, bo poza kodem konsumuje **dane** i **modele**.

| Element | Zagrożenie | Kontrola |
|---|---|---|
| Zależności | podatność, przejęty pakiet, literówka w nazwie | plik blokady, skan, przegląd nowych zależności |
| Obraz bazowy | nieaktualne biblioteki systemowe | przypięcie wersji, regularna przebudowa |
| Dane | dane zatrute albo podmienione | suma kontrolna z zajęć 3, kontrola źródła |
| Model | artefakt wykonujący kod przy wczytaniu (zajęcia 7) | zaufane źródło, bezpieczniejszy format, atestacja |
| Artefakt budowania | podmiana między budową a wdrożeniem | atestacja pochodzenia, podpis |

### SBOM i ML-BOM

**SBOM** (Software Bill of Materials) to lista składników artefaktu: nazwa, wersja, identyfikator, licencja. Odpowiada na pytanie „czy nas dotyczy podatność ogłoszona dziś rano” w minutę zamiast w tydzień.

**ML-BOM** to rozszerzenie tej listy o składniki charakterystyczne dla ML: **model** (wersja, pochodzenie, metryki) oraz **zbiór danych** (źródło, wersja, licencja). Bez tego rozszerzenia zestawienie składników projektu ML jest niekompletne, bo pomija dwa najważniejsze elementy.

### Narzędzia, których używamy

| Zadanie | Narzędzie | Gdzie działa |
|---|---|---|
| Podatności w zależnościach Pythona | `pip-audit` (baza PyPI Advisory) | lokalnie i w CI |
| Podatności w obrazie kontenera | `trivy` (akcja `aquasecurity/trivy-action`) | w CI |
| Sekrety w kodzie i historii | `gitleaks` (hak `pre-commit` oraz akcja w CI) | lokalnie i w CI |
| SBOM i atestacja pochodzenia | `docker buildx --sbom=true --provenance=true` | lokalnie i w CI |
| Składniki ML w zestawieniu | własny krok rozszerzający SBOM o model i zbiór danych | lokalnie i w CI |

Ważna różnica względem wcześniejszych zajęć: to są **prawdziwe narzędzia z aktualnymi bazami**, a nie uproszczone odpowiedniki. Wynik skanu zależy od dnia, w którym go uruchomisz — i to jest pożądane.

### Atestacja i podpis

Atestacja pochodzenia (*provenance*) to podpisane oświadczenie: „ten artefakt powstał z tego commita, tym potokiem, o tej godzinie”. Podpis pozwala je zweryfikować przed wdrożeniem. To poziom rozszerzenia dla oceny 5,0, ale warto wiedzieć, że problem „skąd wziął się ten obraz” ma standardowe rozwiązanie.

## 5. Sekrety w repozytorium

Sekret, który raz trafił do historii Git, jest w niej na zawsze — usunięcie pliku kolejnym commitem niczego nie naprawia. Dlatego:

- wykrywanie sekretów działa **przed** commitem (hak `pre-commit` z `gitleaks`) i **w CI** (na całej historii);
- sekret wykryty w historii wymaga **unieważnienia i wymiany**, nie tylko usunięcia z plików;
- w repozytorium trzymamy wyłącznie plik przykładowy `.env.example` bez wartości;
- wartości przekazujemy przez **sekrety repozytorium** (Settings → Secrets and variables → Actions), do których workflow sięga przez `${{ secrets.NAZWA }}`;
- typowe miejsca wycieku w projektach ML: notebook z tokenem w komórce, plik konfiguracyjny z hasłem do bazy, wynik `print` w logu CI.

### Hak przed commitem

`pre-commit` uruchamia zestaw kontroli lokalnie, zanim zmiana trafi do repozytorium. Minimalny zestaw w tym przedmiocie to `gitleaks` (sekrety) i `ruff` (styl oraz proste błędy):

```bash
pre-commit install
pre-commit run --all-files
```

Pierwsze uruchomienie pobiera narzędzia, więc wymaga sieci. Później działa lokalnie i kosztuje sekundy.

## 6. Ćwiczenie praktyczne

### Cel

Zbudowanie obrazu kontenera, uruchomienie go, przygotowanie workflow GitHub Actions oraz kontroli łańcucha dostaw: SBOM, skan zależności i skan sekretów.

Ćwiczenie składa się z trzech części:

1. **Lokalnie w notebooku** — `Dockerfile`, kontrola jego jakości, budowa obrazu, test dymny uruchomionego kontenera, `pip-audit`, SBOM z ML-BOM.
2. **Symulator potoku** — wykonanie kroków workflow lokalnie, żeby zobaczyć kolejność i skutki błędu bez czekania na runnera.
3. **Na GitHubie** — wysłanie repozytorium, obserwacja przebiegu, publikacja obrazu do `ghcr.io`, włączenie ochrony gałęzi.

Część pierwsza wymaga uruchomionego Dockera; komórki, które go potrzebują, są wyraźnie oznaczone i przy jego braku wypisują komendy do samodzielnego wykonania. Część trzecia odbywa się poza notebookiem.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_09.ipynb`.

### Punkty kontrolne

1. **Podatna zależność.** Dodaj do pliku zależności bibliotekę w wersji z podatnością. Co zgłosił `pip-audit` i który krok potoku został przez to zatrzymany?
2. **Sekret w repozytorium.** Wprowadź do pliku klucz API i spróbuj utworzyć commit. Czy hak `pre-commit` go zatrzymał i co należy zrobić poza usunięciem linii?
3. **Czerwony test.** Zepsuj jeden test. Który krok potoku zawiódł i czy obraz został zbudowany mimo błędu?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_09/
    └── projekt/
        ├── Dockerfile
        ├── .dockerignore
        ├── .pre-commit-config.yaml
        ├── .github/workflows/ci.yml
        ├── src/, tests/, requirements.txt
        └── reports/{sbom.json,pip_audit.json,secret_scan.json,ci_run.json}
```

## 7. Zadanie projektowe (po zajęciach)

1. Napisz `Dockerfile` dla swojego projektu: budowanie wieloetapowe, przypięty obraz bazowy, użytkownik bez uprawnień administratora, `.dockerignore`.
2. Zbuduj obraz lokalnie i uruchom **test dymny** — kontener wstaje i odpowiada na sprawdzenie stanu.
3. Wyślij projekt na GitHuba i skonfiguruj workflow uruchamiany przy każdej zmianie: kontrola stylu, testy, walidacja danych, trening kontrolny na próbce.
4. Doprowadź przebieg CI do czasu **poniżej trzech minut**, wykorzystując cache zależności.
5. Opublikuj obraz do `ghcr.io` i zapisz jego **digest** w artefaktach przebiegu.
6. Wygeneruj **SBOM** i rozszerz go o składniki ML: model i zbiór danych.
7. Włącz `pip-audit`, skan obrazu oraz `gitleaks` jako kroki blokujące; wyniki zapisz jako artefakty.
8. Dodaj hak `pre-commit` z `gitleaks` i `ruff`.
9. Włącz **ochronę gałęzi** `main`: scalenie możliwe dopiero po zielonym przebiegu.
10. Opisz w dokumentacji, czy model jest w obrazie, czy pobierany przy starcie, i uzasadnij wybór.

**Kryterium ukończenia:** zgłoszenie zmiany z czerwonym testem nie da się scałić do `main`, a obraz dla tej zmiany nie powstaje.

## 8. Co wymaga sprawdzenia przed zajęciami

Części wykonywanych na zewnątrz nie da się zweryfikować z poziomu notebooka. Przed spotkaniem należy sprawdzić samodzielnie:

- czy Docker Desktop działa na komputerach w sali i czy `docker buildx` obsługuje `--sbom` oraz `--provenance`;
- czy studenci mogą zakładać repozytoria i czy mają dostępne minuty GitHub Actions;
- czy publikacja do `ghcr.io` działa przy uprawnieniu `packages: write`;
- czy `pre-commit run --all-files` przechodzi przy pierwszym, pobierającym uruchomieniu.

## 8. Literatura

1. Docker, **Best practices for writing Dockerfiles**:
   <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>
2. Docker, **Build attestations — SBOM i provenance**:
   <https://docs.docker.com/build/attestations/>
3. CycloneDX, **specyfikacja SBOM oraz ML-BOM**:
   <https://cyclonedx.org/capabilities/mlbom/>
4. SLSA, **poziomy zabezpieczenia łańcucha dostaw**:
   <https://slsa.dev/>
5. OWASP, **CI/CD Security Top 10**:
   <https://owasp.org/www-project-top-10-ci-cd-security-risks/>
