# Road Map Inference Evaluator

To launch the script you have to use the following command :

```shell
C:/.../evaluator> python3 evaluator.py -f "result file path" -t "truth file path" -m "intersection matching threshold"
```

Please acquaint the 2 mandatory options as follow :

-f : your result file in geojson which contains the segments (geometry = LineString) and the intersections (geometry = Point)

-t : your ground truth file in geojson which contains the segments (geometry = LineString) and the intersections (geometry = Point)

Your can also optionally mention an intersection matching threshold by using -m. Beyond this value an groundtruth intersection will not be match with a computed intersection.