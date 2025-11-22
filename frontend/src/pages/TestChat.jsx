import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Trash2, Loader, AlertCircle, CheckCircle } from 'lucide-react';
import { getTestApiKey, queryBackend, getConfig, callLLM } from '../services/chatService';

const TestChat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [apiKey, setApiKey] = useState(null);
    const [config, setConfig] = useState(null);
    const [error, setError] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        initializeChat();
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const initializeChat = async () => {
        try {
            const key = await getTestApiKey();
            const cfg = await getConfig();
            setApiKey(key);
            setConfig(cfg);

            // Add welcome message
            setMessages([{
                role: 'assistant',
                content: 'Hello! I\'m your AI assistant. I can help you access data through your configured connectors. Try asking me for information!',
                timestamp: new Date()
            }]);
        } catch (err) {
            setError('Failed to initialize chat. Please check your configuration.');
        }
    };

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage = {
            role: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);
        setError(null);

        try {
            // Fetch fresh configuration each time to ensure we have the latest settings
            const freshConfig = await getConfig();

            // Build conversation history for LLM
            const conversationHistory = messages.map(m => ({
                role: m.role,
                content: m.content
            }));
            conversationHistory.push({ role: 'user', content: input });

            // Call LLM with fresh config
            const llmResponse = await callLLM(conversationHistory, freshConfig);

            // Check if LLM needs external data
            let finalResponse = llmResponse;
            let apiCallInfo = null;

            // Try to extract JSON from the response
            // Handle cases where LLM wraps JSON in markdown code blocks or adds extra text
            let jsonMatch = null;

            // Try to find JSON in markdown code blocks first
            const codeBlockMatch = llmResponse.match(/```(?:json)?\s*(\{[\s\S]*?\})\s*```/);
            if (codeBlockMatch) {
                jsonMatch = codeBlockMatch[1];
            } else {
                // Try to find raw JSON object
                const rawJsonMatch = llmResponse.match(/\{[\s\S]*"need_external_data"[\s\S]*\}/);
                if (rawJsonMatch) {
                    jsonMatch = rawJsonMatch[0];
                }
            }

            if (jsonMatch) {
                try {
                    const parsed = JSON.parse(jsonMatch);
                    if (parsed.need_external_data) {
                        // LLM indicated it needs external data
                        const backendResponse = await queryBackend(parsed.query, apiKey);

                        if (backendResponse.success) {
                            // Add API call info for display
                            apiCallInfo = {
                                query: parsed.query,
                                matched: backendResponse.matched_function,
                                data: backendResponse.data
                            };

                            console.log('[CHAT] API call successful, formatting response with LLM...');
                            console.log('[CHAT] Data received:', backendResponse.data);

                            // Ask LLM to format the response with the data
                            const dataMessage = {
                                role: 'user',
                                content: `The external API returned this data: ${JSON.stringify(backendResponse.data, null, 2)}. Please format this information in a user-friendly, natural language way to answer my original question.`
                            };

                            try {
                                const formattedResponse = await callLLM([...conversationHistory, dataMessage], freshConfig);
                                console.log('[CHAT] LLM formatted response:', formattedResponse);
                                finalResponse = formattedResponse;
                            } catch (formatError) {
                                console.error('[CHAT] Error formatting response with LLM:', formatError);
                                // Fallback to showing raw data if LLM formatting fails
                                finalResponse = `I successfully retrieved the data:\n\n${JSON.stringify(backendResponse.data, null, 2)}`;
                            }
                        } else {
                            console.log('[CHAT] API call failed:', backendResponse.error);
                            finalResponse = `I tried to fetch that information, but encountered an error: ${backendResponse.error}`;
                            apiCallInfo = {
                                query: parsed.query,
                                matched: backendResponse.matched_function,
                                error: backendResponse.error
                            };
                        }
                    }
                } catch (e) {
                    console.error('Error parsing JSON from LLM response:', e);
                    // Not valid JSON, treat as regular response
                }
            }

            const assistantMessage = {
                role: 'assistant',
                content: finalResponse,
                timestamp: new Date(),
                apiCall: apiCallInfo
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (err) {
            console.error('Chat error:', err);
            const errorMsg = err.message || 'Failed to get response. Please check your LLM configuration.';
            setError(errorMsg);

            const errorMessage = {
                role: 'assistant',
                content: `Sorry, I encountered an error: ${errorMsg}`,
                timestamp: new Date(),
                isError: true
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleClear = () => {
        setMessages([{
            role: 'assistant',
            content: 'Chat history cleared. How can I help you?',
            timestamp: new Date()
        }]);
        setError(null);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-8rem)]">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">AI Test Chat</h2>
                    <p className="text-gray-500">Test your connectors with an AI assistant</p>
                </div>
                <button
                    onClick={handleClear}
                    className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-red-600 transition-colors"
                >
                    <Trash2 size={18} />
                    Clear History
                </button>
            </div>

            {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
                    <AlertCircle size={20} />
                    <span>{error}</span>
                </div>
            )}

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto bg-gray-50 rounded-xl p-6 space-y-4 mb-4">
                {messages.map((message, index) => (
                    <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[70%] ${message.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white text-gray-900'} rounded-lg p-4 shadow-sm`}>
                            <div className="flex items-start gap-2">
                                {message.role === 'assistant' && (
                                    <MessageCircle size={18} className="mt-1 flex-shrink-0" />
                                )}
                                <div className="flex-1">
                                    <p className="whitespace-pre-wrap">{message.content}</p>

                                    {/* API Call Info */}
                                    {message.apiCall && (
                                        <div className="mt-3 pt-3 border-t border-gray-200 text-sm">
                                            <div className="flex items-center gap-2 mb-2">
                                                {message.apiCall.error ? (
                                                    <AlertCircle size={14} className="text-red-500" />
                                                ) : (
                                                    <CheckCircle size={14} className="text-green-500" />
                                                )}
                                                <span className="font-medium text-gray-700">API Call Made</span>
                                            </div>
                                            {message.apiCall.matched && (
                                                <div className="text-gray-600 space-y-1">
                                                    <p><strong>Connector:</strong> {message.apiCall.matched.connector}</p>
                                                    <p><strong>Function:</strong> {message.apiCall.matched.operation}</p>
                                                    <p><strong>Endpoint:</strong> {message.apiCall.matched.method.toUpperCase()} {message.apiCall.matched.path}</p>
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    <p className="text-xs mt-2 opacity-70">
                                        {message.timestamp.toLocaleTimeString()}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white rounded-lg p-4 shadow-sm flex items-center gap-2">
                            <Loader className="animate-spin" size={18} />
                            <span className="text-gray-600">Thinking...</span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-4">
                <div className="flex gap-2">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask me anything..."
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
                        rows="2"
                        disabled={loading}
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                        className={`px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 ${loading || !input.trim()
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            : 'bg-indigo-600 text-white hover:bg-indigo-700'
                            }`}
                    >
                        <Send size={18} />
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default TestChat;
