### The Project
- Uses Python Faker to generate fake click stream from a shopping mall
- Spark Structured Streaming consumes the click stream topic and transforms it in real time
- Sinks structured data to an OLAP sink (Clickhouse) + RT dashboard
- Scheduled mart layer transformation(dbt) for historicals
- Grafana + Prometheus for metrics and visualization

### Purpose
- Stress-test the pipeline
- Pinpoint bottleneck
- Optimize for SLO
- Re-evaluate toolchain use

### SLO
- Schema check as early as possible per schema formation, 100% pass within the evo
- Boost from 1k to 2k events/s (600B per row of raw json byte data, padded for uniformity) without any bottleneck
- 80GB per day raw.
- Failure targets not set yet...

### Usage
- `docker compose up -d`
- Airflow UI → http://localhost:8080
- Kafka UI → http://localhost:8085
- Spark Master UI → http://localhost:8081
- Grafana → http://localhost:3000

### Future Plan
- Migrate to GCP