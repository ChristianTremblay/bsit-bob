for f in ../ttl/g36-figure-a-1.ttl
do
    log_ttl=$"4-1Rule_log.txt"
    echo $f $log_ttl
 
    python3 ../../validate.py "$f" --shacl_rule "4-1Rule.ttl" > "$log_ttl"

done