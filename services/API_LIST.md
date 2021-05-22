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

# Avg Median Income
* Avg Median Income object (per city)
```
{
  UCL_CODE_2016: str
  avg_med_weekly_inc: float
}
```
**GET /median_income/all**
----
  Returns median incomes for all cities.
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
  products: [
           {<avg_median_income_object>},
           {<avg_median_income_object>},
           {<avg_median_income_object>}
         ]
}
``` 

**GET /median_income**
----
  Returns the avg median income for specified city.
* **URL Params**  
  None
* **Data Params**  
  *Required:* `id=[str]` refer to UCL_CODE_2016
* **Headers**  
  Content-Type: application/json  
  Authorization: Bearer `<OAuth Token>`
* **Success Response:**  
* **Code:** 200  
  **Content:**  `{ <product_object> }` 
* **Error Response:**  
  * **Code:** 404  
  **Content:** `{ error : "Product doesn't exist" }`  
  OR  
  * **Code:** 401  
  **Content:** `{ error : error : "You are unauthorized to make this request." }`

# Proportion age 25-34 to Total Population
* Proportion age 25-34 to Total Population object (per city)
```
{
  UCL_CODE_2016: str
  proportion_age_25_34: float
  tot_p: integer
}
```
**GET /age_25_34/all**
----
  Returns proportion of residents aged 25-34 for all cities.
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
  products: [
           {<prop_age_25_34_object>},
           {<prop_age_25_34_object>},
           {<prop_age_25_34_object>}
         ]
}
``` 

**GET /age_25_34**
----
  Returns the proportion of residents aged 25-34 for specified city.
* **URL Params**  
  None
* **Data Params**  
  *Required:* `id=[str]` refer to UCL_CODE_2016
* **Headers**  
  Content-Type: application/json  
  Authorization: Bearer `<OAuth Token>`
* **Success Response:**  
* **Code:** 200  
  **Content:**  `{ <product_object> }` 
* **Error Response:**  
  * **Code:** 404  
  **Content:** `{ error : "Product doesn't exist" }`  
  OR  
  * **Code:** 401  
  **Content:** `{ error : error : "You are unauthorized to make this request." }`

# Unemployment Rate
* Unemployment Rate (per city)
```
{
  UCL_CODE_2016: str
  unemployment_rate: float
  tot_lf: integer
}
```
**GET /unemployment_rate/all**
----
  Returns proportion of residents aged 25-34 for all cities.
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
  products: [
           {<unemployment_rate>},
           {<unemployment_rate>},
           {<unemployment_rate>}
         ]
}
``` 

**GET /unemployment_rate**
----
  Returns the proportion of residents aged 25-34 for specified city.
* **URL Params**  
  None
* **Data Params**  
  *Required:* `id=[str]` refer to UCL_CODE_2016
* **Headers**  
  Content-Type: application/json  
  Authorization: Bearer `<OAuth Token>`
* **Success Response:**  
* **Code:** 200  
  **Content:**  `{ <product_object> }` 
* **Error Response:**  
  * **Code:** 404  
  **Content:** `{ error : "Product doesn't exist" }`  
  OR  
  * **Code:** 401  
  **Content:** `{ error : error : "You are unauthorized to make this request." }`
