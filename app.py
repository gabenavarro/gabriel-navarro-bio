import argparse
from fasthtml.common import serve
from src.core.app_factory import create_app
from src.core.routes import register_routes

# Create the application and router
app, rt = create_app()

# Register all routes
register_routes(app, rt)

if __name__ == "__main__":
    # Parse command line argument for port
    parser = argparse.ArgumentParser(description="Run the FastHTML app.")
    parser.add_argument("--port", type=int, default=80, help="Port to run the app on")
    args = parser.parse_args()

    # Serve the application
    serve(port=args.port, reload=False)
