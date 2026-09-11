# Graph Report - map-to-poster-backend  (2026-09-11)

## Corpus Check
- Corpus is ~7,335 words - fits in a single context window. You may not need a graph.

## Summary
- 243 nodes · 329 edges · 49 communities (9 shown, 14 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.93)
- Token cost: 75,000 input · 7,633 output

## Community Hubs (Navigation)
- Theme CRUD API
- Poster Rendering & Export
- Poster Layout & Typography
- Map Geometry Processing
- Map Caching & OSM Worker
- Service Infra & Dependencies
- Map Service API & Models
- Theme Loader & Registry
- Location Service API
- Loading Animation Utility
- Map Zoom Coverage Utility
- Postman Workspace Config
- httpx Dependency (location)
- pydantic Dependency (location)
- uvicorn Dependency (location)
- geopandas Dependency
- networkx Dependency
- pydantic Dependency (map)
- shapely Dependency
- uvicorn Dependency (map)
- httpx Dependency (poster)
- numpy Dependency
- uvicorn Dependency (poster)

## God Nodes (most connected - your core abstractions)
1. `ThemeModel` - 16 edges
2. `render_poster()` - 11 edges
3. `process_job()` - 10 edges
4. `render_map_poster()` - 9 edges
5. `process_map_data()` - 8 edges
6. `Map` - 8 edges
7. `get_layout()` - 8 edges
8. `postgres (PostGIS) service` - 8 edges
9. `map-service container` - 8 edges
10. `poster-service container` - 7 edges

## Surprising Connections (you probably didn't know these)
- `psycopg2-binary (map-service dependency)` --shares_data_with--> `postgres (PostGIS) service`  [INFERRED]
  services/map-service/requirements.txt → infrastructure/docker-compose.yml
- `sqlalchemy (map-service dependency)` --shares_data_with--> `postgres (PostGIS) service`  [INFERRED]
  services/map-service/requirements.txt → infrastructure/docker-compose.yml
- `psycopg2-binary (poster-service dependency)` --shares_data_with--> `postgres (PostGIS) service`  [INFERRED]
  services/poster-service/requirements.txt → infrastructure/docker-compose.yml
- `sqlalchemy (poster-service dependency)` --shares_data_with--> `postgres (PostGIS) service`  [INFERRED]
  services/poster-service/requirements.txt → infrastructure/docker-compose.yml
- `map-service container` --references--> `fastapi (map-service dependency)`  [INFERRED]
  infrastructure/docker-compose.yml → services/map-service/requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared FastAPI Web Framework Across Microservices** — services_location_service_requirements_fastapi, services_map_service_requirements_fastapi, services_poster_service_requirements_fastapi [INFERRED 0.85]
- **Map-Service Geospatial Graph Processing Stack** — services_map_service_requirements_osmnx, services_map_service_requirements_geopandas, services_map_service_requirements_shapely, services_map_service_requirements_networkx [INFERRED 0.85]
- **Shared PostGIS/Postgres Persistence via SQLAlchemy** — services_map_service_requirements_sqlalchemy, services_poster_service_requirements_sqlalchemy, infrastructure_docker_compose_postgres [INFERRED 0.85]

## Communities (49 total, 14 thin omitted)

### Community 0 - "Theme CRUD API"
Cohesion: 0.12
Nodes (26): delete, put, Base, ThemeModel, create_theme(), delete_theme(), get_theme(), get_themes() (+18 more)

### Community 1 - "Poster Rendering & Export"
Cohesion: 0.10
Nodes (19): get_map_data(), health(), get, post, Session, render_map_poster(), Render MapToPoster-style poster. Pipeline: Map Data ↓ Map Bounds ↓ Map Camera ↓…, render_poster() (+11 more)

### Community 2 - "Poster Layout & Typography"
Cohesion: 0.12
Nodes (20): create_bottom_layout(), create_center_layout(), create_full_layout(), create_top_layout(), get_layout(), PosterLayout, Render roads using the Road Styling Engine., render_roads() (+12 more)

### Community 3 - "Map Geometry Processing"
Cohesion: 0.16
Nodes (17): extract_polygons(), polygon_to_coordinates(), get_bounds(), get_normalization_config(), normalize_coordinate(), normalize_coordinates(), Normalize a list of coordinates., Calculate one uniform scale factor. This preserves the geographic aspect ratio. (+9 more)

### Community 4 - "Map Caching & OSM Worker"
Cohesion: 0.17
Nodes (17): generate_cache_key(), get_cached_map(), Generate a stable cache key for a map location., Retrieve processed map geometry from Redis., Save processed JSON-serializable geometry to Redis., save_map_to_cache(), execute_with_fallback(), fetch_park_features() (+9 more)

### Community 5 - "Service Infra & Dependencies"
Cohesion: 0.13
Nodes (20): gateway (nginx API Gateway), location-service container, map-service container, map-worker container, poster_exports volume, poster-service container, postgres (PostGIS) service, postgres_data volume (+12 more)

### Community 6 - "Map Service API & Models"
Cohesion: 0.18
Nodes (14): on_event, init_db(), generate_map(), get_map(), health(), get, post, startup() (+6 more)

### Community 7 - "Theme Loader & Registry"
Cohesion: 0.17
Nodes (7): get_all_themes(), get_theme(), get_theme_names(), Return all available themes., Return available theme keys., Get a theme by its key. Example: get_theme("midnight"), Theme

### Community 8 - "Location Service API"
Cohesion: 0.40
Nodes (5): health(), LocationResponse, BaseModel, get, search_location()

## Knowledge Gaps
- **24 isolated node(s):** `Config`, `Postman Workspace (45c71a01-8a0c-43a9-8b4c-6a3f596c8288)`, `Postman Workspace Globals`, `postgres_data volume`, `poster_exports volume` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 107 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ThemeModel` connect `Theme CRUD API` to `Poster Rendering & Export`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `render_poster()` connect `Poster Rendering & Export` to `Poster Layout & Typography`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `render_map_poster()` connect `Poster Rendering & Export` to `Theme CRUD API`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ThemeModel` (e.g. with `render_map_poster()` and `create_theme()`) actually correct?**
  _`ThemeModel` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `render_map_poster()` (e.g. with `ThemeModel` and `PosterRenderRequest`) actually correct?**
  _`render_map_poster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Postman Workspace (45c71a01-8a0c-43a9-8b4c-6a3f596c8288)`, `Postman Workspace Globals` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Theme CRUD API` be split into smaller, more focused modules?**
  _Cohesion score 0.11895161290322581 - nodes in this community are weakly interconnected._