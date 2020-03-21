# DZ COVID19 Data Retrieval

## About

This repository contains a small script which allows to download
data from some websites that follows the situation of the COVID-19
in Algeria at province level.

The data is obtained by calling the internal API of the website
selected. The information gathered can differ depending on the
website. Generally, they offer at least the number of cases for
each province from the provinces affected by the epidemic.

The useful data will be retained and converted into a JSON file
that can be saved or printed on the standard output.

## <span dir='rtl'>حول</span>

<div dir="rtl">
هذا المستودع يحوي برنامجا نصيا صغيرا يسمح يتنزيل بيانات من بعض المواقع التي تتبع وضع
كوفيد-19 في الجزائر على المستوى الولائي.
</div>

<div dir="rtl">
تمّ الحصول على هذه البيانات باستدعاء واجهة البرمجة التطبيقية للموقع الشبكي المختار. المعلومات الملتقطة
قد تختلف اعتمادا على الموقع الشبكي. عادة، يوفرون على الأقل عدد الحالات لكل ولاية من الولاية المتأثّرة
بالوباء.
</div>

<div dir="rtl">
يتمّ ابقاء البيانات المفيدة وتحويلها إلى ملف JSON يمكن حفظه أو طباعة محتواه في المخرج القياسي.
</div>

## Usage

```
$ python3 dz_covid19_data_retriever.py --source {COVID19Maghreb,ArcGisMaps} [--output-file OUTPUT_FILE]
```

### Examples

Get the data from [Yassir COVID-19 Maghreb](http://www.covid19-maghreb.live/)
and display it:

```
$ python3 dz_covid19_data_retriever.py --source COVID19Maghreb
```

Get the data from [ArcGisMaps COVID-19 Algeria](https://abdelghafour.maps.arcgis.com/apps/opsdashboard/index.html?fbclid=IwAR06TyO9BGI6r-V1yJ8JSgda-56rbO4o0rp3-l0-SmNeJJ_JD_q3Fb0mVBo#/ad57a9371f6a4bf7b1b7881be4cdb8ae)
and save it into a JSON file named ArcGisMaps_DZ.json

```
$ python3 dz_covid19_data_retriever.py --source ArcGisMaps --output-file ArcGisMaps_DZ.json
```
