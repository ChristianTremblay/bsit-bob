for f in b59_spaces.py
do
    ttl=${f/[.]py/.ttl}
    exp_ttl=${f/[.]py/exp.ttl}
    log_ttl=${f/[.]py/log.txt}
    onto_ttl=$S223_DIRECTORY/inference/model-rules.shapes.ttl
    echo $ttl $log_ttl $exp_ttl $onto_ttl

    # python3 "$f" | python ../sort_turtle_file.py > "$ttl"
    python3 "$f" > "$ttl"
    python3 ../../../validate.py "$ttl" --rdfs --ontology "$onto_ttl" --inference "$exp_ttl" > "$log_ttl"

    
done