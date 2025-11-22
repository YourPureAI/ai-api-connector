import chromadb
from app.core.config import settings

# Reset the ChromaDB collection to fix embedding function conflicts
client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

try:
    # Delete the existing collection
    client.delete_collection(name="connector_functions")
    print("✅ Successfully deleted 'connector_functions' collection")
except Exception as e:
    print(f"ℹ️  Collection may not exist: {e}")

print("✅ ChromaDB reset complete. The collection will be recreated with the correct embedding function on next use.")
