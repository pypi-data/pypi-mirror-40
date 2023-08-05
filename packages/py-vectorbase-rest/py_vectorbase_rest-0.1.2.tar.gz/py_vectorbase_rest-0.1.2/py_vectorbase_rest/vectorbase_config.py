'''
    Copyright (C) 2018, Romain Feron
    Based on code from Steve Moss Copyright (C) 2013-2016, pyEnsemblRest
    py_vectorbase_rest is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    py_vectorbase_rest is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with py_vectorbase_rest.  If not, see <http://www.gnu.org/licenses/>.
    Configuration information for the EnsEMBL REST API
'''


# Vectorbase server URL
vectorbase_default_url = 'https://www.vectorbase.org'

vectorbase_api_table = {

    'archive_id_get': {
        'method': 'GET',
        'url': '/rest/archive/id/{{id}}',
        'doc': 'Uses the given identifier to return the archived sequence.',
        'doc_url': '/rest/documentation/info/archive_id_get',
        'content_type': 'application/json'},

    'archive_id_post': {
        'method': 'POST',
        'url': '/rest/archive/id',
        'doc': 'Retrieve the archived sequence for a set of identifiers.',
        'doc_url': '/rest/documentation/info/archive_id_post',
        'content_type': 'application/json'},

    'genetree': {
        'method': 'GET',
        'url': '/rest/genetree/id/{{id}}',
        'doc': 'Retrieves a gene tree dump for a gene tree stable identifier.',
        'doc_url': '/rest/documentation/info/genetree',
        'content_type': 'application/json'},

    'genetree_member_id': {
        'method': 'GET',
        'url': '/rest/genetree/member/id/{{id}}',
        'doc': 'Retrieves a gene tree that contains the stable identifier.',
        'doc_url': '/rest/documentation/info/genetree_member_id',
        'content_type': 'application/json'},

    'genetree_member_symbol': {
        'method': 'GET',
        'url': '/rest/genetree/member/symbol/{{species}}/{{symbol}}',
        'doc': 'Retrieves a gene tree containing the gene identified by a symbol.',
        'doc_url': '/rest/documentation/info/genetree_member_symbol',
        'content_type': 'application/json'},

    'genomic_alignment_region': {
        'method': 'GET',
        'url': '/rest/alignment/region/{{species}}/{{region}}',
        'doc': 'Retrieves genomic alignments as separate blocks based on a region and species.',
        'doc_url': '/rest/documentation/info/genomic_alignment_region',
        'content_type': 'application/json'},

    'homology_ensemblgene': {
        'method': 'GET',
        'url': '/rest/homology/id/{{id}}',
        'doc': 'Retrieves homology information (orthologs) by Ensembl gene id.',
        'doc_url': '/rest/documentation/info/homology_ensemblgene',
        'content_type': 'application/json'},

    'homology_symbol': {
        'method': 'GET',
        'url': '/rest/homology/symbol/{{species}}/{{symbol}}',
        'doc': 'Retrieves homology information (orthologs) by symbol.',
        'doc_url': '/rest/documentation/info/homology_symbol',
        'content_type': 'application/json'},

    'xref_external': {
        'method': 'GET',
        'url': '/rest/xrefs/symbol/{{species}}/{{symbol}}',
        'doc': 'Looks up an external symbol and returns all Ensembl objects linked to it. This can be a display name for a gene/transcript/translation, a synonym or an externally linked reference. If a gene''s transcript is linked to the supplied symbol the service will return both gene and transcript (it supports transient links).',
        'doc_url': '/rest/documentation/info/xref_external',
        'content_type': 'application/json'},

    'xref_id': {
        'method': 'GET',
        'url': '/rest/xrefs/id/{{id}}',
        'doc': 'Perform lookups of Ensembl Identifiers and retrieve their external references in other databases.',
        'doc_url': '/rest/documentation/info/xref_id',
        'content_type': 'application/json'},

    'xref_name': {
        'method': 'GET',
        'url': '/rest/xrefs/name/{{species}}/{{name}}',
        'doc': 'Performs a lookup based upon the primary accession or display label of an external reference and returning the information we hold about the entry.',
        'doc_url': '/rest/documentation/info/xref_name',
        'content_type': 'application/json'},

    'analysis': {
        'method': 'GET',
        'url': '/rest/info/analysis/{{species}}',
        'doc': 'List the names of analyses involved in generating Ensembl data.',
        'doc_url': '/rest/documentation/info/analysis',
        'content_type': 'application/json'},

    'assembly_info': {
        'method': 'GET',
        'url': '/rest/info/assembly/{{species}}',
        'doc': 'List the currently available assemblies for a species, along with toplevel sequences, chromosomes and cytogenetic bands.',
        'doc_url': '/rest/documentation/info/assembly_info',
        'content_type': 'application/json'},

    'assembly_stats': {
        'method': 'GET',
        'url': '/rest/info/assembly/{{species}}/{{region_name}}',
        'doc': 'Returns information about the specified toplevel sequence region for the given species.',
        'doc_url': '/rest/documentation/info/assembly_stats',
        'content_type': 'application/json'},

    'biotypes': {
        'method': 'GET',
        'url': '/rest/info/biotypes/{{species}}',
        'doc': 'List the functional classifications of gene models that Ensembl associates with a particular species. Useful for restricting the type of genes/transcripts retrieved by other endpoints.',
        'doc_url': '/rest/documentation/info/biotypes',
        'content_type': 'application/json'},

    'compara_methods': {
        'method': 'GET',
        'url': '/rest/info/compara:/methods',
        'doc': 'List all compara analyses available (an analysis defines the type of comparative data).',
        'doc_url': '/rest/documentation/info/compara_methods',
        'content_type': 'application/json'},

    'compara_species_sets': {
        'method': 'GET',
        'url': '/rest/info/compara/species_sets/{{method}}',
        'doc': 'List all collections of species analysed with the specified compara method.',
        'doc_url': '/rest/documentation/info/compara_species_sets',
        'content_type': 'application/json'},

    'comparas': {
        'method': 'GET',
        'url': '/rest/info/comparas',
        'doc': 'Lists all available comparative genomics databases and their data release.',
        'doc_url': '/rest/documentation/info/comparas',
        'content_type': 'application/json'},

    'data': {
        'method': 'GET',
        'url': '/rest/info/data',
        'doc': 'Shows the data releases available on this REST server. May return more than one release (unfrequent non-standard Ensembl configuration).',
        'doc_url': 'nfrequent non-standard Ensembl configuration).',
        'doc_url': '/rest/documentation/info/data',
        'content_type': 'application/json'},

    'external_dbs': {
        'method': 'GET',
        'url': '/rest/info/external_dbs/{{species}}',
        'doc': 'Lists all available external sources for a species.',
        'doc_url': '/rest/documentation/info/external_dbs',
        'content_type': 'application/json'},

    'ping': {
        'method': 'GET',
        'url': '/rest/info/ping',
        'doc': 'Checks if the service is alive.',
        'doc_url': '/rest/documentation/info/ping',
        'content_type': 'application/json'},

    'rest': {
        'method': 'GET',
        'url': '/rest/info/rest',
        'doc': 'Shows the current version of the Ensembl REST API.',
        'doc_url': '/rest/documentation/info/rest',
        'content_type': 'application/json'},

    'software': {
        'method': 'GET',
        'url': '/rest/info/software',
        'doc': 'Shows the current version of the Ensembl API used by the REST server.',
        'doc_url': '/rest/documentation/info/software',
        'content_type': 'application/json'},

    'species': {
        'method': 'GET',
        'url': '/rest/info/species',
        'doc': 'Lists all available species, their aliases, available adaptor groups and data release.',
        'doc_url': '/rest/documentation/info/species',
        'content_type': 'application/json'},

    'variation': {
        'method': 'GET',
        'url': '/rest/info/variation/{{species}}',
        'doc': 'List the variation sources used in Ensembl for a species.',
        'doc_url': '/rest/documentation/info/variation',
        'content_type': 'application/json'},

    'variation_consequence_types': {
        'method': 'GET',
        'url': '/rest/info/variation/consequence_types',
        'doc': 'Lists all variant consequence types.',
        'doc_url': '/rest/documentation/info/variation_consequence_types',
        'content_type': 'application/json'},

    'variation_populations': {
        'method': 'GET',
        'url': '/rest/info/variation/populations/{{species}}',
        'doc': 'List all populations for a species',
        'doc_url': '/rest/documentation/info/variation_populations',
        'content_type': 'application/json'},

    'ld_id_get': {
        'method': 'GET',
        'url': '/rest/ld/{{species}}/{{id}}/{{population_name}}',
        'doc': 'Computes and returns LD values between the given variant and all other variants in a window centered around the given variant. The window size is set to 500 kb.',
        'doc_url': '/rest/documentation/info/ld_id_get',
        'content_type': 'application/json'},

    'ld_pairwise_get': {
        'method': 'GET',
        'url': '/rest/ld/{{species}}/pairwise/{{id1}}/{{id2}}',
        'doc': 'Computes and returns LD values between the given variants.',
        'doc_url': '/rest/documentation/info/ld_pairwise_get',
        'content_type': 'application/json'},

    'ld_region_get': {
        'method': 'GET',
        'url': '/rest/ld/{{species}}/region/{{region}}/{{population_name}}',
        'doc': 'Computes and returns LD values between all pairs of variants in the defined region.',
        'doc_url': '/rest/documentation/info/ld_region_get',
        'content_type': 'application/json'},

    'lookup': {
        'method': 'GET',
        'url': '/rest/lookup/id/{{id}}',
        'doc': 'Find the species and database for a single identifier e.g. gene, transcript, protein',
        'doc_url': '/rest/documentation/info/lookup',
        'content_type': 'application/json'},

    'lookup_post': {
        'method': 'POST',
        'url': '/rest/lookup/id',
        'doc': 'Find the species and database for several identifiers. IDs that are not found are returned with no data.',
        'doc_url': '/rest/documentation/info/lookup_post',
        'content_type': 'application/json'},

    'symbol_lookup': {
        'method': 'GET',
        'url': '/rest/lookup/symbol/{{species}}/{{symbol}}',
        'doc': 'Find the species and database for a symbol in a linked external database',
        'doc_url': '/rest/documentation/info/symbol_lookup',
        'content_type': 'application/json'},

    'symbol_post': {
        'method': 'POST',
        'url': '/rest/lookup/symbol/{{species}}/{{symbol}}',
        'doc': 'Find the species and database for a set of symbols in a linked external database. Unknown symbols are omitted from the response.',
        'doc_url': '/rest/documentation/info/symbol_post',
        'content_type': 'application/json'},

    'assembly_cdna': {
        'method': 'GET',
        'url': '/rest/map/cdna/{{id}}/{{region}}',
        'doc': 'Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.',
        'doc_url': '/rest/documentation/info/assembly_cdna',
        'content_type': 'application/json'},

    'assembly_cds': {
        'method': 'GET',
        'url': '/rest/map/cds/{{id}}/{{region}}',
        'doc': 'Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.',
        'doc_url': '/rest/documentation/info/assembly_cds',
        'content_type': 'application/json'},

    'assembly_map': {
        'method': 'GET',
        'url': '/rest/map/{{species}}/{{asm_one}}/{{region}}/{{asm_two}}',
        'doc': 'Convert the co-ordinates of one assembly to another',
        'doc_url': '/rest/documentation/info/assembly_map',
        'content_type': 'application/json'},

    'assembly_translation': {
        'method': 'GET',
        'url': '/rest/map/translation/{{id}}/{{region}}',
        'doc': 'Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API.',
        'doc_url': '/rest/documentation/info/assembly_translation',
        'content_type': 'application/json'},

    'ontology_ancestors': {
        'method': 'GET',
        'url': '/rest/ontology/ancestors/{{id}}',
        'doc': 'Reconstruct the entire ancestry of a term from is_a and part_of relationships.',
        'doc_url': '/rest/documentation/info/ontology_ancestors',
        'content_type': 'application/json'},

    'ontology_ancestors_chart': {
        'method': 'GET',
        'url': '/rest/ontology/ancestors/chart/{{id}}',
        'doc': 'Reconstruct the entire ancestry of a term from is_a and part_of relationships.',
        'doc_url': '/rest/documentation/info/ontology_ancestors_chart',
        'content_type': 'application/json'},

    'ontology_descendants': {
        'method': 'GET',
        'url': '/rest/ontology/descendants/{{id}}',
        'doc': 'Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier',
        'doc_url': '/rest/documentation/info/ontology_descendants',
        'content_type': 'application/json'},

    'ontology_id': {
        'method': 'GET',
        'url': '/rest/ontology/id/{{id}}',
        'doc': 'Search for an ontological term by its namespaced identifier',
        'doc_url': '/rest/documentation/info/ontology_id',
        'content_type': 'application/json'},

    'ontology_name': {
        'method': 'GET',
        'url': '/rest/ontology/name/{{name}}',
        'doc': 'Search for a list of ontological terms by their name',
        'doc_url': '/rest/documentation/info/ontology_name',
        'content_type': 'application/json'},

    'taxonomy_classification': {
        'method': 'GET',
        'url': '/rest/taxonomy/classification/{{id}}',
        'doc': 'Return the taxonomic classification of a taxon node',
        'doc_url': '/rest/documentation/info/taxonomy_classification',
        'content_type': 'application/json'},

    'taxonomy_id': {
        'method': 'GET',
        'url': '/rest/taxonomy/id/{{id}}',
        'doc': 'Search for a taxonomic term by its identifier or name',
        'doc_url': '/rest/documentation/info/taxonomy_id',
        'content_type': 'application/json'},

    'taxonomy_name': {
        'method': 'GET',
        'url': '/rest/taxonomy/name/{{name}}',
        'doc': 'Search for a taxonomic id by a non-scientific name',
        'doc_url': '/rest/documentation/info/taxonomy_name',
        'content_type': 'application/json'},

    'overlap_id.': {
        'method': 'GET',
        'url': '/rest/overlap/id/{{id}}',
        'doc': 'Retrieves features (e.g. genes, transcripts, variants and more) that overlap a region defined by the given identifier.',
        'doc_url': '/rest/documentation/info/overlap_id',
        'content_type': 'application/json'},

    'overlap_region.': {
        'method': 'GET',
        'url': '/rest/overlap/region/{{species}}/{{region}}',
        'doc': 'Retrieves features (e.g. genes, transcripts, variants and more) that overlap a given region.',
        'doc_url': '/rest/documentation/info/overlap_region',
        'content_type': 'application/json'},

    'overlap_translation).': {
        'method': 'GET',
        'url': '/rest/overlap/translation/{{id}}',
        'doc': 'Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variants).',
        'doc_url': '/rest/documentation/info/overlap_translation',
        'content_type': 'application/json'},

    'phenotype_gene': {
        'method': 'GET',
        'url': '/rest//phenotype/gene/{{species}}/{{gene}}',
        'doc': 'Return phenotype annotations for a given gene.',
        'doc_url': '/rest/documentation/info/phenotype_gene',
        'content_type': 'application/json'},

    'phenotype_region': {
        'method': 'GET',
        'url': '/rest//phenotype/region/{{species}}/{{region}}',
        'doc': 'Return phenotype annotations that overlap a given genomic region.',
        'doc_url': '/rest/documentation/info/phenotype_region',
        'content_type': 'application/json'},

    'array': {
        'method': 'GET',
        'url': '/rest/regulatory/species/{{species}}/microarray/{{microarray}}/vendor/{{vendor}}',
        'doc': 'Returns information about a specific microarray',
        'doc_url': '/rest/documentation/info/array',
        'content_type': 'application/json'},

    'list_all_microarrays': {
        'method': 'GET',
        'url': '/rest/regulatory/species/{{species}}/microarray',
        'doc': 'Returns information about all microarrays available for the given species',
        'doc_url': '/rest/documentation/info/list_all_microarrays',
        'content_type': 'application/json'},

    'probe': {
        'method': 'GET',
        'url': '/rest/regulatory/species/{{species}}/microarray/{{microarray}}/probe/{{probe}}',
        'doc': 'Returns information about a specific probe from a microarray',
        'doc_url': '/rest/documentation/info/probe',
        'content_type': 'application/json'},

    'probe_set': {
        'method': 'GET',
        'url': '/rest/regulatory/species/{{species}}/microarray/{{microarray}}/probe_set/{{probe_set}}',
        'doc': 'Returns information about a specific probe_set from a microarray',
        'doc_url': '/rest/documentation/info/probe_set',
        'content_type': 'application/json'},

    'sequence_id': {
        'method': 'GET',
        'url': '/rest/sequence/id/{{id}}',
        'doc': 'Request multiple types of sequence by stable identifier. Supports feature masking and expand options.',
        'doc_url': '/rest/documentation/info/sequence_id',
        'content_type': 'application/json'},

    'sequence_id_post': {
        'method': 'POST',
        'url': '/rest/sequence/id',
        'doc': 'Request multiple types of sequence by a stable identifier list.',
        'doc_url': '/rest/documentation/info/sequence_id_post',
        'content_type': 'application/json'},

    'sequence_region': {
        'method': 'GET',
        'url': '/rest/sequence/region/{{species}}/{{region}}',
        'doc': 'Returns the genomic sequence of the specified region of the given species. Supports feature masking and expand options.',
        'doc_url': '/rest/documentation/info/sequence_region',
        'content_type': 'application/json'},

    'sequence_region_post': {
        'method': 'POST',
        'url': '/rest/sequence/region/{{species}}',
        'doc': 'Request multiple types of sequence by a list of regions.',
        'doc_url': '/rest/documentation/info/sequence_region_post',
        'content_type': 'application/json'},

    'variant_recoder': {
        'method': 'GET',
        'url': '/rest/variant_recoder/{{species}}/{{id}}',
        'doc': 'Translate a variant identifier or HGVS notation to all possible variant IDs and HGVS',
        'doc_url': '/rest/documentation/info/variant_recoder',
        'content_type': 'application/json'},

    'variant_recoder_post': {
        'method': 'POST',
        'url': '/rest/variant_recoder/{{species}}',
        'doc': 'Translate a list of variant identifiers or HGVS notations to all possible variant IDs and HGVS',
        'doc_url': '/rest/documentation/info/variant_recoder_post',
        'content_type': 'application/json'},

    'variation_id': {
        'method': 'GET',
        'url': '/rest/variation/{{species}}/{{id}}',
        'doc': 'Uses a variant identifier (e.g. rsID) to return the variation features including optional genotype, phenotype and population data.',
        'doc_url': '/rest/documentation/info/variation_id',
        'content_type': 'application/json'},

    'variation_pmcid_get': {
        'method': 'GET',
        'url': '/rest/variation/{{species}}/pmcid/{{pmcid}}',
        'doc': 'Fetch variants by publication using PubMed Central reference number (PMCID).',
        'doc_url': '/rest/documentation/info/variation_pmcid_get',
        'content_type': 'application/json'},

    'variation_pmid_get': {
        'method': 'GET',
        'url': '/rest/variation/{{species}}/pmid/{{pmid}}',
        'doc': 'Fetch variants by publication using PubMed reference number (PMID).',
        'doc_url': '/rest/documentation/info/variation_pmid_get',
        'content_type': 'application/json'},

    'variation_post': {
        'method': 'POST',
        'url': '/rest/variation/{{species}}/',
        'doc': 'Uses a list of variant identifiers (e.g. rsID) to return the variation features including optional genotype, phenotype and population data.',
        'doc_url': '/rest/documentation/info/variation_post',
        'content_type': 'application/json'}
}

# HTTP return status codes
http_status_codes = {
    200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
    400: ('Bad Request', 'Occurs during exceptional circumstances such as the service is unable to find an ID. '
                         'Check if the response Content-type was JSON. '
                         'If so the JSON object is an exception hash with the message keyed under error'),
    404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
    415: ('Unsupported Media Type', 'The server is refusing to service the request '
                                    'because the entity of the request is in a format not supported '
                                    'by the requested resource for the requested method'),
    429: ('Too Many Requests', 'You have been rate-limited; wait and retry. '
                               'The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will '
                               'inform you of how long you have until your limit is reset and what that limit was. '
                               'If you get this response and have not exceeded your limit '
                               'then check if you have made too many requests per second.'),
    500: ('Internal Server Error', 'This error is not documented. Maybe there is an error in user input or '
                                   'REST server could have problems. Try to do the query with curl. '
                                   'If your data input and query are correct, contact ensembl team'),
    503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}

# User agent
vectorbase_user_agent = 'py_VB_rest'
vectorbase_header = {'User-Agent': vectorbase_user_agent}
vectorbase_content_type = 'application/json'

# define known errors
ensembl_known_errors = [
    "something bad has happened",
    "Something went wrong while fetching from LDFeatureContainerAdaptor",
    "%s timeout" % vectorbase_user_agent
]
