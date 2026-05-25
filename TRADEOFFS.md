# TRADEOFFS.md

Given the 4-day time constraint, I made deliberate architectural tradeoffs to prioritize a sharp data model and a functional review pipeline over feature bloat. Here are three things I explicitly chose not to build:

**1. A Production-Grade Distance Calculation API**
* **What I omitted:** I did not integrate a live external API (like Google Maps or an aviation database) to calculate Great-Circle distances between all global airports.
* **Why:** Calling an external API during a batch ingestion loop introduces severe rate-limiting and latency issues. Instead, I built a mocked internal lookup dictionary. In production, this proves the architecture: we would populate a local database table with the coordinates of all 40,000+ airports and run a vectorized Haversine formula on our own servers to calculate distances instantly without external dependencies.

**2. Automated Unit Conversion Table**
* **What I omitted:** I did not build the backend mathematical logic to dynamically convert every possible unit (Gallons, Liters, MMBtu) into a single standard unit (MT CO2e) during ingestion.
* **Why:** Building an exhaustive, scientifically accurate conversion matrix (including localized grid emission factors for electricity) is a massive data engineering task. I prioritized building the *schema* to hold both the `raw_value` and the `normalized_value`, proving the system is ready to accept those conversion scripts once the sustainability scientists provide the exact factors.

**3. Complex Authentication and Role-Based Access Control (RBAC)**
* **What I omitted:** I did not build a login screen, JWT token management, or distinct "Analyst" vs. "Admin" roles for the frontend dashboard.
* **Why:** The core challenge of this assignment is data normalization and review workflow, not boilerplate auth. I utilized Django's built-in session framework for the backend and left the React dashboard open to prove the core user experience. In production, I would wrap the API routes in DRF permission classes.