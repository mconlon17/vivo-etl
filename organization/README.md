# Making Organization Data

Two examples are provided.  One uses data coming from [ROR](https://ror.org).  ROR
maintains data on more than 91,000 research organizations around the world.  The data is 
openly available.  The second example uses data from a TSV file that you create.  A 
sample file, `organizations.tsv` includes fictional data for a small institution.

## Source is ROR

To get ROR data, you will need the RORO ID of the organization you wish to get.  Use
the script `ror.sh`, which has three parameters:

1. The ror id of the organization whose data is to be fetched and represented.
1. the file name (no extension) of the resulting data file
1. The word `new` to represent the organization using the new VIVO ontologies, or `vivo`
to represent using the existing VIVO ontologies.

For example:

    ./ror.sh 02y3ad647 uf new
    
will fetch data for ROR ID 02y3ad647 (the University of Florida) and return a file named
`uf.ttl` containing assertions abut UF made using the new VIVO ontologies.

## Source is Local

For local org, data, make a TSV file with data as in the example `organization.tsv`.  
One row per organization, with data for each organization as shown.

Use the provide script `local-org` to make data.  local-org takes two arguments. The
first is the file name of your TSV file.  The second is either `new` or `vivo` to make 
data for the new VIVO ontologies or the existing VIVO ontologies.  The default is `new`.

For example:

    ./local-org.sh organizations new
    
will process the supplied sample file `organizations.tsv` and return a data file called 
`organizaations.ttl` represented using the new VIVO ontologies.

