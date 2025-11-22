import axios from 'axios';

// Get the test API key from backend
export const getTestApiKey = async () => {
    try {
        const response = await axios.get('/api/v1/query/test-key');
        return response.data.api_key;
    } catch (error) {
        console.error('Error fetching test API key:', error);
        return null;
    }
};

// Query our backend for data through connectors
export const queryBackend = async (query, apiKey) => {
    try {
        const response = await axios.post(
            '/api/v1/query/query',
            { query },
            {
                headers: {
                    'X-API-Key': apiKey
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error querying backend:', error);
        throw error;
    }
};

// Get configuration to determine which LLM to use
export const getConfig = async () => {
    try {
        const response = await axios.get('/api/v1/config/');
        return response.data;
    } catch (error) {
        console.error('Error fetching config:', error);
        return null;
    }
};

// Call the configured LLM
export const callLLM = async (messages, config) => {
    if (!config) {
        throw new Error('Configuration not loaded. Please configure your LLM settings first.');
    }

    const provider = config?.agentProvider || 'openai';
    const model = config?.agentModel || 'gpt-4';

    // Validate API key exists
    let apiKey;
    if (provider === 'openai') {
        apiKey = config.openaiApiKey;
        if (!apiKey) {
            throw new Error('OpenAI API key not configured. Please add it in Settings.');
        }
    } else if (provider === 'anthropic') {
        apiKey = config.anthropicApiKey;
        if (!apiKey) {
            throw new Error('Anthropic API key not configured. Please add it in Settings.');
        }
    } else if (provider === 'google') {
        apiKey = config.googleApiKey;
        if (!apiKey) {
            throw new Error('Google API key not configured. Please add it in Settings.');
        }
    }

    // System prompt for the test chatbot
    const systemPrompt = `You are a helpful AI assistant. When a user asks for information that you don't have direct access to (like weather data, calendar events, or other external data), you should recognize this and indicate that you need to fetch this data from an external source.

When you need external data, respond with a JSON object in this format:
{
  "need_external_data": true,
  "query": "natural language description of what data is needed"
}

Otherwise, respond normally to the user's question.`;

    const fullMessages = [
        { role: 'system', content: systemPrompt },
        ...messages
    ];

    if (provider === 'openai') {
        return await callOpenAI(fullMessages, model, apiKey);
    } else if (provider === 'anthropic') {
        return await callAnthropic(fullMessages, model, apiKey);
    } else if (provider === 'google') {
        return await callGoogle(fullMessages, model, apiKey);
    }

    throw new Error('Unsupported LLM provider');
};

// OpenAI API call
const callOpenAI = async (messages, model, apiKey) => {
    try {
        const response = await axios.post(
            'https://api.openai.com/v1/chat/completions',
            {
                model: model,
                messages: messages
            },
            {
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        return response.data.choices[0].message.content;
    } catch (error) {
        console.error('OpenAI API error:', error);
        console.error('Error details:', error.response?.data);
        throw new Error(`OpenAI API error: ${error.response?.data?.error?.message || error.message}`);
    }
};

// Anthropic API call
const callAnthropic = async (messages, model, apiKey) => {
    try {
        // Extract system message
        const systemMessage = messages.find(m => m.role === 'system')?.content || '';
        const userMessages = messages.filter(m => m.role !== 'system');

        const response = await axios.post(
            'https://api.anthropic.com/v1/messages',
            {
                model: model,
                max_tokens: 1024,
                system: systemMessage,
                messages: userMessages
            },
            {
                headers: {
                    'x-api-key': apiKey,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                }
            }
        );
        return response.data.content[0].text;
    } catch (error) {
        console.error('Anthropic API error:', error);
        console.error('Error details:', error.response?.data);
        throw new Error(`Anthropic API error: ${error.response?.data?.error?.message || error.message}`);
    }
};

// Google Gemini API call
const callGoogle = async (messages, model, apiKey) => {
    try {
        // Remove 'models/' prefix if present
        const modelName = model.startsWith('models/') ? model.substring(7) : model;

        // Convert messages to Gemini format
        const contents = messages
            .filter(m => m.role !== 'system')
            .map(m => ({
                role: m.role === 'assistant' ? 'model' : 'user',
                parts: [{ text: m.content }]
            }));

        const systemInstruction = messages.find(m => m.role === 'system')?.content;

        // Use correct Gemini API endpoint format
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;

        const requestBody = {
            contents: contents
        };

        // Add system instruction if present
        if (systemInstruction) {
            requestBody.systemInstruction = {
                parts: [{ text: systemInstruction }]
            };
        }

        const response = await axios.post(
            apiUrl,
            requestBody,
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        // Handle the response
        if (response.data.candidates && response.data.candidates.length > 0) {
            return response.data.candidates[0].content.parts[0].text;
        } else {
            throw new Error('No response from Gemini API');
        }
    } catch (error) {
        console.error('Google API error:', error);
        console.error('Error details:', error.response?.data);
        throw new Error(`Google API error: ${error.response?.data?.error?.message || error.message}`);
    }
};
