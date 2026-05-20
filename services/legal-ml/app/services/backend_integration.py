import httpx
import json
from typing import Dict, Any, Optional
from datetime import datetime
import os


class BackendIntegration:
    """
    Service to send analysis results to your backend
    Configure with your backend URL
    """
    
    def __init__(self, backend_url: Optional[str] = None):
        """
        Initialize backend integration
        
        Args:
            backend_url: Your backend API URL (e.g., http://your-backend.com/api)
        """
        self.backend_url = backend_url or os.getenv("BACKEND_URL", "http://localhost:3000/api")
        self.api_key = os.getenv("BACKEND_API_KEY", "")
        self.timeout = 30.0
    
    async def send_analysis_result(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send analysis results to backend
        
        Args:
            analysis_data: Complete analysis response
            
        Returns:
            Backend response
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.backend_url}/analysis/results",
                    json=analysis_data,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"❌ Failed to send results to backend: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch document from backend
        
        Args:
            document_id: Document identifier
            
        Returns:
            Document data or None
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.backend_url}/documents/{document_id}",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            print(f"❌ Failed to fetch document: {e}")
            return None
    
    async def update_analysis_status(
        self, 
        analysis_id: str, 
        status: str, 
        progress: Optional[int] = None
    ) -> bool:
        """
        Update analysis status in backend
        
        Args:
            analysis_id: Analysis identifier
            status: Status (queued/processing/completed/failed)
            progress: Optional progress percentage
            
        Returns:
            Success boolean
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    f"{self.backend_url}/analysis/{analysis_id}/status",
                    json={"status": status, "progress": progress},
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return True
                
        except httpx.HTTPError as e:
            print(f"❌ Failed to update status: {e}")
            return False
    
    async def notify_webhook(self, webhook_url: str, data: Dict[str, Any]) -> bool:
        """
        Send notification to webhook URL
        
        Args:
            webhook_url: URL to notify
            data: Data to send
            
        Returns:
            Success boolean
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    webhook_url,
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return True
                
        except httpx.HTTPError as e:
            print(f"❌ Webhook notification failed: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for backend requests"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Nyay-Samiti-AI/2.0"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers


# Global instance
_backend_integration = None


def get_backend_integration() -> BackendIntegration:
    """Get or create backend integration instance"""
    global _backend_integration
    if _backend_integration is None:
        _backend_integration = BackendIntegration()
    return _backend_integration
