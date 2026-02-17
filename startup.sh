#!/bin/bash
set -e

streamlit run app.py \
    --server.port=${STREAMLIT_SERVER_PORT:-8000} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
