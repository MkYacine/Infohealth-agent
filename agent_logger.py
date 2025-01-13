import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import streamlit as st
from typing import List, Dict, Any

class AgentLogger:
    def __init__(self, conversation_id):
        """Initialize Firebase connection if not already initialized."""
        self.conversation_id = conversation_id
        self.db = None
        
        try:
            creds = self._get_firebase_credentials()
            if creds:
                if not firebase_admin._apps:
                    cred = credentials.Certificate(creds)
                    firebase_admin.initialize_app(cred)
                self.db = firestore.client()
        except Exception as e:
            st.warning(f"Failed to initialize Firebase: {str(e)}")

    def _get_firebase_credentials(self):
        """Get Firebase credentials from Streamlit secrets."""
        if 'firebase' in st.secrets:
            # Create a dictionary with all required fields from secrets
            creds = {
                "type": st.secrets.firebase["type"],
                "project_id": st.secrets.firebase["project_id"],
                "private_key_id": st.secrets.firebase["private_key_id"],
                "private_key": st.secrets.firebase["private_key"],
                "client_email": st.secrets.firebase["client_email"],
                "client_id": st.secrets.firebase["client_id"],
                "auth_uri": st.secrets.firebase["auth_uri"],
                "token_uri": st.secrets.firebase["token_uri"],
                "auth_provider_x509_cert_url": st.secrets.firebase["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets.firebase["client_x509_cert_url"],
                "universe_domain": st.secrets.firebase["universe_domain"]
            }
            return creds
        
        # If not available, return None and disable logging
        st.warning("No Firebase credentials found in Streamlit secrets. Logging will be disabled.")
        return None

    def log_chat(self, messages: List[Dict[str, str]]) -> None:
        """Log chat messages to Firestore.
        
        Args:
            messages: List containing the latest messages exchange
        """
        if not self.db:
            #print("early exit")
            return
        
        conversation_id = self.conversation_id

        try:
            # Get reference to the messages subcollection
            messages_ref = self.db.collection('conversations').document(conversation_id) \
                            .collection('messages')
            
            # Add timestamp and create document
            data = {
                'timestamp': datetime.now(),
                'messages': messages
            }
            messages_ref.add(data)
            #print("succesfully wrote logs")

        except Exception as e:
            st.error(f"Failed to log chat messages: {str(e)}")

    def log_completion(self, prompt: str, completion: str) -> None:
        """Log LLM completion to Firestore.
        
        Args:
            prompt: The prompt sent to the LLM
            completion: The completion received from the LLM
        """
        if not self.db:
            return
        
        conversation_id = self.conversation_id

        try:
            # Determine collection based on prompt type
            collection_name = 'railguard' if 'railguard' in prompt.lower() else 'extraction'
            
            # Get reference to the appropriate subcollection
            collection_ref = self.db.collection('conversations').document(conversation_id) \
                             .collection(collection_name)
            
            # Add timestamp and create document
            data = {
                'timestamp': datetime.now(),
                'prompt': prompt,
                'completion': completion
            }
            collection_ref.add(data)

        except Exception as e:
            st.error(f"Failed to log completion: {str(e)}")

    def log_flag(self, messages: List[Dict[str, str]], flagged_index: int) -> None:
        """Log flagged messages to Firestore.
        
        Args:
            messages: List of all messages in the conversation
            flagged_index: Index of the flagged message in the messages list
        """
        if not self.db:
            return
            
        try:
            # Get reference to the conversation's flags collection
            flags_collection = self.db.collection('flagged').document(self.conversation_id).collection('flags')
        
            
            # Add timestamp and create document
            data = {
                'timestamp': datetime.now(),
                'full_conversation': messages,
                'flagged_message_index': flagged_index
            }
            
            # Add a new document to the flags subcollection
            flags_collection.add(data)

        except Exception as e:
            st.error(f"Failed to log flagged message: {str(e)}")