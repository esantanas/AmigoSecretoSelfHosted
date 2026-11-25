import base64
import mimetypes
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scope estricto: solo permite enviar correos
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class GmailSender:
    def __init__(self, credentials_path="credentials.json", token_path="token.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _authenticate(self):
        """Gestiona la autenticación OAuth2 y genera/actualiza el token."""
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # Si no hay credenciales válidas, inicia el flujo de login en el navegador
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Guarda el token para futuras ejecuciones sin intervención manual
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def send_email(self, to, subject, body, is_html=False, attachments=None):
        """
        Envía un correo electrónico.

        :param to: Correo del destinatario (str) o lista de correos (list).
        :param subject: Asunto del correo (str).
        :param body: Cuerpo del mensaje (str).
        :param is_html: True si el cuerpo contiene etiquetas HTML, False si es texto plano.
        :param attachments: Lista de rutas de archivos a adjuntar (list de str).
        :return: Diccionario con la respuesta de la API (incluye el 'id' del mensaje) o None si falla.
        """
        try:
            message = EmailMessage()

            # Configurar destinatarios
            if isinstance(to, list):
                message["To"] = ", ".join(to)
            else:
                message["To"] = to

            message["Subject"] = subject

            # Configurar cuerpo (Texto plano o HTML)
            if is_html:
                message.set_content("Tu cliente de correo no soporta HTML.")
                message.add_alternative(body, subtype="html")
            else:
                message.set_content(body)

            # Procesar archivos adjuntos si existen
            if attachments:
                for file_path in attachments:
                    if not os.path.isfile(file_path):
                        print(f"Advertencia: No se encontró el archivo {file_path}")
                        continue

                    mime_type, _ = mimetypes.guess_type(file_path)
                    if mime_type is None:
                        mime_type = "application/octet-stream"
                    maintype, subtype = mime_type.split("/", 1)

                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        file_name = os.path.basename(file_path)

                    message.add_attachment(
                        file_data,
                        maintype=maintype,
                        subtype=subtype,
                        filename=file_name,
                    )

            # Codificar el mensaje en base64 seguro para URLs (requisito de la API)
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}

            # Llamada a la API para enviar
            send_result = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            return send_result

        except HttpError as error:
            print(f"Ocurrió un error en la API de Gmail: {error}")
            return None