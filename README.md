# tdsp
Steps to find shortest path in the hierarchical road networks with time dependent travel times

Description about the variation in traffic on road networks, and the model, in general, is provided in the [hierarchical_tdsp.pdf](hierarchical_tdsp.pdf) file.

## Steps to implement 'Time dependent shortest path' algorithm in Python:
1) To get the network database from OpenStreetMap (OSM) on your system, first install pgRouting. Instructions on how to install pgRouting is given on this link: https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS22UbuntuPGSQL95Apt

2) After that, create a role "user", then create a database for this user, and then import the OSM data of the city you want to work with. In this project, we consider the road network of Buffalo, US. Therefore, we'll name this database 'buffalo_routing'. Instructions on how to create the role and the database, and how to import the data, is given in [pgrouting_prepare_data.md](pgrouting_prepare_data.md)
