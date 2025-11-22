import React, { useState, useEffect } from 'react';
import { Save, Server, Cpu, Key, Copy, RefreshCw, Eye, EyeOff } from 'lucide-react';
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
        embeddingModels: []
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
        agentProvider: 'openai',
        agentModel: 'gpt-4o',
        embeddingProvider: 'openai',
        embeddingModel: 'text-embedding-3-small',
        openaiApiKey: '',
        anthropicApiKey: '',
        googleApiKey: '',
        logLevel: 'INFO'
    });

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [apiKey, setApiKey] = useState('');
    const [apiKeyLoading, setApiKeyLoading] = useState(false);
    const [showApiKey, setShowApiKey] = useState(false);
    const [apiKeyCopied, setApiKeyCopied] = useState(false);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const response = await axios.get('/api/v1/config/');
                if (response.data) {
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

    useEffect(() => {
        fetchApiKey();
    }, []);

    const fetchApiKey = async () => {
        setApiKeyLoading(true);
        try {
            const response = await axios.get('/api/v1/config/api-key');
            setApiKey(response.data.api_key);
        } catch (error) {
            console.error('Error fetching API key:', error);
        } finally {
            setApiKeyLoading(false);
        }
    };

    const handleRegenerateApiKey = async () => {
        if (!confirm('Are you sure you want to regenerate the API key? The old key will stop working.')) {
            return;
        }

        setApiKeyLoading(true);
        try {
            const response = await axios.post('/api/v1/config/api-key/regenerate');
            setApiKey(response.data.api_key);
            setShowApiKey(true);
            alert('New API key generated successfully!');
        } catch (error) {
            console.error('Error regenerating API key:', error);
            alert('Failed to regenerate API key');
        } finally {
            setApiKeyLoading(false);
        }
    };

    const handleCopyApiKey = () => {
        navigator.clipboard.writeText(apiKey);
        setApiKeyCopied(true);
        setTimeout(() => setApiKeyCopied(false), 2000);
    };

    const handleProviderChange = (type, provider) => {
        setConfig(prev => ({
            ...prev,
            [`${type}Provider`]: provider,
            [`${type}Model`]: PROVIDERS[provider].models[0] || ''
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

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
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
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">LLM API Credentials</h3>
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

            {/* API Key Management Section */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
                    <div className="flex items-center gap-2 text-indigo-600">
                        <Key size={24} />
                        <h3 className="text-lg font-semibold text-gray-800">Application API Key</h3>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">API key for external chatbots and integrations</p>
                </div>

                <div className="p-6 space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Your API Key</label>
                        <div className="flex gap-2">
                            <div className="flex-1 relative">
                                <input
                                    type={showApiKey ? "text" : "password"}
                                    value={apiKey}
                                    readOnly
                                    className="w-full px-4 py-2 pr-12 border border-gray-300 rounded-lg bg-gray-50 font-mono text-sm"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowApiKey(!showApiKey)}
                                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-500 hover:text-gray-700"
                                >
                                    {showApiKey ? <EyeOff size={16} /> : <Eye size={16} />}
                                </button>
                            </div>
                            <button
                                type="button"
                                onClick={handleCopyApiKey}
                                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
                            >
                                <Copy size={16} />
                                {apiKeyCopied ? 'Copied!' : 'Copy'}
                            </button>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">
                            Use this key in the <code className="bg-gray-100 px-1 rounded">X-API-Key</code> header when making requests to the API
                        </p>
                    </div>

                    <div className="pt-2">
                        <button
                            type="button"
                            onClick={handleRegenerateApiKey}
                            disabled={apiKeyLoading}
                            className="flex items-center gap-2 px-4 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition-colors disabled:opacity-50"
                        >
                            <RefreshCw size={16} className={apiKeyLoading ? 'animate-spin' : ''} />
                            {apiKeyLoading ? 'Generating...' : 'Regenerate API Key'}
                        </button>
                        <p className="text-xs text-gray-500 mt-2">
                            ⚠️ Warning: Regenerating will invalidate the current key. Update all integrations with the new key.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Configuration;
