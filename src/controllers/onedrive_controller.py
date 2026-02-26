"""OneDrive integration controller."""
import os
from typing import Optional

import msal
import requests


class OneDriveController:
    """Manages OneDrive uploads."""
    
    def __init__(self, client_id: str = "", tenant_id: str = "", enabled: bool = False):
        """Initialize OneDrive controller.
        
        Args:
            client_id: Azure AD application client ID
            tenant_id: Azure AD tenant ID
            enabled: Whether OneDrive integration is enabled
        """
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.enabled = enabled
        self.access_token: Optional[str] = None
        self._msal_app: Optional[msal.PublicClientApplication] = None

    def _get_authority(self) -> str:
        """Return Azure AD authority URL."""
        tenant = (self.tenant_id or "common").strip()
        return f"https://login.microsoftonline.com/{tenant}"

    def _get_msal_app(self) -> msal.PublicClientApplication:
        """Return cached MSAL PublicClientApplication instance."""
        if self._msal_app is None:
            self._msal_app = msal.PublicClientApplication(
                client_id=self.client_id,
                authority=self._get_authority()
            )
        return self._msal_app

    def start_device_flow(self, scopes: Optional[list[str]] = None) -> Optional[dict]:
        """Start OAuth device code flow and return flow details.

        Args:
            scopes: Optional list of Graph scopes

        Returns:
            Flow dictionary containing `user_code`, `verification_uri`, etc.
            or None if flow initialization fails.
        """
        if not self.client_id:
            return None

        requested_scopes = scopes or ["Files.ReadWrite", "offline_access", "User.Read"]

        try:
            app = self._get_msal_app()
            flow = app.initiate_device_flow(scopes=requested_scopes)
            if not flow or "user_code" not in flow:
                return None
            return flow
        except Exception as e:
            print(f"Error starting OneDrive device flow: {e}")
            return None

    def complete_device_flow(self, flow: dict) -> bool:
        """Complete OAuth device flow and store access token.

        Args:
            flow: Flow object returned by `start_device_flow`

        Returns:
            True if token acquired, False otherwise
        """
        if not flow:
            return False

        try:
            app = self._get_msal_app()
            result = app.acquire_token_by_device_flow(flow)

            token = result.get("access_token") if isinstance(result, dict) else None
            if token:
                self.access_token = token
                return True

            error = result.get("error_description", "Unknown error") if isinstance(result, dict) else "Unknown error"
            print(f"OneDrive authentication failed: {error}")
            return False
        except Exception as e:
            print(f"Error completing OneDrive device flow: {e}")
            return False
    
    def authenticate_with_credentials(self, email: str, password: str) -> bool:
        """Authenticate with OneDrive using email and password.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            True if authentication successful, False otherwise
        """
        if not self.client_id:
            print("Client ID is required for authentication")
            return False
        
        requested_scopes = ["https://graph.microsoft.com/.default", "offline_access"]
        
        try:
            app = self._get_msal_app()
            result = app.acquire_token_by_username_password(
                username=email,
                password=password,
                scopes=requested_scopes
            )
            
            if isinstance(result, dict) and "access_token" in result:
                self.access_token = result["access_token"]
                self.enabled = True
                return True
            
            error = result.get("error_description", "Unknown error") if isinstance(result, dict) else "Unknown error"
            print(f"OneDrive authentication failed: {error}")
            return False
            
        except Exception as e:
            print(f"Error during OneDrive authentication: {e}")
            return False
    
    def authenticate(self) -> bool:
        """Authenticate with OneDrive.
        
        Returns:
            True if authentication successful, False otherwise
        """
        if not self.enabled or not self.client_id:
            return False

        flow = self.start_device_flow()
        if not flow:
            return False

        return self.complete_device_flow(flow)

    def authenticate_interactive(self, scopes: Optional[list[str]] = None) -> bool:
        """Authenticate using interactive browser flow (email + phone validation).

        Args:
            scopes: Optional list of Graph scopes

        Returns:
            True if authentication successful, False otherwise
        """
        if not self.client_id:
            return False

        requested_scopes = scopes or ["Files.ReadWrite", "offline_access", "User.Read"]

        try:
            app = self._get_msal_app()
            result = app.acquire_token_interactive(
                scopes=requested_scopes,
                prompt="select_account"
            )

            if isinstance(result, dict) and "access_token" in result:
                self.access_token = result["access_token"]
                self.enabled = True
                return True

            error = result.get("error_description", "Unknown error") if isinstance(result, dict) else "Unknown error"
            print(f"OneDrive interactive authentication failed: {error}")
            return False

        except Exception as e:
            print(f"Error during OneDrive interactive authentication: {e}")
            return False
    
    def upload_photo(self, file_path: str, remote_folder: str = "/Photos/Photobooth") -> bool:
        """Upload a photo to OneDrive.
        
        Args:
            file_path: Local path to photo file
            remote_folder: Remote folder path in OneDrive
            
        Returns:
            True if upload successful, False otherwise
        """
        if not self.enabled or not os.path.exists(file_path):
            return False

        if not self.access_token:
            if not self.authenticate():
                return False

        try:
            filename = os.path.basename(file_path)
            normalized_folder = (remote_folder or "/Photos/Photobooth").strip()
            if not normalized_folder.startswith("/"):
                normalized_folder = f"/{normalized_folder}"
            normalized_folder = normalized_folder.rstrip("/")

            upload_path = f"{normalized_folder}/{filename}" if normalized_folder else f"/{filename}"
            endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:{upload_path}:/content"

            with open(file_path, "rb") as photo_file:
                response = requests.put(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/octet-stream"
                    },
                    data=photo_file,
                    timeout=60
                )

            if response.status_code in (200, 201):
                return True

            if response.status_code == 401:
                self.access_token = None
                print("OneDrive token expired, retrying authentication...")
                return self.upload_photo(file_path, remote_folder)

            print(
                "Error uploading to OneDrive: "
                f"HTTP {response.status_code} - {response.text[:300]}"
            )
            return False
        except Exception as e:
            print(f"Error uploading to OneDrive: {e}")
            return False
