from bob.core import prefixes


def sample_header(sample_name, suffix=None):
    sample_name = sample_name + "-" + suffix if suffix else sample_name
    header = f"""# baseURI: http://data.ashrae.org/standard223/1.0/sample/{sample_name}
# imports: http://data.ashrae.org/standard223/1.0/model/all

@prefix owl: {prefixes["owl"]} .
@prefix rdf: {prefixes["rdf"]} .
@prefix rdfs: {prefixes["rdfs"]} .
@prefix xsd: {prefixes["xsd"]} .

<http://data.ashrae.org/standard223/1.0/data/{sample_name}>
  a owl:Ontology ;
  rdfs:isDefinedBy <http://data.ashrae.org/standard223/1.0/sample/{sample_name}> ;
  rdfs:label "{sample_name}" ;
  owl:imports <http://data.ashrae.org/standard223/1.0/model/all> .

"""
    return header
