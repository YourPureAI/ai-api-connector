import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Lock, Save, Code, FileText, Globe, Trash2 } from 'lucide-react';

const ConnectorDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [connector, setConnector] = useState(null);
    const [secrets, setSecrets] = useState({});
    const [saving, setSaving] = useState(false);
    const [loading, setLoading] = useState(true);
    const [functionDef, setFunctionDef] = useState('');
    const [functionFormat, setFunctionFormat] = useState('yaml');
    const [addingFunction, setAddingFunction] = useState(false);
    const [showExample, setShowExample] = useState(false);

    useEffect(() => {
        const fetchConnector = async () => {
            try {
                const response = await axios.get(`/api/v1/connectors/${id}`);
                setConnector(response.data);
            } catch (error) {
                console.error("Error fetching connector:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchConnector();
    }, [id]);

    const handleInputChange = (key, value) => {
        setSecrets(prev => ({ ...prev, [key]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        try {
            await axios.post(`/api/v1/connectors/${id}/secrets`, secrets);
            alert("Secrets saved successfully!");
            navigate('/');
        } catch (error) {
            console.error("Error saving secrets:", error);
            alert("Failed to save secrets.");
        } finally {
            setSaving(false);
        }
    };

    const handleAddFunction = async () => {
        if (!functionDef.trim()) {
            alert("Please enter a function definition");
            return;
        }

        setAddingFunction(true);
        try {
            const response = await axios.post(`/api/v1/connectors/${id}/add-function`, {
                function_definition: functionDef,
                format: functionFormat
            });

            console.log('Add function response:', response.data);

            alert(response.data.message + (response.data.conflicts ? `\n\nWarning: Overwrote existing functions: ${response.data.conflicts.join(', ')}` : ''));
            setFunctionDef('');

            // Refresh connector data
            const updatedConnector = await axios.get(`/api/v1/connectors/${id}`);
            console.log('Updated connector:', updatedConnector.data);
            console.log('Updated paths:', updatedConnector.data.full_schema_json?.paths);
            setConnector(updatedConnector.data);
        } catch (error) {
            console.error("Error adding function:", error);
            alert(error.response?.data?.detail || "Failed to add function");
        } finally {
            setAddingFunction(false);
        }
    };

    const handleDeleteFunction = async (path, method) => {
        if (!confirm(`Are you sure you want to delete ${method.toUpperCase()} ${path}?\n\nThis will remove the function from the connector and vector database.`)) {
            return;
        }

        try {
            const response = await axios.delete(`/api/v1/connectors/${id}/function`, {
                params: { path, method }
            });

            alert(response.data.message);

            // Refresh connector data
            const updatedConnector = await axios.get(`/api/v1/connectors/${id}`);
            setConnector(updatedConnector.data);
        } catch (error) {
            console.error("Error deleting function:", error);
            alert(error.response?.data?.detail || "Failed to delete function");
        }
    };

    if (loading) return <div className="p-8 text-center">Loading connector details...</div>;
    if (!connector) return <div className="p-8 text-center text-red-600">Connector not found.</div>;

    const { full_schema_json } = connector;
    const paths = full_schema_json?.paths || {};

    return (
        <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Left Column: Auth Configuration */}
            <div className="lg:col-span-1 space-y-6">
                <div>
                    <h2 className="text-xl font-bold text-gray-900">Configuration</h2>
                    <p className="text-sm text-gray-500">Manage authentication and secrets.</p>
                </div>

                <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex items-center gap-3 mb-6 p-3 bg-yellow-50 text-yellow-800 rounded-lg">
                        <Lock size={16} />
                        <p className="text-xs">Credentials are encrypted and stored securely in the local vault.</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                            <input
                                type="password"
                                onChange={(e) => handleInputChange('api_key', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-sm"
                                placeholder="sk_..."
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Client ID (Optional)</label>
                            <input
                                type="text"
                                onChange={(e) => handleInputChange('client_id', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-sm"
                                placeholder="client_..."
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={saving}
                            className={`w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-white font-medium text-sm transition-colors ${saving ? 'bg-gray-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'}`}
                        >
                            <Save size={16} />
                            {saving ? 'Saving...' : 'Save Credentials'}
                        </button>
                    </form>
                </div>
            </div>

            {/* Right Column: Connector Info & Functions */}
            <div className="lg:col-span-2 space-y-6">
                <div>
                    <h2 className="text-xl font-bold text-gray-900">{connector.name}</h2>
                    <div className="flex items-center gap-4 text-sm text-gray-500 mt-1">
                        <span className="flex items-center gap-1"><Globe size={14} /> v{connector.version}</span>
                        <span className="flex items-center gap-1"><FileText size={14} /> OpenAPI Spec</span>
                    </div>
                    <p className="mt-2 text-gray-600">{connector.description}</p>
                </div>

                {/* Add New Function Section */}
                <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
                        <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                            <Code size={18} className="text-indigo-600" />
                            Add New Function
                        </h3>
                        <p className="text-sm text-gray-500 mt-1">Paste a function definition to extend this connector</p>
                    </div>

                    <div className="p-6 space-y-4">
                        {/* Format Selector */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Format</label>
                            <div className="flex gap-4">
                                <label className="flex items-center gap-2 cursor-pointer">
                                    <input
                                        type="radio"
                                        value="yaml"
                                        checked={functionFormat === 'yaml'}
                                        onChange={(e) => setFunctionFormat(e.target.value)}
                                        className="text-indigo-600 focus:ring-indigo-500"
                                    />
                                    <span className="text-sm text-gray-700">YAML</span>
                                </label>
                                <label className="flex items-center gap-2 cursor-pointer">
                                    <input
                                        type="radio"
                                        value="json"
                                        checked={functionFormat === 'json'}
                                        onChange={(e) => setFunctionFormat(e.target.value)}
                                        className="text-indigo-600 focus:ring-indigo-500"
                                    />
                                    <span className="text-sm text-gray-700">JSON</span>
                                </label>
                            </div>
                        </div>

                        {/* Function Definition Input */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Function Definition</label>
                            <textarea
                                value={functionDef}
                                onChange={(e) => setFunctionDef(e.target.value)}
                                placeholder={functionFormat === 'yaml' ?
                                    '/pets/{petId}:\n  get:\n    summary: Get a pet by ID\n    operationId: getPetById\n    ...' :
                                    '{\n  "/pets/{petId}": {\n    "get": {\n      "summary": "Get a pet by ID",\n      ...\n    }\n  }\n}'
                                }
                                className="w-full h-64 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none font-mono text-sm"
                            />
                        </div>

                        {/* Example Toggle */}
                        <button
                            onClick={() => setShowExample(!showExample)}
                            className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
                        >
                            {showExample ? 'Hide' : 'Show'} Example
                        </button>

                        {/* Example */}
                        {showExample && (
                            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                                <p className="text-xs font-medium text-gray-700 mb-2">Example {functionFormat.toUpperCase()}:</p>
                                <pre className="text-xs font-mono text-gray-800 overflow-x-auto">
                                    {functionFormat === 'yaml' ?
                                        `/pets/{petId}:
  get:
    summary: Get a pet by ID
    operationId: getPetById
    parameters:
      - name: petId
        in: path
        required: true
        schema:
          type: integer
    responses:
      '200':
        description: Success
        content:
          application/json:
            schema:
              type: object` :
                                        `{
  "/pets/{petId}": {
    "get": {
      "summary": "Get a pet by ID",
      "operationId": "getPetById",
      "parameters": [
        {
          "name": "petId",
          "in": "path",
          "required": true,
          "schema": {"type": "integer"}
        }
      ],
      "responses": {
        "200": {
          "description": "Success"
        }
      }
    }
  }
}`}
                                </pre>
                            </div>
                        )}

                        {/* Add Button */}
                        <button
                            onClick={handleAddFunction}
                            disabled={addingFunction || !functionDef.trim()}
                            className={`w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-white font-medium transition-colors ${addingFunction || !functionDef.trim()
                                ? 'bg-gray-300 cursor-not-allowed'
                                : 'bg-indigo-600 hover:bg-indigo-700'
                                }`}
                        >
                            <Code size={16} />
                            {addingFunction ? 'Adding Function...' : 'Add Function'}
                        </button>
                    </div>
                </div>

                {/* Available Functions */}
                <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
                        <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                            <Code size={18} className="text-indigo-600" />
                            Available Functions
                        </h3>
                        <span className="text-xs font-medium bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">
                            {Object.keys(paths).length} Paths
                        </span>
                    </div>

                    <div className="divide-y divide-gray-100 max-h-[600px] overflow-y-auto">
                        {Object.entries(paths).map(([path, methods]) => (
                            Object.entries(methods).map(([method, details]) => (
                                <div key={`${method}-${path}`} className="p-4 hover:bg-gray-50 transition-colors">
                                    <div className="flex items-start gap-3">
                                        <span className={`uppercase text-[10px] font-bold px-2 py-1 rounded border ${method === 'get' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                                            method === 'post' ? 'bg-green-50 text-green-700 border-green-200' :
                                                method === 'delete' ? 'bg-red-50 text-red-700 border-red-200' :
                                                    'bg-gray-50 text-gray-700 border-gray-200'
                                            }`}>
                                            {method}
                                        </span>
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-2 mb-1">
                                                <code className="text-sm font-mono text-gray-700">{path}</code>
                                                {details.operationId && (
                                                    <span className="text-xs text-gray-400 font-mono">({details.operationId})</span>
                                                )}
                                            </div>
                                            <p className="text-sm text-gray-600 line-clamp-2">{details.summary || details.description || "No description available"}</p>
                                        </div>
                                        <button
                                            onClick={() => handleDeleteFunction(path, method)}
                                            className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                                            title="Delete this function"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            ))
                        ))}
                        {Object.keys(paths).length === 0 && (
                            <div className="p-8 text-center text-gray-500">No paths found in OpenAPI spec.</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ConnectorDetail;
