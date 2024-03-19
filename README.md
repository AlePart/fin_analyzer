# Fin Analyzer

Fin Analyzer è un programma che consente di analizzare un portafoglio utilizzando dati di Yahoo Finance. Il programma genera una matrice di correlazione, una grafico a torta di allocazione e la performance del portafoglio.

## Requisiti

- Python 3.x
- Libreria pandas
- Libreria matplotlib

## Installazione

1. Clona il repository:
    
    ```bash
    git clone https://github.com/AlePart/fin_analyzer.git
    ```

2. Installa le librerie necessarie:

    ```bash
    pip install -r requirements.txt
    ```

## Utilizzo

1. Modifica il file `operations.json` con i tuoi dati di acquisto. Il file deve avere la seguente struttura:
    
        ```json
        {
            "ticker": "ENWD.MI",
            "adj_close": true,
            "quantity": 21,
            "price": 6.9138,
            "date": "2023-12-04"
        },
        {
            "ticker": "XXSC.MI",
            "adj_close": true,
            "quantity": 6,
            "price": 56.0,
            "date": "2024-01-15"
        },
        {
            "ticker": "ENWD.MI",
            "adj_close": true,
            "quantity": 50,
            "price": 6.74,
            "date": "2023-10-16"
        },
        {
            "ticker": "LCAS.MI",
            "adj_close": true,
            "quantity": 10,
            "price": 10.57,
            "date": "2021-08-27"
        },
        {
            "ticker": "GOLD.AS",
            "adj_close": false,
            "quantity": 5,
            "date": "2023-10-30"
        }
    ```
specifica se desideri per il tuo ticker il prezzo di chiusura o il prezzo di chiusura aggiustato (nel caso di dividendi o altre operazioni che influenzano il prezzo di chiusura).

2. Esegui il programma:

    ```bash
    python fin_analyzer.py
    ```

## TODO
- [ ] Controllo file operations.json
- [ ] Aggiungere la possibilità di utilizzare file json con nomi diversi
- [ ] Aggiungere la possibilità di utilizzare piu file json
- [ ] Aggiungere una riepilogo delle operazioni con relativi gain/loss
- [ ] Aggiungere la possibilità di vendere asset e calcolare il gain/loss
- [ ] Aggiungere la possibilità di inserire liquidità
- [ ] Aggiungere la possibilità di inserire conti deposito
- [ ] Aggiungere la possibilita di inserire obbligazioni
- [ ] Calcolo delle tasse
- [ ] Aggiungere Euribor e indici
- [ ] Aggiungere la possibilità esportare grafici




