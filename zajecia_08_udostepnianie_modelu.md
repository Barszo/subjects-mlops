# Zajęcia 8. Udostępnianie modelu: predykcja wsadowa i usługa

## Informacje podstawowe

- **Przedmiot:** Techniki MLOps
- **Czas:** 90 minut
- **Charakter zajęć:** wprowadzenie teoretyczne i ćwiczenie prowadzone
- **Tryb pracy:** indywidualny
- **Wymagania wstępne:** ukończone zajęcia 7, wersjonowany model z sygnaturą we własnym projekcie
- **Środowisko:** notebook `gotowe_notebooki/zajecia_08.ipynb`, usługa uruchamiana lokalnie na `127.0.0.1`
- **Rezultat:** usługa predykcyjna z jawnym kontraktem, jej test, wariant wsadowy i pomiar opóźnienia

---

## 1. Cele zajęć

Po zakończeniu zajęć student:

1. dobiera sposób udostępnienia modelu do charakteru problemu;
2. definiuje jawny, wersjonowany kontrakt wejścia i wyjścia;
3. odróżnia zgodność wsteczną od zmiany łamiącej kontrakt;
4. mierzy opóźnienie w percentylach i rozumie różnicę wobec średniej;
5. projektuje bezpieczne logowanie z identyfikatorem żądania;
6. buduje niezawodne zadanie wsadowe z raportem wykonania.

## 2. Trzy sposoby udostępnienia modelu

| Sposób | Kiedy | Typowe wymagania | Ryzyko |
|---|---|---|---|
| **Wsadowy** | predykcja dla wielu rekordów naraz, wynik potrzebny „na jutro” | harmonogram, idempotencja, raport wykonania | nieaktualne predykcje |
| **Request-response** | predykcja na żądanie użytkownika lub aplikacji | opóźnienie, dostępność, skalowanie | koszt utrzymania usługi |
| **Strumieniowy** | reakcja na zdarzenia w czasie zbliżonym do rzeczywistego | kolejka, przetwarzanie stanowe | najwyższa złożoność operacyjna |

Domyślnym wyborem powinien być **tryb wsadowy**. Jest najtańszy, najprostszy w utrzymaniu i najłatwiejszy do odtworzenia. Usługę online wprowadza się wtedy, gdy istnieje wymaganie, którego tryb wsadowy nie spełnia — na przykład predykcja musi powstać w trakcie interakcji z użytkownikiem.

Pytania rozstrzygające:

- Jak szybko wynik musi być dostępny od momentu pojawienia się danych?
- Czy zbiór obiektów do oceny jest znany z wyprzedzeniem?
- Ile predykcji dziennie i jaki jest ich koszt jednostkowy?
- Co się dzieje, gdy usługa jest niedostępna przez godzinę?

## 3. Kontrakt usługi

Kontrakt to jawna umowa między modelem a jego konsumentami. Obejmuje strukturę żądania, strukturę odpowiedzi, kody błędów i wersję.

Zasady:

- **Nazwy w API są niezależne od nazw kolumn w modelu.** Kolumna `petal length (cm)` nie powinna wyciekać do interfejsu publicznego. Mapowanie należy do warstwy usługi.
- **Walidacja następuje na brzegu.** Żądanie niezgodne z kontraktem jest odrzucane z kodem 422 i czytelnym opisem, zanim dotknie modelu.
- **Odpowiedź niesie kontekst.** Poza predykcją: wersja modelu, wersja kontraktu i identyfikator żądania.
- **Kontrakt jest wersjonowany w ścieżce**, na przykład `/v1/predict`.

### Zgodność wsteczna

| Zmiana | Zgodna wstecz? |
|---|---|
| dodanie **opcjonalnego** pola żądania | tak |
| dodanie pola odpowiedzi | zwykle tak |
| usunięcie pola odpowiedzi | **nie** |
| zmiana typu pola | **nie** |
| zaostrzenie walidacji istniejącego pola | **nie** |
| zmiana znaczenia wartości przy tej samej nazwie | **nie**, i jest to najgorszy wariant, bo niewidoczny |

Zmiana łamiąca kontrakt wymaga nowej wersji ścieżki i okresu, w którym działają obie. Sam fakt, że model jest lepszy, nie uprawnia do zepsucia integracji u konsumentów.

## 4. Opóźnienie, przepustowość i koszt

Średnie opóźnienie jest metryką mylącą. Jeżeli 95% żądań trwa 20 ms, a 5% trwa sekundę, średnia wynosi około 70 ms i nie opisuje doświadczenia nikogo.

Mierzymy **percentyle**: p50 (mediana), p95 i p99. To p99 decyduje o tym, ilu użytkowników uzna usługę za wolną.

Praktyczne obserwacje:

- **Predykcja zbiorcza jest wielokrotnie tańsza na rekord** niż seria pojedynczych żądań — narzut sieci i serializacji jest stały.
- **Pierwsze żądanie po starcie jest wolne** (wczytanie modelu, inicjalizacja bibliotek). Dlatego istnieje osobny stan „gotowy do ruchu”.
- **Koszt liczymy na tysiąc predykcji**, nie na godzinę pracy usługi. Dopiero wtedy da się porównać wariant wsadowy z online.

## 5. Obsługa błędów i stan usługi

Rozróżniamy dwa różne pytania:

- **liveness** (`/health`) — czy proces żyje; negatywna odpowiedź oznacza restart;
- **readiness** (`/ready`) — czy usługa może przyjmować ruch; model może być jeszcze wczytywany.

Mieszanie tych dwóch stanów jest częstym błędem: usługa, która nie zdążyła wczytać modelu, dostaje ruch i zwraca błędy, albo jest bez końca restartowana.

Kody odpowiedzi:

| Sytuacja | Kod |
|---|---|
| poprawne żądanie | 200 |
| żądanie niezgodne z kontraktem | 422 |
| zbyt wiele rekordów w jednym żądaniu | 422 |
| model niegotowy | 503 |
| błąd wewnętrzny | 500, bez szczegółów w treści odpowiedzi |

## 6. Bezpieczne logowanie

Log usługi predykcyjnej jest jednocześnie najcenniejszym źródłem obserwowalności (zajęcia 11) i najczęstszym miejscem wycieku danych.

Zasady:

- każde żądanie ma **identyfikator** przekazywany do odpowiedzi i zapisywany w logu;
- logujemy **metadane**, nie treść: liczbę rekordów, czas przetwarzania, wersję modelu, kod odpowiedzi;
- wartości cech logujemy wyłącznie w postaci zagregowanej albo na próbce, świadomie i z ustaloną retencją;
- log jest strukturalny (JSON), bo ma być czytany przez maszynę.

## 7. Niezawodne zadanie wsadowe

Zadanie wsadowe też jest sposobem udostępnienia modelu i podlega tym samym wymaganiom co usługa:

- **idempotencja** — powtórne uruchomienie dla tego samego wejścia daje ten sam wynik i nie duplikuje danych;
- **raport wykonania** — liczba rekordów, liczba odrzuconych, czas, wersja modelu, wersja danych;
- **obsługa rekordów niepoprawnych** — odrzucamy pojedyncze rekordy i raportujemy, zamiast przerywać całość;
- **ten sam kod scoringowy** co w usłudze — inaczej wracamy do problemu z zajęć 4.

## 8. Ćwiczenie praktyczne

### Cel

Zbudowanie usługi predykcyjnej z jawnym kontraktem, testu kontraktu, wariantu wsadowego oraz pomiaru opóźnienia.

Pracujesz z notebookiem `gotowe_notebooki/zajecia_08.ipynb`. Usługa uruchamiana jest lokalnie jako osobny proces i zatrzymywana na końcu notebooka.

### Punkty kontrolne

1. **Żądanie niezgodne z kontraktem.** Wyślij żądanie z brakującym polem, błędnym typem i wartością spoza zakresu. Jaki kod i jaki opis błędu otrzymujesz?
2. **Złamanie kontraktu odpowiedzi.** Usuń pole z odpowiedzi usługi. Który test to wykrył i co zobaczyłby konsument, gdyby testu nie było?
3. **Opóźnienie.** Porównaj p50, p95 i p99 dla żądań pojedynczych i zbiorczych. Ile razy tańszy jest rekord w żądaniu zbiorczym?

### Oczekiwana struktura artefaktów

```text
artifacts/
└── zajecia_08/
    ├── models/model.joblib
    ├── src/{app.py,scoring.py,batch.py}
    └── reports/
        ├── latency.json
        ├── batch_report.json
        └── predictions.csv
```

## 9. Zadanie projektowe (po zajęciach)

1. Udostępnij swój model jako usługę HTTP **albo** jako niezawodne zadanie wsadowe — wybór uzasadnij charakterem problemu.
2. Zdefiniuj jawny, wersjonowany kontrakt wejścia i wyjścia; nazwy w API mają być niezależne od nazw kolumn modelu.
3. Napisz **test kontraktu** uruchamiany razem z resztą zestawu z zajęć 6.
4. Dodaj sprawdzenie stanu (`/health` i `/ready` albo ich odpowiednik w zadaniu wsadowym).
5. Wprowadź logowanie strukturalne z identyfikatorem żądania, bez danych wrażliwych.
6. Zmierz opóźnienie w percentylach albo czas przetworzenia paczki i zapisz wynik jako artefakt.
7. Opisz w dokumentacji, co się stanie przy niedostępności usługi przez godzinę.

**Kryterium ukończenia:** inna osoba potrafi wywołać twój model, znając wyłącznie opis kontraktu, bez czytania kodu.

## 10. Literatura

1. FastAPI, **dokumentacja**:
   <https://fastapi.tiangolo.com/>
2. Pydantic, **walidacja modeli danych**:
   <https://docs.pydantic.dev/>
3. Google SRE Book, **Monitoring Distributed Systems** — percentyle i SLI:
   <https://sre.google/sre-book/monitoring-distributed-systems/>
4. Microsoft, **API versioning and backward compatibility guidance**:
   <https://learn.microsoft.com/azure/architecture/best-practices/api-design>
5. MLflow, **Deploy models — batch i online**:
   <https://mlflow.org/docs/latest/deployment/>
