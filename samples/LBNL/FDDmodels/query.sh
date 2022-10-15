for f in Equipment_props.py
do
    ttl=${f/[.]py/.ttl}
    exp_ttl=${f/[.]py/exp.ttl}
    log_ttl=${f/[.]py/log.txt}
    onto_ttl=$S223_DIRECTORY/inference/model-rules.shapes.ttl
    echo $ttl $log_ttl $exp_ttl $onto_ttl

    sparql_query="""
    SELECT ?o 
    WHERE {
    	?s a sh:SPARQLRule ;
    		sh:construct ?o .

    }

    """
    # sparql_query="""
    # Construct {LBNL:newobject a ?o} 
    # WHERE {
    # 	?s a ?o .

    # }

    # """
    # python3 "$f" | python ../sort_turtle_file.py > "$ttl"
    #python3 "$f" > "$ttl"
   # python3 ../../../sparql-query.py "$onto_ttl" <<< "$sparql_query" > "$log_ttl"
    #python3 ../../../validate.py "$ttl" --inference "$exp_ttl" --sparql_rule "device_props_rules.ttl" --s223_sparql_rule > "$log_ttl"
    python3 ../../../validate.py "$ttl" --inference "$exp_ttl" --shacl_rule "device_props_rules.ttl" --s223_sparql_rule > "$log_ttl"
    #python3 construct.py "$ttl" --expanded "$exp_ttl" > "$log_ttl"
done