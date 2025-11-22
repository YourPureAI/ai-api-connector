import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Plus, Activity, Trash2 } from 'lucide-react';

const Dashboard = () => {
    const [connectors, setConnectors] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchConnectors();
    }, []);

    const fetchConnectors = async () => {
        try {
            const response = await axios.get('/api/v1/connectors/');
            setConnectors(response.data);
        } catch (error) {
            console.error("Error fetching connectors:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id, name) => {
        if (window.confirm(`Are you sure you want to delete "${name}"? This action cannot be undone.`)) {
            try {
                await axios.delete(`/api/v1/connectors/${id}`);
                fetchConnectors(); // Refresh list
            } catch (error) {
                console.error("Error deleting connector:", error);
                const message = error.response?.data?.detail || "Failed to delete connector.";
                alert(message);
            }
        }
    };

    if (loading) return <div className="flex items-center justify-center h-64">Loading...</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">Active Connectors</h2>
                    <p className="text-gray-500">Manage your API integrations and their status.</p>
                </div>
                <Link to="/upload" className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                    <Plus size={20} />
                    Add Connector
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {connectors.map((connector) => (
                    <div key={connector.connector_id} className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow relative group">
                        <div className="flex items-start justify-between mb-4">
                            <div className="p-2 bg-blue-50 rounded-lg">
                                <Activity className="text-blue-600" size={24} />
                            </div>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${connector.status === 'ACTIVE' ? 'bg-green-100 text-green-700' :
                                connector.status === 'PENDING_SECRETS' ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-700'
                                }`}>
                                {connector.status.replace('_', ' ')}
                            </span>
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">{connector.name}</h3>
                        <p className="text-sm text-gray-500 mb-4 line-clamp-2">{connector.description || "No description provided."}</p>

                        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                            <span className="text-xs text-gray-400">v{connector.version}</span>
                            <div className="flex items-center gap-3">
                                <Link to={`/connectors/${connector.connector_id}`} className="text-sm font-medium text-indigo-600 hover:text-indigo-700">
                                    Configure
                                </Link>
                                <button
                                    onClick={() => handleDelete(connector.connector_id, connector.name)}
                                    className="text-gray-400 hover:text-red-600 transition-colors"
                                    title="Delete Connector"
                                >
                                    <Trash2 size={18} />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}

                {connectors.length === 0 && (
                    <div className="col-span-full text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-300">
                        <p className="text-gray-500 mb-2">No connectors found.</p>
                        <Link to="/upload" className="text-indigo-600 font-medium hover:underline">Upload your first OpenAPI spec</Link>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
