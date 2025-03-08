import uvicorn
from typing import Any

def start_server(host: str = "0.0.0.0", 
                port: int = 8080, 
                reload: bool = False,
                **kwargs: Any) -> None:
    """
    Starts the uvicorn server with the FastAPI application.
    
    Args:
        host (str): Host to bind to
        port (int): Port to bind to
        reload (bool): Enable auto-reload
        **kwargs: Additional uvicorn server options
    """
    uvicorn.run(
        "infrastructure.web.app:app",
        host=host,
        port=port,
        reload=reload,
        **kwargs
    ) 