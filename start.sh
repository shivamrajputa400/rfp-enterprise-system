#!/bin/bash
echo "🚀 Starting RFP Agentic AI System v2.0..."
echo "🌐 Frontend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo "🛑 Press Ctrl+C to stop"
echo ""
source venv/bin/activate
python -m backend.main_simple
