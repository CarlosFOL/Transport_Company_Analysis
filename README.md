# Transportation Company Analysis


<p align = "center">
<img src = "https://img.shields.io/badge/Python-3.12.3-blue?style=plastic" alt = "Python">
<img src="https://img.shields.io/github/repo-size/CarlosFOL/Transport_Company_Analysis?style=plastic">
</p>

<img src = "https://tso-assets-prd.s3.amazonaws.com/_processed_/2/4/csm_Landingpage_Hersteller_a58de32001.jpg" width = 450 height = 150>

The main goal of this analysis is to identify the key variables this **"anonymous"** transport company records about their daily trips. This project primarily focuses on cleaning a chaotic dataset containing null values, redundant information, unconstrained domains, and non-atomic values.

<p align = "center">
<img src = "img/null_data.png" width = 550 height = 350><br>
<img src = "img/nulldata_over_trips.png" width = 250 height = 150> 
</p>

The dataset exhibits significant data quality issues: 30% of all columns have null values in more than half of their entries. Every trip record contains at least some null values, with 75% of all records missing data in 20-40% of their attributes. 

## Data Cleaning 🗑️

The dataset's structure presents significant challenges for analysis. A substantial portion of the data contains null values, requiring an especially methodical approach to data cleaning. Throughout this process, I've prioritized data preservation, carefully evaluating each transformation to retain as much valuable information as possible.

1. Fill in the columns related to extra costs in a trip by using `'Missing'`values:
```py
extra_costs = ['COMBUSTIBLE', 'CINTA REFLECTIVA', 'PARACHOQUE', 
                'OBSERVACIONES', 'LAVADO', 'REVISIÓN TÉCNICA', 
                'OTROS', 'COMENTARIOS', 
                'INCIDENTES DE TRANSITO / SINIESTROS']
```
2. Fill in the `VOLQUETE` column, indicating whether it was necessary to use a tipper truck in the trip `[1, 0, 'Not Specified']`.

3. `HORAS DE ESPERA` (Waiting hours). It is the column with the most amount of null data (99.04%). It's is a derived attribute that must not be included in the logical schema of this datatset. We can calculate by the difference between `'HORA DE INICIO DEL TRANSITO'` (Transit start time) and `'HORA LLEGADA CONDUCTOR'` (Driver Arrival time). The big problem was that not all values of these columns were `date` objects. So, we had to cast them or get them by using the information of other variabes in the worst case.
    
    3.1. I was surprised that the company decided to store the status of a trip in the same column where the driver's arrival time or the start of the trip should be stored.

    3.2. There are trips whose `STATUS = EN DESTINO` (At Destination). However, there are nulls values in both `HORA LLEGADA CONDUCTOR` and `HORA DE INICIO DEL TRANSITO`<br> <p align = "center"><img src = "img/trip_status.png" width = 340 height = 200></p>
    I decided to fill the columns of `HORA LLEGADA CONDUCTOR`, `HORA DE INICIO DEL TRANSITO` with `'Unregistered'` for those trips are `FALSO FLETE` and `CANCELADO`. At this moment, I could know in which trips I could not get their waiting hours.<br>
    > [!NOTE] More information about the meaning of the variable `STATUS` in `notebooks/data_cleaning.ipynb`.

4. `FECHA DE TRANSFERENCIA` (Transfer Date). This was a variable that the company didn't handle properly. While drivers could receive multiple transfers during a single trip, the company's system only recorded the first transfer received on the trip's start date.<br> This column has a lot of null data, but we can get it by using the data of another columns (`FECHA DE INICIO`). However, his raises two important questions: First, how should we handle cases where even the start date is unavailable? Second, even after imputation, can we be confident in the format integrity and validity of this derived dat
   
    4.1. First, we check the dtypes in `FECHA DE INICIO` (Start Date) and `FECHA DE LLEGADA` (Arrival Date). I want to analyze the latter, because it's important to check if the following relationship is met: $$\text{Arrival Date} \geq \text{Start Date}$$<br><div align="center" display="flex">
    <img src = "img/dtypes_arr_start.png" width = 371>
    <img src = "img/relation_start_arr.png" width = 300>
    </div>

    4.2. Analysis revealed that 98% of trips with both valid start and end dates (where the temporal relationship between these dates was logically consistent) also contained transit start times and arrival times in the correct format.<br><p align = "center"><img src = "img/start_arr_format.png" width = 350></p>

    4.3. It was possible to estimate the arrival date for these trips that had a consistent value on the start date variable by using the duration of trips with a similar route. To accomplish this  task, I created a class in `scripts/trip_management/date_types/datetimes/trip_duration.py`.


    4.4. I had to deal with start and arrival dates that were strings. The following table shows the different types of pairs that I have found.<table border="1">
  <thead>
    <tr>
      <th colspan="3" style="text-align: center;">Multi-index</th>
      <th rowspan="2" style="text-align: center; vertical-align: bottom;">freq</th>
    </tr>
    <tr>
      <th style="text-align: center;">Pair</th>
      <th style="text-align: center;">Column</th>
      <th style="text-align: center;">DType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td style="text-align: left;">FECHA DE INICIO</td>
      <td style="text-align: left;">datetime.datetime</td>
      <td style="text-align: right;">59</td>
    </tr>
    <tr>
      <td style="text-align: center;">1</td>
      <td style="text-align: left;">FECHA DE LLEGADA</td>
      <td style="text-align: left;">str</td>
      <td style="text-align: right;">59</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td style="text-align: left;">FECHA DE INICIO</td>
      <td style="text-align: left;">str</td>
      <td style="text-align: right;">115</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td style="text-align: left;">FECHA DE LLEGADA</td>
      <td style="text-align: left;">str</td>
      <td style="text-align: right;">115</td>
    </tr>
  </tbody>
</table>
For the second pair, we got inconsistent values instead of dates in string format:
<p align = "center"><img src = "img/pair2_mc_values.png" width = 400></p>
4.5. It was also found dates that were floats. This behavior could be caused by NaN values, because NumPy handles them that way.
<table border="1">
  <thead>
    <tr>
      <th colspan="3" style="text-align: center;">Multi-index</th>
      <th rowspan="2" style="text-align: center; vertical-align: bottom;">freq</th>
    </tr>
    <tr>
      <th style="text-align: center;">Dataset</th>
      <th style="text-align: center;">Column Name</th>
      <th style="text-align: center;">Data Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td style="text-align: left;">FECHA DE INICIO</td>
      <td style="text-align: left;">datetime.datetime</td>
      <td style="text-align: right;">47</td>
    </tr>
    <tr>
      <td style="text-align: center;">1</td>
      <td style="text-align: left;">FECHA DE LLEGADA</td>
      <td style="text-align: left;">float</td>
      <td style="text-align: right;">47</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td style="text-align: left;">FECHA DE INICIO</td>
      <td style="text-align: left;">float</td>
      <td style="text-align: right;">52</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td style="text-align: left;">FECHA DE LLEGADA</td>
      <td style="text-align: left;">float</td>
      <td style="text-align: right;">52</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td style="text-align: left;">FECHA DE INICIO</td>
      <td style="text-align: left;">float</td>
      <td style="text-align: right;">1</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td style="text-align: left;">FECHA DE LLEGADA</td>
      <td style="text-align: left;">datetime.datetime</td>
      <td style="text-align: right;">1</td>
    </tr>
  </tbody>
</table>
I could only work with pair 1, where I have to proceed the same way if there are valid start dates, estimating the arrival date by using the duration of trips with similar route.

---
At this point, I was able to significantly reduce the null values in the dataset. However, simply filling missing values with 'Unregistered' is not the most optimal approach from a data integrity perspective.
When designing a proper database following conceptual and logical schema principles, we would handle this situation differently. 

For example, a well-designed system would enforce data entry constraints requiring employees to ALWAYS register both start and arrival dates, as well as start and arrival times for each trip. In such a system, null values would only be permitted in specific scenarios, such as when a trip needed to be cancelled or rescheduled.<p align = "center"><img src = "img/nulldata_updated.png" width = 500></p>
