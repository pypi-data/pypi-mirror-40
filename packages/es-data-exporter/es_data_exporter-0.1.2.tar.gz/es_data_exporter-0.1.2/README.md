# Elasticsearch Data Exporter

## Installation 

```
pip install es_data_exporter
```

### ES Search Exporter Configuration

You will need to add your Elasticsearch query to the searches hash in es.yml.
This could also be a JSON file as well if that would make it easier (JSON is valid
YAML, and most tools like Kibana can produce a JSON version of your query).

### Prometheus Job Configuration

```
scrape_configs:
  - job_name: 'es_data_exporter'
    params:
      search: ['example']
    relabel_configs:
      - source_labels: [__address__]
        regex: (.*?)(:80)?
        target_label: __param_target
      - source_labels: []
        regex: .*
        target_label: __address__
      - source_labels: [__address__]
        regex: (.*)
        target_label: instance 
```

## Developing Locally

To work on this locally without installing the package, execute:

```
./scripts/run --kerberos --tls
```

This script will setup your path correctly and run the exporter.
