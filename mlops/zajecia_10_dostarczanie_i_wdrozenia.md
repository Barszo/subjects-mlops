# Zajęcia 10. Dostarczanie i strategie wdrożeń

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 9, obraz opublikowany do `ghcr.io`, działający potok CI
- **Środowisko:** notebook `gotowe_notebooki/zajecia_10.ipynb`, `docker compose`, GitHub Actions
- **Rezultat:** dwa środowiska w `docker compose`, workflow dostarczania z bramką zatwierdzenia, wdrożenie canary z automatyczną decyzją, przetestowana procedura wycofania i model zagrożeń

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. odróżnia CI, CD i CT oraz wie, co należy do którego procesu;
2. promuje ten sam artefakt między środowiskami zamiast budować go ponownie;
3. opisuje stan docelowy wdrożenia deklaratywnie i uruchamia go przez `docker compose`;
4. buduje workflow dostarczania z bramką zatwierdzenia dla produkcji;
5. dobiera strategię zmiany wersji do ryzyka i kosztu;
6. definiuje kryteria automatycznej promocji i wycofania;
7. buduje model zagrożeń dla wdrożonej usługi ML.

## 2. CI, CD i CT

| Skrót | Co uruchamia | Co jest wynikiem |
|---|---|---|
| **CI** — ciągła integracja | zmiana w kodzie | zweryfikowany artefakt (obraz, pakiet) |
| **CD** — ciągłe dostarczanie | zatwierdzony artefakt | działająca wersja w środowisku |
| **CT** — ciągłe trenowanie | nowe dane, harmonogram, sygnał z monitoringu | nowa wersja modelu, kandydat do wdrożenia |

W zwykłej aplikacji istnieją dwa pierwsze procesy. W systemie ML dochodzi trzeci, bo **model może się zdezaktualizować bez żadnej zmiany w kodzie**. To najważniejsza różnica organizacyjna między MLOps a klasycznym DevOps.

Trzy procesy oznaczają trzy niezależne wyzwalacze i trzy niezależne bramki jakości. CT bez bramki to automat, który prędzej czy później wdroży gorszy model.

## 3. Jeden artefakt, wiele środowisk

Podstawowa zasada dostarczania: **artefakt buduje się raz**, a następnie promuje między środowiskami. Ponowna budowa dla produkcji oznacza, że testowano co innego, niż wdrożono.

```text
CI buduje obraz  →  dev  →  staging  →  production
      (jeden i ten sam artefakt, identyfikowany sumą kontrolną)
```

Między środowiskami zmienia się wyłącznie **konfiguracja**: adresy usług, poświadczenia, limity, poziom logowania. Nigdy kod ani zawartość obrazu.

W praktyce oznacza to jedną konkretną decyzję: wdrażamy obraz **po digeście**, nie po znaczniku.

```text
ghcr.io/uzytkownik/projekt:v1.4        ← znacznik, można go przesunąć
ghcr.io/uzytkownik/projekt@sha256:9f3c…  ← digest, identyfikuje dokładnie jedną zawartość
```

Znacznik `v1.4` może jutro wskazywać inny obraz. Digest nie może. Jeżeli wdrożenie odwołuje się do znacznika, tracimy odpowiedź na pytanie „co dokładnie działa na produkcji” — a to jest pytanie, które pada podczas każdego incydentu.

Środowiska różnią się też celem:

- **dev** — szybka pętla zwrotna, dane syntetyczne, brak gwarancji;
- **staging** — możliwie wierne odwzorowanie produkcji, dane zbliżone do rzeczywistych, tu odbywa się test kontraktu i test wydajności;
- **production** — ruch użytkowników, pełny monitoring, kontrolowana zmiana.

## 4. Deklaratywny opis stanu docelowego

Zamiast wykonywać sekwencję poleceń wdrożeniowych, zapisujemy w repozytorium, **jak środowisko ma wyglądać**:

```yaml
environment: production
image: ghcr.io/uzytkownik/projekt@sha256:9f3c...
model:
  name: iris_classifier
  version: 4
traffic:
  champion: 100
  challenger: 0
```

Proces uzgadniający porównuje stan rzeczywisty z zapisanym i doprowadza system do zgodności. Zalety:

- **historia zmian wdrożeń** jest historią repozytorium — wiadomo kto, kiedy i co zmienił;
- **wycofanie** to cofnięcie zmiany w pliku, a nie improwizacja pod presją;
- **stan rzeczywisty nie rozjeżdża się** z opisem, bo uzgadnianie działa w pętli;
- **uprawnienia do produkcji** ma proces, a nie człowiek.

W tym przedmiocie warstwą wykonawczą jest `docker compose`: plik `compose.yaml` opisuje usługi, a `docker compose up -d` doprowadza maszynę do opisanego stanu. W większej skali tę samą rolę pełnią narzędzia GitOps (Argo CD, Flux) nad Kubernetesem — **zasada jest identyczna, różni się tylko warstwa wykonawcza**.

## 5. Dwa środowiska w `docker compose`

Staging i produkcja to dwa zestawy usług uruchomione z **tego samego obrazu**, różniące się wyłącznie plikiem konfiguracji:

```yaml
services:
  api-champion:
    image: ${IMAGE_DIGEST}
    env_file: env/${ENVIRONMENT}.env
    volumes:
      - ./models:/app/models:ro
  api-challenger:
    image: ${CHALLENGER_DIGEST}
    env_file: env/${ENVIRONMENT}.env
  router:
    image: nginx:1.27-alpine
    ports:
      - "${PUBLIC_PORT}:80"
```

Router (`nginx`) rozdziela ruch między obie wersje według wag. Zmiana udziału wersji kandydującej to zmiana jednej liczby w konfiguracji routera i przeładowanie — bez restartu usług i bez utraty żądań.

Dwie rzeczy warte podkreślenia:

- **środowiska są od siebie odizolowane** — osobne sieci, osobne porty, osobne wolumeny;
- **model jest podłączany jako wolumin**, więc wymiana modelu nie wymaga budowy obrazu. To decyzja, którą podjęliśmy na zajęciach 9; jej cena to konieczność wersjonowania modelu poza obrazem.

## 6. Workflow dostarczania

Dostarczanie uruchamiamy po scaleniu do `main`, gdy potok jakości z zajęć 9 zakończył się powodzeniem:

```text
merge do main
  → CI: testy, skanery, budowa obrazu, publikacja do ghcr (digest)
     → deploy-staging   (automatycznie)
        → test dymny i test kontraktu na stagingu
           → deploy-production   (po zatwierdzeniu przez człowieka)
```

Dwa mechanizmy GitHuba realizują tę bramkę:

| Mechanizm | Rola |
|---|---|
| **GitHub Environments** | nazwane środowiska z regułą *required reviewers* — zadanie czeka, aż ktoś je zatwierdzi |
| **self-hosted runner** | proces na maszynie docelowej, który wykonuje `docker compose up -d`; GitHub nie musi mieć dostępu do maszyny |

Runner samodzielny odwraca kierunek połączenia: to **maszyna docelowa łączy się z GitHubem**, a nie odwrotnie. Dzięki temu nie trzeba wystawiać maszyny na świat ani przekazywać do CI poświadczeń administracyjnych. Ten sam wzorzec stosuje się w środowiskach, do których CI nie ma i nie powinno mieć dostępu sieciowego.

Zatwierdzenie produkcji przez człowieka to **ciągłe dostarczanie** (continuous delivery). Usunięcie tej bramki daje **ciągłe wdrażanie** (continuous deployment). Wybór między nimi zależy od tego, czy monitoring i automatyczne wycofanie są na tyle dobre, żeby zastąpić decyzję człowieka.

## 7. Strategie zmiany wersji

| Strategia | Na czym polega | Kiedy stosować | Koszt |
|---|---|---|---|
| **Rolling** | stopniowa wymiana instancji | zmiany o niskim ryzyku | niski |
| **Blue-green** | dwa komplety środowiska, przełączenie ruchu | wymagane natychmiastowe wycofanie | wysoki (podwójne zasoby) |
| **Canary** | mały procent ruchu do nowej wersji, stopniowy wzrost | zmiana modelu o realnym wpływie | średni |
| **Shadow** | nowa wersja dostaje kopię ruchu, jej odpowiedzi nie trafiają do użytkownika | walidacja modelu na prawdziwym ruchu bez ryzyka | średni, podwójne obliczenia |
| **A/B** | równoległe wersje, porównanie **wyniku biznesowego** | pytanie „czy nowy model daje lepszy efekt”, nie „czy działa” | wysoki, wymaga istotności statystycznej |

Dla modeli ML szczególnie wartościowe są **shadow** i **canary**. Shadow odpowiada na pytanie „czy nowa wersja w ogóle zachowuje się rozsądnie na prawdziwych danych”, canary — „czy możemy jej powierzyć ruch”.

Uzupełnieniem jest **przełącznik funkcji**: możliwość wyłączenia modelu i przejścia na regułę zapasową bez wdrożenia. To najtańsza forma wycofania.

## 8. Automatyczna analiza i decyzja

Wdrożenie canary bez automatycznej analizy jest tylko wolniejszym wdrożeniem. Wartość pojawia się wtedy, gdy zdefiniowano **kryteria zatrzymania**:

1. metryka techniczna: udział błędów i opóźnienie nie gorsze niż w wersji obecnej;
2. metryka modelu: jakość nie niższa o więcej niż zadany margines;
3. metryka danych: rozkład wejścia porównywalny w obu wersjach;
4. minimalna liczba obserwacji, poniżej której decyzji nie podejmujemy.

Ostatni punkt jest najczęściej pomijany. Decyzja o promocji podjęta na trzydziestu żądaniach to podrzucenie monetą.

Wynik analizy może być tylko trojaki: **promuj**, **czekaj** (za mało danych), **wycofaj**. Nie ma opcji „wygląda w porządku, zostawmy".

## 9. Zgodność wsteczna i wycofanie

Wycofanie modelu jest łatwe, dopóki nie zmienia się nic poza modelem. Trudność pojawia się, gdy nowa wersja wymaga innych cech albo zwraca inny format.

| Zmiana | Czy da się wycofać samym przełączeniem wersji? |
|---|---|
| inne wagi modelu | tak |
| dodatkowe pole opcjonalne w odpowiedzi | tak |
| nowa wymagana cecha wejściowa | nie — potrzebna migracja po stronie klienta |
| zmiana znaczenia klas na wyjściu | nie — konsument interpretuje wynik błędnie |
| zmiana źródła cech | nie — trzeba wycofać też potok danych |

Stąd zasada: **zmiana modelu i zmiana kontraktu to dwa osobne wdrożenia**. Najpierw wprowadzamy zgodną wstecz zmianę kontraktu, potem model, który z niej korzysta.

### Procedura wycofania

Procedura wycofania musi być **zapisana i przetestowana**, a nie odtwarzana z pamięci w trakcie incydentu. Minimalny zakres:

- warunek uruchomienia — co dokładnie oznacza „wycofujemy";
- kto podejmuje decyzję i kto ją wykonuje;
- kroki wycofania i oczekiwany czas powrotu do stanu poprawnego;
- sposób potwierdzenia, że wycofanie zadziałało;
- co robimy z danymi, które powstały w czasie awarii.

Przy wdrożeniu po digeście wycofanie jest jedną operacją: podstawiamy poprzedni digest i uruchamiamy uzgadnianie. Poprzedni obraz jest nadal w rejestrze, więc nie trzeba niczego budować — a budowanie pod presją incydentu jest najgorszym momentem na wprowadzanie nowego artefaktu.

```bash
# wycofanie = ponowne wdrożenie poprzedniego digestu
IMAGE_DIGEST=ghcr.io/uzytkownik/projekt@sha256:1a7b... docker compose up -d
```

Czas tej operacji trzeba **zmierzyć**, a nie oszacować. To jedna z niewielu liczb, które realnie opisują dojrzałość procesu dostarczania.

## 10. Model zagrożeń dla wdrożonej usługi ML

Usługa predykcyjna wystawiona na zewnątrz ma kategorie zagrożeń, których nie ma zwykłe API:

| Zagrożenie | Na czym polega | Podstawowe ograniczenie ryzyka |
|---|---|---|
| **Nadużycie endpointu** | masowe odpytywanie w celu uzyskania darmowych predykcji | uwierzytelnianie, limity zapytań |
| **Kradzież modelu** | odtworzenie modelu na podstawie odpowiedzi | limity, ograniczenie szczegółowości wyjścia |
| **Wnioskowanie o danych treningowych** | ustalenie, czy konkretny rekord był w zbiorze | ograniczenie zwracanych prawdopodobieństw |
| **Dane trujące** | wpływ na model przez dane wracające do treningu | walidacja i przegląd danych zwrotnych |
| **Wejście adwersarialne** | spreparowane dane wymuszające błędną predykcję | walidacja zakresów, wykrywanie danych spoza dziedziny |
| **Podmiana artefaktu** | wdrożenie modelu z niezaufanego źródła | suma kontrolna, atestacja pochodzenia (zajęcia 9) |

Nie każdy projekt musi ograniczać wszystkie te ryzyka. Każdy powinien je **wymienić i świadomie zdecydować**, które akceptuje.

## 11. Ćwiczenie praktyczne

### Cel

Uruchomienie dwóch środowisk w `docker compose`, wdrożenie canary z automatyczną decyzją, tryb shadow, przetestowana procedura wycofania i model zagrożeń.

Notebook składa się z dwóch warstw:

- **warstwa wykonawcza** — `compose.yaml`, router `nginx`, wdrożenie po digeście i wycofanie; komórki oznaczone **[DOCKER]** wymagają działającego demona;
- **warstwa decyzyjna** — generator ruchu, analiza metryk i reguła promocji albo wycofania; działa bez Dockera, bo to jest część, którą piszesz sam.

Workflow dostarczania przygotowujemy w notebooku, ale uruchamiamy go na GitHubie — ta część jest opisana jako „poza notebookiem".

Pracujesz z notebookiem `gotowe_notebooki/zajecia_10.ipynb`.

### Punkty kontrolne

1. **Gorszy kandydat.** Wprowadź jako challengera model gorszy od obecnego. Co zrobiła automatyczna analiza i po ilu żądaniach?
2. **Złamana zgodność wsteczna.** Wdróż wersję zwracającą inny format odpowiedzi. Czy wystarczyło przełączenie wersji, żeby wrócić do stanu poprawnego?
3. **Wycofanie.** Zmierz czas od wykrycia problemu do przywrócenia poprawnego działania. Co zajęło najwięcej czasu?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_10/
    ├── wdrozenie/
    │   ├── compose.yaml
    │   ├── router/nginx.conf
    │   ├── env/staging.env
    │   ├── env/production.env
    │   └── .github/workflows/cd.yml
    ├── registry/           # artefakty modeli z sumami kontrolnymi
    └── reports/
        ├── deployment.yaml
        ├── canary_analysis.json
        ├── rollback_timing.json
        ├── rollback_runbook.md
        └── threat_model.md
```

### Co wymaga sprawdzenia przed zajęciami

- działający Docker Desktop i polecenie `docker compose version`;
- obraz z zajęć 9 opublikowany w `ghcr.io` i jego digest;
- zarejestrowany **self-hosted runner** na maszynie demonstracyjnej (Settings → Actions → Runners);
- utworzone środowiska `staging` i `production` w Settings → Environments, z regułą *required reviewers* dla produkcji.

## 12. Zadanie projektowe (po zajęciach)

1. Opisz stan docelowy wdrożenia **deklaratywnie**, w pliku w repozytorium.
2. Zapewnij, że ten sam artefakt jest promowany między środowiskami — wdrażany **po digeście**, bez ponownej budowy.
3. Zbuduj workflow dostarczania z automatycznym wdrożeniem na staging i **bramką zatwierdzenia** dla produkcji.
4. Zaimplementuj jedną strategię bezpiecznej zmiany wersji: canary, shadow albo blue-green.
5. Zdefiniuj **kryteria automatycznej promocji i wycofania**, wraz z minimalną liczbą obserwacji.
6. Napisz procedurę wycofania i **wykonaj ją co najmniej raz**, zapisując zmierzony czas powrotu do stanu poprawnego.
7. Sporządź model zagrożeń dla swojej usługi oraz rejestr ryzyk z decyzją dla każdego z nich.
8. Opisz, które zmiany w twoim projekcie **nie** dają się wycofać samym przełączeniem wersji modelu.

**Kryterium ukończenia:** wprowadzenie gorszej wersji modelu kończy się automatycznym wycofaniem bez udziału człowieka, a ślad tej decyzji jest zapisany.

## 13. Literatura

1. Google Cloud, **MLOps: Continuous delivery and automation pipelines in machine learning**:
   <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning>
2. GitHub Docs, **Using environments for deployment** (bramki zatwierdzenia):
   <https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment>
3. GitHub Docs, **Self-hosted runners**:
   <https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners>
4. Docker Docs, **Compose file reference**:
   <https://docs.docker.com/reference/compose-file/>
5. Argo Rollouts, **progressive delivery: canary i blue-green** (skala Kubernetesa):
   <https://argo-rollouts.readthedocs.io/>
6. Argo CD, **dostarczanie sterowane repozytorium** (skala Kubernetesa):
   <https://argo-cd.readthedocs.io/>
7. KServe, **canary rollout dla modeli**:
   <https://kserve.github.io/website/>
8. MITRE ATLAS, **taksonomia ataków na systemy ML**:
   <https://atlas.mitre.org/>
9. OWASP, **Machine Learning Security Top 10**:
   <https://owasp.org/www-project-machine-learning-security-top-10/>
