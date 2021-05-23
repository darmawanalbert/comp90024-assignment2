# Cities_top50_simplified
* Geojson object containing coordinates of top 50 cities
```
{
  geometry: {"type": str, "coordinates": [long, lat]}
  properties: {"UCL_CODE_2016": str, "UCL_NAME_2016": str, "STATE_NAME_2016": str}
}
```
**GET /cities**
----
  Returns all cities in the system.
* **URL Params**
  None
* **Data Params**
  None
* **Headers**
  Content-Type: application/json
* **Success Response:**
* **Code:** 200
  **Content:**
```
{
  features: [
     {<city>},
     {<city>},
     {<city>}
   ],
  type: "FeatureCollection"
}
```
# LDA scores
* LDA scores object (grouped by city) during a period of time.
```
{
  id: str,
  key: [place (str, lowercase), YYYY (int), M(M) (int), D(D) (int)],
  value: {lda_keywords: {keyword1: freq (str), 
                        keyword2: freq (str)}
          topic_score: {business: str, 
                        education: str, 
                        entertainment: str, 
                        places: str, 
                        politics: str, 
                        sport: str}
          tweets_count: str
  },
}

```
**GET /lda-scores**
----
  Returns LDA score for all cities during a period of time.
* **URL Params**  
  *Optional:* `start_date=YYYY-MM-DD` if left blank, uses today's date as start_date
  *Optional:* `end_date=YYYY-MM-DD` if left blank, retrieves one-day data
* **Data Params** 
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:** 
* **Code:** 200  
  **Content:**  
```
{
  products: [
           {<lda_score_object>},
           {<lda_score_object>},
           {<lda_score_object>}
         ]
}
```

# Chart Data
* Chart Data object (grouped by analysis metric: age, income, unemployment) during a period of time.
```
{
  id: str,
  value: {business: { c: y-intercept (float), 
                      m: gradient (float),
                      p_val: (float),
                      r_squared: (float),
                      std_err: (float),
                      x: [x1, x2, ..., xn] (float),
                      y: [y1, y2, ..., yn] (float)},
          education: { same as above },
          entertainment: { same as above },
          places: { same as above },
          politics: { same as above },
          sport: { same as above },
  },
}
```
**GET /charts**
----
  Returns chart data for all cities during a period of time.
* **URL Params**  
  *Optional:* `start_month=YYYY-MM` if left blank, uses today's date as start_date
  *Optional:* `end_month=YYYY-MM` if left blank, retrieves one-month data
* **Data Params** 
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:** 
* **Code:** 200  
  **Content:**  
```
{
  products: [
           {<chart_data_object>},
           {<chart_data_object>},
           {<chart_data_object>}
         ]
}
```