# TDSP
Steps to find shortest path in the hierarchical road networks with time dependent travel times

Description about the variation in traffic on road networks, and the model, in general, is provided in the [hierarchical_tdsp.pdf](hierarchical_tdsp.pdf) file.

## Steps to implement 'Time dependent shortest path' algorithm in Python:
1) To get the network database from OpenStreetMap (OSM) on your system, first install pgRouting. Instructions on how to install pgRouting is given on this link: https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS22UbuntuPGSQL95Apt

2) After that, create a role "user", then create a database for this user, and then import the OSM data of the city you want to work with. In this project, we consider the road network of Buffalo, US. Therefore, we'll name this database 'buffalo_routing'. Instructions on how to create the role and the database, and how to import the data, is given in [pgrouting_prepare_data.md](pgrouting_prepare_data.md)

3) Log in to the buffalo_routing database:
```
psql -U user buffalo_routing
```

4) Create a table 'graph' in the database and add data into it:
```
create table graph AS select gid as edge_id, class_id, source, target, cost_s as cost, y1 as source_lat, x1 as source_lon, y2 as target_lat, x2 as target_lon from ways where one_way >= 0;
insert into graph select gid, class_id, target, source, reverse_cost_s, y2, x2, y1, x1 from ways where one_way < 0;
insert into graph select gid, class_id, target, source, reverse_cost_s, y2, x2, y1, x1 from ways where one_way in (0,2);
```

5) Create a table 'macro_nodes' in the database and then, exit:
```
create table macro_nodes as select * from (select source as id from ways where class_id in (101,103,102,104,105,106,107,108,124,109,125) union select target as id from ways where class_id in (101,103,102,104,105,106,107,108,124,109,125)) x;
\q
```

6) In this step, we'll perform preprocessing. Download the file [preprocess_nodes.py](preprocess_nodes.py) and run it on terminal:
```
python preprocess_nodes.py
```

This will create two tables in the 'buffalo_routing' database: 'start_macro_nodes' and 'end_macro_nodes'. These are the tables which store preprocessed data.

7) Now, download the file [tdsp_matrix.py](tdsp_matrix.py) and run it on terminal to get a matrix of arrival time:
```
python tdsp_matrix.py
```

8) Once you've run this file, it will ask for 3 inputs: i. list of source nodes, ii. list of target nodes, and iii. start time. Input these values, as given in example below:
    ```
    sources = [12, 524, 1351, 63, 435, 345, 366, 757, 673, 2]
    targets = [13, 525, 1352, 64, 436, 346, 367, 758, 674, 1]
    start hour = 36300
    ```

9) You are done! It will generate a dictionary of arrival times at the destination nodes. Once you enter the values given in the example in step 8, it will generate the following result:
```
Total time taken is 3.305581 seconds
{(435, 674, 36300): 38194.620737937876, (366, 674, 36300): 37979.87655211168, (435, 436, 36300): 37241.40274344803, (345, 346, 36300): 38074.582969419214, (757, 367, 36300): 37298.321417861414, (1351, 525, 36300): 37367.16941518482, (435, 758, 36300): 37939.31569208465, (63, 1, 36300): 37211.95920284815, (435, 1352, 36300): 37976.80189852339, (757, 346, 36300): 37220.08686717837, (63, 367, 36300): 37156.531174294476, (1351, 436, 36300): 37543.576899162545, (366, 1, 36300): 38317.80604349819, (1351, 346, 36300): 37192.70757823416, (366, 436, 36300): 38190.1762978334, (12, 64, 36300): 37671.158270887936, (12, 367, 36300): 37148.28125952087, (435, 64, 36300): 38095.90895381709, (757, 674, 36300): 37988.293628683496, (524, 64, 36300): 36967.139094732076, (12, 13, 36300): 37668.41383891707, (345, 1352, 36300): 37905.74627822158, (366, 525, 36300): 37302.479450468636, (366, 758, 36300): 37968.85469998358, (366, 346, 36300): 38094.34231132629, (673, 13, 36300): 38116.955747712855, (1351, 1, 36300): 37324.24279724321, (12, 758, 36300): 37131.86139105367, (12, 346, 36300): 37342.18303080081, (757, 1352, 36300): 37657.397312624395, (524, 674, 36300): 37639.39292120148, (12, 1352, 36300): 37645.60827039084, (63, 13, 36300): 37676.40048371355, (366, 13, 36300): 37281.34522389596, (2, 13, 36300): 36847.72360476587, (366, 1352, 36300): 37925.75227440191, (673, 346, 36300): 37574.150876634005, (673, 758, 36300): 37679.80294763812, (345, 367, 36300): 37379.72094522595, (63, 674, 36300): 38050.620673707956, (345, 1, 36300): 38298.308752316814, (673, 436, 36300): 36948.78724108629, (524, 346, 36300): 37796.72117081359, (757, 13, 36300): 37766.589158427305, (757, 64, 36300): 37769.33359039817, (1351, 13, 36300): 36940.90139211846, (673, 64, 36300): 38119.70017968372, (1351, 367, 36300): 37444.59319094458, (2, 1, 36300): 37747.803587023765, (435, 525, 36300): 38259.069076829954, (366, 64, 36300): 37284.08965586683, (345, 13, 36300): 37260.30258393321, (345, 525, 36300): 37281.513190918005, (435, 13, 36300): 38093.16452184622, (2, 346, 36300): 37516.67881332639, (673, 1352, 36300): 38000.69380990797, (673, 525, 36300): 38282.52396213991, (63, 1352, 36300): 37653.57428083952, (63, 436, 36300): 37050.35888203709, (12, 436, 36300): 37042.042453703536, (673, 674, 36300): 38323.442755722484, (524, 758, 36300): 37701.44351779128, (2, 1352, 36300): 37269.274085436155, (63, 758, 36300): 37140.12067928094, (757, 758, 36300): 37109.44147593339, (524, 436, 36300): 38183.97489379536, (2, 674, 36300): 37671.59855991996, (757, 436, 36300): 36914.78539485995, (12, 525, 36300): 37962.242483654496, (2, 367, 36300): 37130.81621325564, (63, 64, 36300): 37679.14491568442, (345, 436, 36300): 38368.30806570816, (435, 346, 36300): 37444.73638976126, (757, 1, 36300): 37080.053902538384, (524, 525, 36300): 36693.12101140267, (524, 1, 36300): 38024.131989696354, (63, 346, 36300): 37350.32225472054, (2, 64, 36300): 36850.46803673674, (63, 525, 36300): 37970.04662099421, (673, 367, 36300): 38010.94300812571, (12, 1, 36300): 37203.71561563513, (12, 674, 36300): 38042.88145080888, (524, 1352, 36300): 37624.415953168325, (1351, 64, 36300): 36943.645824089326, (345, 674, 36300): 37959.94974201272, (366, 367, 36300): 37188.42887250221, (435, 1, 36300): 37317.65813108647, (435, 367, 36300): 38354.24571629671, (345, 758, 36300): 37981.22326794757, (1351, 758, 36300): 36557.794138228084, (2, 436, 36300): 37703.091719545126, (2, 525, 36300): 37121.318850507196, (1351, 674, 36300): 37404.47013926161, (673, 1, 36300): 37239.592251021946, (1351, 1352, 36300): 36988.48917140089, (757, 525, 36300): 37945.50697586851, (345, 64, 36300): 37263.047015904085, (524, 13, 36300): 36964.3946627612, (524, 367, 36300): 38009.29264814533, (2, 758, 36300): 36849.094503731794}
```

In the result shown in step 9, the first element signifies that if a vehicle departs from node 435 at 36300 seconds (10:05AM), it will reach node 674 at 38194.620737937876 seconds (10:36:34AM), and likewise.
