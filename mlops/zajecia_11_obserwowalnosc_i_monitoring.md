# Zajęcia 11. Obserwowalność i monitoring modeli

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 10, wdrożona usługa albo zadanie wsadowe
- **Środowisko:** notebook `gotowe_notebooki/zajecia_11.ipynb`; usługa z `prometheus-client`, stos Prometheus + Grafana + Jaeger w `docker compose`
- **Rezultat:** usługa eksportująca metryki, definicje metryk czterech warstw, SLI/SLO, reguły alertów, konfiguracja stosu i raport monitoringu

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. rozróżnia logi, metryki i ślady oraz wie, do czego służy każde z nich;
2. instrumentuje kod tak, aby dało się prześledzić pojedyncze żądanie;
3. definiuje metryki na czterech warstwach systemu ML;
4. radzi sobie z opóźnionymi etykietami;
5. formułuje SLI i SLO oraz liczy budżet błędu;
6. ustawia progi alertów, które nie generują fałszywych alarmów.

## 2. Trzy sygnały obserwowalności

| Sygnał | Odpowiada na pytanie | Koszt | Typowe użycie |
|---|---|---|---|
| **Logi** | co dokładnie się stało w tym jednym przypadku | wysoki (objętość) | diagnoza po fakcie |
| **Metryki** | jak system zachowuje się w czasie | niski (agregacja) | alerty, dashboardy, trendy |
| **Ślady** | gdzie w łańcuchu wywołań poszedł czas | średni | wąskie gardła, zależności |

Nie są zamienne. Metryka mówi „udział błędów wzrósł do 4%", log mówi „to żądanie zawiodło, bo kolumna była pusta", ślad mówi „80% czasu zajęło pobranie cech, nie predykcja".

Standardem instrumentacji jest dziś **OpenTelemetry**: jeden zestaw bibliotek generujący wszystkie trzy sygnały, niezależny od tego, gdzie je później wysyłamy. To ważne w praktyce, bo pozwala zmienić dostawcę monitoringu bez zmiany kodu aplikacji.

### Identyfikator żądania

Każde żądanie dostaje identyfikator, który:

- wraca w odpowiedzi do konsumenta,
- pojawia się w każdym wpisie logu związanym z tym żądaniem,
- łączy ze sobą ślady z różnych usług.

Bez niego diagnoza incydentu polega na zgadywaniu, które wpisy dotyczą tego samego zdarzenia.

## 3. Cztery warstwy metryk

W systemie ML nie wystarczy monitorować usługi. Trzeba obserwować cztery warstwy, bo awaria każdej z nich wygląda inaczej.

| Warstwa | Przykładowe metryki | Co wykrywa |
|---|---|---|
| **System** | opóźnienie p50/p95/p99, udział błędów, przepustowość, zużycie zasobów | awarie techniczne, przeciążenie |
| **Dane wejściowe** | udział braków, udział wartości spoza zakresu, średnia i rozrzut cech, nowe kategorie | zmianę po stronie źródła danych |
| **Predykcje** | rozkład klas, udział predykcji o niskiej pewności, udział wartości skrajnych | zmianę zachowania modelu |
| **Jakość i wartość** | accuracy, F1, koszt błędu, wskaźnik biznesowy | rzeczywistą utratę użyteczności |

Kolejność ma znaczenie diagnostyczne. Warstwa systemowa reaguje w sekundach, danych — w minutach, predykcji — w godzinach, jakości — dopiero gdy pojawią się etykiety. **Im niżej w tabeli, tym późniejszy sygnał, ale tym bliższy prawdzie.**

## 4. Opóźnione etykiety

Prawdziwa jakość modelu jest znana dopiero wtedy, gdy pojawi się etykieta. W wielu problemach oznacza to opóźnienie liczone w dniach albo miesiącach: rezygnacja klienta, spłata kredytu, nawrót choroby.

Konsekwencje:

- **metryka jakości zawsze opisuje przeszłość** — dziś wiemy, jak model radził sobie tydzień temu;
- **w oknie bez etykiet trzeba monitorować sygnały pośrednie**: rozkład wejścia, rozkład predykcji, pewność modelu;
- **etykiety bywają obciążone** — jeżeli model odrzuca wnioski, nie poznamy wyniku tych odrzuconych.

Do metod szacowania jakości bez etykiet wrócimy na zajęciach 12. Tutaj wystarczy zasada: **nie czekaj z monitoringiem na etykiety**, bo do tego czasu incydent zdąży się skończyć.

## 5. SLI, SLO i budżet błędu

- **SLI** (wskaźnik poziomu usługi) — mierzalna wielkość opisująca jakość obsługi, np. udział żądań obsłużonych poprawnie poniżej 50 ms.
- **SLO** (cel poziomu usługi) — wartość docelowa SLI, np. 99% w oknie 30 dni.
- **Budżet błędu** — dopuszczalna różnica: przy SLO 99% wolno „zepsuć" 1% żądań.

Budżet błędu jest narzędziem decyzyjnym, nie sprawozdawczym. Dopóki budżet jest niewyczerpany, można wdrażać zmiany. Gdy się wyczerpie, priorytetem staje się stabilność. To zamienia dyskusję „czy wdrażamy w piątek" w pytanie o liczbę.

Dobry SLI jest liczony **z perspektywy konsumenta**, a nie serwera. „Usługa działała" to nie to samo co „użytkownik dostał odpowiedź na czas".

## 6. Alerty, które da się utrzymać

Alert ma sens tylko wtedy, gdy **wymaga działania człowieka**. Wszystko inne należy do dashboardu albo raportu.

Typowe błędy:

| Błąd | Skutek | Naprawa |
|---|---|---|
| Próg dopasowany do najlepszego dnia | alarm przy każdej normalnej fluktuacji | próg z zapasem, oparty na rozkładzie |
| Okno zbyt krótkie | pojedynczy wyskok budzi dyżurnego | wymaganie utrzymania stanu przez N minut |
| Alert bez działania | zespół uczy się ignorować alarmy | usunąć albo powiązać z procedurą |
| Alert na przyczynę zamiast na skutek | dziesięć alarmów o jednym incydencie | alarmować na objawie widocznym dla użytkownika |

Miarą zdrowia systemu alertów jest **udział alarmów, które doprowadziły do działania**. Jeżeli spada poniżej połowy, alerty przestają pełnić swoją funkcję.

## 7. Prywatność w logach

Log usługi predykcyjnej jest najczęstszym miejscem niezamierzonego wycieku danych. Zasady:

- **logujemy metadane, nie treść**: liczbę rekordów, czas przetwarzania, wersję modelu, kod odpowiedzi;
- wartości cech zapisujemy **w postaci zagregowanej** albo na **próbce**, świadomie i z ustaloną retencją;
- pola identyfikujące osobę (adres e-mail, numer dokumentu, adres IP) nie trafiają do logu bez wyraźnej potrzeby, a jeśli trafiają — są maskowane;
- retencja jest krótsza niż domyślna: log diagnostyczny rzadko jest potrzebny dłużej niż 30 dni;
- monitoring rozkładu cech da się prowadzić na **statystykach**, bez przechowywania surowych rekordów.

## 8. Skąd monitoring bierze liczby

Dotąd liczyliśmy metryki **po fakcie**, przetwarzając plik logów. W produkcji działa to odwrotnie: usługa **wystawia** swój stan pod adresem `/metrics`, a system monitorujący sam po niego przychodzi w regularnych odstępach. Ten model nazywa się *pull*.

Trzy konsekwencje, które warto rozumieć:

- usługa nie musi wiedzieć, kto ją obserwuje, ani co się dzieje, gdy monitoring przestanie działać;
- metryki są **agregatami w pamięci procesu**, a nie zapisem każdego zdarzenia — dlatego są tanie i nie rosną wraz z ruchem;
- restart procesu zeruje liczniki, więc pytania zadaje się o **przyrost** (`rate`), nie o wartość bezwzględną.

Trzy typy metryk wystarczają na początek:

| Typ | Do czego | Przykład |
|---|---|---|
| `Counter` | wartości, które tylko rosną | liczba predykcji, liczba odrzuconych żądań |
| `Histogram` | rozkład wartości w koszykach | czas obsługi, pewność predykcji |
| `Gauge` | wartość, która rośnie i maleje | żądania w toku, wersja modelu |

Histogram jest tu ważniejszy, niż się wydaje: pozwala policzyć percentyl **po stronie systemu monitorującego**, bez przechowywania pojedynczych pomiarów. Średnia z opóźnień nie mówi nic; `histogram_quantile(0.95, ...)` mówi wszystko.

## 9. Stos obserwowalności

Trzy składniki, każdy odpowiadający na inne pytanie:

| Składnik | Pytanie |
|---|---|
| **Prometheus** | jak metryki zmieniały się w czasie? |
| **Grafana** | jak to wygląda i kiedy przekroczyliśmy próg? |
| **Jaeger** | gdzie dokładnie poszło czas w tym jednym wolnym żądaniu? |

Całość uruchamiamy jednym plikiem `compose.yaml`. Dwie decyzje konfiguracyjne są istotne:

- w `prometheus.yml` podajemy **adres usługi**, bo to Prometheus po nią przychodzi — nie odwrotnie;
- hasło do Grafany pochodzi ze zmiennej środowiskowej i **nie ma wartości domyślnej**. Domyślne hasło administratora zapisane w pliku wersjonowanym w repozytorium to jeden z częstszych sposobów wystawienia panelu na świat.

Zapytanie, które warto zapamiętać:

```promql
sum by (klasa) (rate(predictions_total[30m]))
```

Nagła zmiana proporcji klas jest sygnałem dryfu widocznym **bez znajomości prawdziwych etykiet** — a więc dostępnym od razu, a nie po tygodniach oczekiwania. Do tego wracamy na zajęciach 12.

## 10. Ćwiczenie praktyczne

### Cel

Zbudowanie kompletnej warstwy obserwowalności dla wdrożonego modelu: instrumentacja śladami, metryki czterech warstw, SLI/SLO z budżetem błędu, reguły alertów, **usługa eksportująca metryki** oraz konfiguracja stosu monitorującego.

Notebook zawiera przygotowany, syntetyczny strumień logów z doby pracy usługi — trzy okresy: normalny, incydent techniczny i zmiana rozkładu danych wejściowych. Druga część uruchamia prawdziwą usługę z `prometheus-client` i odczytuje jej `/metrics` tak, jak zrobiłby to Prometheus.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_11.ipynb`.

Uruchomienie stosu monitorującego jest w notebooku **wyłączone flagą** `URUCHOM_STOS`, bo pobiera kilkaset megabajtów obrazów. Włącz je, gdy masz na to czas i łącze.

### Punkty kontrolne

1. **Wzrost błędów.** Który alert zadziałał, w którym oknie i ile czasu minęło od początku incydentu do jego wykrycia?
2. **Zbyt czuły próg.** Porównaj dwa progi tej samej reguły. Ile fałszywych alarmów generuje wersja czuła i jak wpłynie to na zespół?
3. **Dane wrażliwe.** Znajdź w logach pola, których nie powinno tam być. Jak zmieniłbyś logowanie, nie tracąc możliwości diagnozy?
4. **Odczyt `/metrics`.** Które z wystawionych metryk odpowiadają poszczególnym warstwom? Której warstwy brakuje i dlaczego jest najtrudniejsza do zmierzenia?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_11/
    ├── logs/requests.jsonl
    ├── usluga/{app.py,model.joblib}
    ├── stos/
    │   ├── compose.yaml
    │   ├── prometheus.yml
    │   ├── zapytania.md
    │   └── grafana/datasources.yaml
    └── reports/
        ├── metrics_by_window.csv
        ├── metrics_exposition.txt
        ├── slo_report.json
        ├── alerts.json
        └── monitoring_report.md
```

### Co wymaga sprawdzenia przed zajęciami

- port, na którym uruchamiana jest usługa, jest dostępny z kontenera (`host.docker.internal`) i nie blokuje go zapora;
- obrazy `prom/prometheus`, `grafana/grafana` i `jaegertracing/all-in-one` zostały pobrane przed zajęciami — pobieranie na miejscu zajmie cały slot.

## 11. Zadanie projektowe (po zajęciach)

1. Zinstrumentuj swoją usługę albo zadanie wsadowe: identyfikator żądania, log strukturalny, co najmniej jeden ślad.
2. Wystaw endpoint `/metrics` z metrykami na **czterech warstwach** — co najmniej po jednej z każdej.
3. Użyj `Histogram` do opóźnienia i policz p95 zapytaniem, a nie w kodzie usługi.
4. Uruchom Prometheusa zbierającego te metryki i pokaż cel w stanie `UP`.
5. Opisz, kiedy w twoim problemie pojawiają się etykiety i co monitorujesz w okresie ich braku.
6. Sformułuj jedno **SLI i SLO** oraz policz budżet błędu.
7. Ustaw co najmniej dwie reguły alertów wraz z uzasadnieniem progów i okien.
8. Wygeneruj raport monitoringu jako artefakt.
9. Sprawdź swoje logi pod kątem danych wrażliwych i opisz przyjętą retencję.
10. Upewnij się, że w repozytorium nie ma żadnego domyślnego hasła do narzędzi monitorujących.

**Kryterium ukończenia:** zasymulowany wzrost udziału błędów powoduje zadziałanie alertu, a raport wskazuje okno, w którym to nastąpiło.

## 12. Literatura

1. OpenTelemetry, **dokumentacja**:
   <https://opentelemetry.io/docs/>
2. Prometheus, **client library dla Pythona**:
   <https://prometheus.github.io/client_python/>
3. Prometheus, **typy metryk i język zapytań**:
   <https://prometheus.io/docs/concepts/metric_types/>
4. Google SRE Book, **Service Level Objectives**:
   <https://sre.google/sre-book/service-level-objectives/>
5. Google SRE Workbook, **Alerting on SLOs**:
   <https://sre.google/workbook/alerting-on-slos/>
6. Evidently, **monitoring systemów ML**:
   <https://docs.evidentlyai.com/>
7. C. Huyen, **Designing Machine Learning Systems**, rozdział o monitoringu i obserwowalności.
