import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from app.core.config import settings
from app.services.vault import vault
import uuid

# Constants for config lookup
SYSTEM_USER_ID = "system"
GLOBAL_CONFIG_ID = "global_config"

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        # We don't initialize collection here anymore because we need the embedding function
        # which depends on the config at runtime.

    def _get_embedding_function(self):
        """
        Retrieves the configured embedding function based on system settings.
        """
        config = vault.get_secrets(SYSTEM_USER_ID, GLOBAL_CONFIG_ID)
        provider = config.get("embeddingProvider", "local")
        model_name = config.get("embeddingModel", "all-MiniLM-L6-v2")
        
        if provider == "openai":
            api_key = config.get("openaiApiKey")
            if api_key:
                return embedding_functions.OpenAIEmbeddingFunction(
                    api_key=api_key,
                    model_name=model_name
                )
        elif provider == "google":
            api_key = config.get("googleApiKey")
            if api_key:
                return embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                    api_key=api_key,
                    model_name=model_name if model_name else "models/embedding-001"
                )
        
        # Default / Local
        return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

    def _get_collection(self):
        """
        Gets the collection with the current embedding function.
        """
        ef = self._get_embedding_function()
        return self.client.get_or_create_collection(
            name="connector_functions",
            embedding_function=ef
        )

    def add_function_chunks(self, chunks: list, metadatas: list, ids: list):
        if not chunks:
            return
        
        collection = self._get_collection()
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def search_functions(self, query: str, n_results: int = 5):
        collection = self._get_collection()
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def delete_connector_functions(self, connector_id: str):
        # For deletion, we don't need to specify an embedding function
        # Get the collection without embedding function to avoid conflicts
        try:
            collection = self.client.get_collection(name="connector_functions")
            collection.delete(
                where={"connector_id": connector_id}
            )
        except Exception as e:
            print(f"Error deleting from vector DB: {str(e)}")
            # If collection doesn't exist, that's fine - nothing to delete
            pass

vector_db = VectorDB()

def process_and_store_connector_chunks(spec: dict, connector_id: str, user_id: str):
    chunks = []
    metadatas = []
    ids = []
    
    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if method not in ["get", "post", "put", "delete", "patch"]:
                continue
                
            operation_id = details.get("operationId")
            # Fallback if operationId is missing
            if not operation_id:
                operation_id = f"{method}_{path.replace('/', '_')}"
                
            summary = details.get("summary", "")
            description = details.get("description", "")
            
            # Create a semantic chunk
            chunk_text = f"Connector: {spec['info']['title']}. Function: {operation_id}. Path: {method.upper()} {path}. Description: {summary} {description}"
            
            chunks.append(chunk_text)
            metadatas.append({
                "connector_id": connector_id,
                "operation_id": operation_id,
                "user_id": user_id,
                "path": path,
                "method": method
            })
            ids.append(f"{connector_id}_{operation_id}")
            
    vector_db.add_function_chunks(chunks, metadatas, ids)
