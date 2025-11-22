import React, { useState, useEffect } from 'react';
import { Save, Server, Cpu } from 'lucide-react';
import axios from 'axios';

const PROVIDERS = {
    openai: {
        name: 'OpenAI',
        models: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        embeddingModels: ['text-embedding-3-small', 'text-embedding-3-large', 'text-embedding-ada-002']
    },
    anthropic: {
        name: 'Anthropic',
        models: ['claude-3-5-sonnet-20240620', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'],
        embeddingModels: [] // Anthropic doesn't strictly have embedding models in the same way, usually use others
    },
    google: {
        name: 'Google Gemini',
        models: ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.5-flash-lite', 'gemini-2.0-flash', 'gemini-2.0-flash-lite'],
        embeddingModels: ['text-embedding-004']
    },
    local: {
        name: 'Local / Custom',
        models: ['llama-3-70b', 'mixtral-8x7b'],
        embeddingModels: ['all-MiniLM-L6-v2', 'e5-large-v2']
    }
};

const Configuration = () => {
    const [config, setConfig] = useState({
        // Agent LLM
        agentProvider: 'openai',
        agentModel: 'gpt-4o',

        // Embeddings
        embeddingProvider: 'openai',
        embeddingModel: 'text-embedding-3-small',

        // Keys
        openaiApiKey: '',
        anthropicApiKey: '',
        googleApiKey: '',

        // System
        logLevel: 'INFO'
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const response = await axios.get('/api/v1/config/');
                if (response.data) {
                    // Merge defaults with response to handle missing keys
                    setConfig(prev => ({ ...prev, ...response.data }));
                }
            } catch (error) {
                console.error("Error fetching config:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchConfig();
    }, []);

    // Reset model when provider changes
    const handleProviderChange = (type, provider) => {
        setConfig(prev => ({
            ...prev,
            [`${type}Provider`]: provider,
            [`${type}Model`]: PROVIDERS[provider].models[0] || '' // Default to first model
        }));
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setConfig(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setSaving(true);
        axios.post('/api/v1/config/', config)
            .then(() => {
                alert('Configuration saved securely.');
            })
            .catch(error => {
                console.error("Error saving config:", error);
                alert('Failed to save configuration.');
            })
            .finally(() => {
                setSaving(false);
            });
    };

    if (loading) return <div className="p-8 text-center">Loading configuration...</div>;

    return (
        <div className="max-w-4xl mx-auto">
            <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-800">System Configuration</h2>
                <p className="text-gray-600 mt-1">Configure AI models, providers, and system settings.</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <form onSubmit={handleSubmit} className="p-6 space-y-8">

                    {/* Agent LLM Configuration */}
                    <section>
                        <div className="flex items-center gap-2 mb-4 text-indigo-600">
                            <Cpu size={24} />
                            <h3 className="text-lg font-semibold text-gray-800">AI Agent Configuration</h3>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
                                <select
                                    name="agentProvider"
                                    value={config.agentProvider}
                                    onChange={(e) => handleProviderChange('agent', e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                >
                                    {Object.entries(PROVIDERS).map(([key, data]) => (
                                        <option key={key} value={key}>{data.name}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
                                <select
                                    name="agentModel"
                                    value={config.agentModel}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                >
                                    {PROVIDERS[config.agentProvider]?.models.map(model => (
                                        <option key={model} value={model}>{model}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </section>

                    <hr className="border-gray-100" />

                    {/* Embeddings Configuration */}
                    <section>
                        <div className="flex items-center gap-2 mb-4 text-indigo-600">
                            <Server size={24} />
                            <h3 className="text-lg font-semibold text-gray-800">Embeddings Configuration</h3>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
                                <select
                                    name="embeddingProvider"
                                    value={config.embeddingProvider}
                                    onChange={(e) => {
                                        const provider = e.target.value;
                                        setConfig(prev => ({
                                            ...prev,
                                            embeddingProvider: provider,
                                            embeddingModel: PROVIDERS[provider].embeddingModels[0] || ''
                                        }));
                                    }}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                >
                                    {Object.entries(PROVIDERS).filter(([_, data]) => data.embeddingModels.length > 0).map(([key, data]) => (
                                        <option key={key} value={key}>{data.name}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
                                <select
                                    name="embeddingModel"
                                    value={config.embeddingModel}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                >
                                    {PROVIDERS[config.embeddingProvider]?.embeddingModels.map(model => (
                                        <option key={model} value={model}>{model}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </section>

                    <hr className="border-gray-100" />

                    {/* API Keys */}
                    <section>
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">API Credentials</h3>
                        <div className="grid gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">OpenAI API Key</label>
                                <input
                                    type="password"
                                    name="openaiApiKey"
                                    value={config.openaiApiKey}
                                    onChange={handleChange}
                                    placeholder="sk-..."
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Anthropic API Key</label>
                                <input
                                    type="password"
                                    name="anthropicApiKey"
                                    value={config.anthropicApiKey}
                                    onChange={handleChange}
                                    placeholder="sk-ant-..."
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Google API Key</label>
                                <input
                                    type="password"
                                    name="googleApiKey"
                                    value={config.googleApiKey}
                                    onChange={handleChange}
                                    placeholder="AIza..."
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                                />
                            </div>
                        </div>
                    </section>

                    <div className="pt-4 flex justify-end">
                        <button
                            type="submit"
                            disabled={saving}
                            className="flex items-center gap-2 px-6 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
                        >
                            <Save size={20} />
                            <span>{saving ? 'Saving...' : 'Save Configuration'}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Configuration;
