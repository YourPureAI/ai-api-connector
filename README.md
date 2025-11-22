# AI API Connector

<div align="center">

![AI API Connector](https://img.shields.io/badge/AI-API%20Connector-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=for-the-badge&logo=fastapi)

**Transform any API into a conversational AI assistant. Just upload an OpenAPI spec and start asking questions in plain English.**

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Documentation](#documentation) • [Use Cases](#use-cases)

</div>

---

## 💡 What is AI API Connector?

Imagine being able to interact with **any API** using natural language, without writing a single line of code. That's exactly what AI API Connector does.

**The Problem:** Modern applications rely on dozens of APIs, each with complex documentation, authentication schemes, and parameter requirements. Developers spend countless hours reading docs, crafting requests, and debugging responses.

**The Solution:** AI API Connector acts as an intelligent middleware that:
- 📚 **Understands** your APIs by analyzing OpenAPI specifications
- 🧠 **Translates** natural language queries into precise API calls
- 🔐 **Manages** authentication and credentials securely
- ⚡ **Executes** requests and formats responses intelligently

### Real-World Example

Instead of this:
```bash
curl -X GET "https://api.example.com/v2/users/12345" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

Just ask:
```
"Show me details for user 12345"
```

The AI figures out the endpoint, authentication, and parameters automatically.

---

## 🎯 Why AI API Connector?

### For Developers
- ⏱️ **Save Time:** No more reading API documentation for simple queries
- 🔄 **Rapid Prototyping:** Test API endpoints conversationally before writing code
- 🧪 **Easy Testing:** Validate API behavior with natural language commands
- 📖 **Living Documentation:** Your APIs become self-documenting through AI

### For Teams
- 🤝 **Democratize API Access:** Non-technical team members can query APIs
- 🔒 **Centralized Security:** Manage all API credentials in one secure place
- 📊 **API Discovery:** Quickly explore what your connected services can do
- 🌐 **Universal Interface:** One chat interface for all your APIs

### For Businesses
- 💰 **Reduce Integration Costs:** Faster API integration and testing
- 🚀 **Accelerate Development:** Developers spend less time on boilerplate
- 🔐 **Enhanced Security:** Encrypted credential storage and controlled access
- 📈 **Scalable Architecture:** Add unlimited APIs without complexity

</div>

---

## 🌟 Features

### Core Capabilities

- **🔌 API Connector Management**
  - Upload OpenAPI specifications (JSON/YAML)
  - Automatic parsing and vectorization
  - Secure credential storage with AES-256 encryption
  - Add individual functions to existing connectors

- **🤖 AI-Powered Query Interface**
  - Natural language to API call translation
  - Automatic parameter extraction
  - Support for multiple LLM providers (OpenAI, Anthropic, Google Gemini)
  - Intelligent function matching via vector search

- **🔍 Vector Database Integration**
  - ChromaDB for semantic search
  - Configurable embedding models
  - Per-function granular embeddings
  - Fast and accurate function discovery

- **🔐 Security & Privacy**
  - Encrypted API key storage
  - Local vault for sensitive data
  - No external data transmission (except to configured LLMs)
  - User-controlled API configurations

### User Interface

- **📊 Dashboard**
  - View all connected APIs
  - Monitor connector status
  - Quick access to configuration

- **⚙️ Configuration**
  - LLM provider selection
  - Embedding model configuration
  - API key management

- **💬 Test Chat**
  - Interactive AI assistant
  - Real-time API execution
  - Visual feedback on API calls

---

## 🚀 Quick Start

Get up and running in 3 simple commands:

```bash
# 1. Clone the repository
git clone https://github.com/YourPureAI/ai-api-connector.git
cd ai-api-connector

# 2. Install all components
python install.py

# 3. Start the application
python start.py
```

**That's it!** Open http://localhost:5173 in your browser.

---

## 📋 Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

---

## 💻 Installation

### Automated Installation (Recommended)

The installation script handles everything automatically:

```bash
python install.py
```

This will:
- ✅ Create Python virtual environment
- ✅ Install backend dependencies
- ✅ Install frontend dependencies
- ✅ Set up database
- ✅ Create necessary directories
- ✅ Configure environment

### Manual Installation

See [INSTALLATION.md](docs/INSTALLATION.md) for detailed manual installation instructions.

---

## 💼 Use Cases

### 1. **Customer Support Automation**
Connect your CRM and support ticket APIs. Support agents can query customer data, order history, and ticket status using natural language instead of switching between multiple systems.

**Example:** *"Show me all open tickets for customer john@example.com"*

### 2. **DevOps & Monitoring**
Integrate monitoring, logging, and infrastructure APIs. Query system health, deployment status, and logs conversationally.

**Example:** *"What's the CPU usage of production server-01?"*

### 3. **Data Analytics**
Connect to analytics and database APIs. Business analysts can extract insights without writing SQL or API calls.

**Example:** *"How many new users signed up last week?"*

### 4. **E-commerce Management**
Integrate inventory, orders, and shipping APIs. Manage your online store through conversational commands.

**Example:** *"List all products with less than 10 items in stock"*

### 5. **Internal Tool Integration**
Connect all your internal APIs (HR, finance, project management) into one unified interface.

**Example:** *"Who is on vacation next week from the engineering team?"*

### 6. **API Testing & Development**
Rapidly test API endpoints during development without writing test scripts.

**Example:** *"Create a test user with email test@example.com"*

---

## 🎯 Usage

### 1. Configure API Keys

After starting the application:

1. Navigate to **Settings** in the sidebar
2. Select your preferred LLM provider
3. Enter your API key
4. Choose embedding model
5. Click **Save Configuration**

### 2. Add a Connector

1. Click **New Connector**
2. Upload an OpenAPI specification (JSON or YAML)
3. Configure authentication (API key, OAuth, etc.)
4. Save the connector

### 3. Query with AI

1. Go to **Test Chat**
2. Ask questions in natural language
3. The AI will automatically:
   - Find the relevant API function
   - Extract parameters from your query
   - Execute the API call
   - Format and display results

### Example Queries

```
"Get pet with ID 5"
"List all available products"
"Create a new user with email test@example.com"
"What's the weather in London?"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  Dashboard │ Connector Detail │ Settings │ Test Chat   │
└────────────────────────┬────────────────────────────────┘
                         │
                    HTTP/REST
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │Connectors│  │  Query   │  │  Config  │             │
│  │   API    │  │   API    │  │   API    │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │              │                    │
│  ┌────▼─────────────▼──────────────▼─────┐             │
│  │         Services Layer                 │             │
│  │  • Ingestion  • Executor  • Vault     │             │
│  └────┬───────────────────────────────────┘             │
└───────┼─────────────────────────────────────────────────┘
        │
   ┌────▼────┐  ┌──────────┐  ┌──────────┐
   │ SQLite  │  │ ChromaDB │  │  Vault   │
   │   DB    │  │ (Vector) │  │(Encrypted)│
   └─────────┘  └──────────┘  └──────────┘
```

### Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- ChromaDB - Vector database
- Cryptography - Encryption library
- Pydantic - Data validation

**Frontend:**
- React 18 - UI library
- Vite - Build tool
- React Router - Navigation
- Axios - HTTP client
- TailwindCSS - Styling
- Lucide React - Icons

---

## 📁 Project Structure

```
ai-api-connector/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/      # API routes
│   │   ├── core/               # Configuration
│   │   ├── db/                 # Database models
│   │   └── services/           # Business logic
│   ├── data/                   # SQLite database
│   ├── vault/                  # Encrypted secrets
│   ├── chroma_db/              # Vector database
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API clients
│   │   └── App.jsx             # Main app
│   └── package.json            # Node dependencies
├── docs/
│   ├── INSTALLATION.md         # Installation guide
│   └── README.md               # This file
├── install.py                  # Installation script
├── start.py                    # Startup script
└── .gitignore                  # Git ignore rules
```

---

## 🔧 Configuration

### Environment Variables

Edit `backend/.env`:

```env
# Database
DATABASE_URL=sqlite:///./data/connector.db

# Security
SECRET_KEY=your-secret-key-here

# Paths
VAULT_PATH=./vault
CHROMA_DB_PATH=./chroma_db

# API
API_V1_STR=/api/v1
PROJECT_NAME=AI API Connector
```

### Supported LLM Providers

- **OpenAI** - GPT-4, GPT-3.5
- **Anthropic** - Claude 3.5, Claude 3
- **Google** - Gemini 2.5, Gemini 2.0

### Supported Embedding Models

- **OpenAI** - text-embedding-3-small, text-embedding-3-large
- **Google** - text-embedding-004
- **Local** - all-MiniLM-L6-v2, e5-large-v2

---

## 🛠️ Development

### Running in Development Mode

```bash
# Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

### API Documentation

Once the backend is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testing

### Test the AI Chat

1. Upload a sample OpenAPI spec (e.g., Petstore)
2. Configure authentication
3. Go to Test Chat
4. Try queries like:
   - "Get pet with ID 10"
   - "List all pets"

### Example OpenAPI Specs

You can test with public APIs:
- [Swagger Petstore](https://petstore.swagger.io/v2/swagger.json)
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/)

---

## 🔒 Security

### Data Protection

- **API Keys:** Encrypted with AES-256
- **Secrets:** Stored in encrypted vault
- **Database:** Local SQLite (no cloud storage)
- **Encryption Key:** Stored locally in `.key` file

### Best Practices

- Never commit `.env` or `.key` files
- Use strong SECRET_KEY in production
- Rotate API keys regularly
- Use HTTPS in production
- Implement proper authentication for multi-user setups

---

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

**Virtual environment issues:**
```bash
cd backend
rm -rf venv
python -m venv venv
```

See [INSTALLATION.md](docs/INSTALLATION.md) for more troubleshooting tips.

---

## 🗺️ Roadmap

- [ ] Multi-user authentication
- [ ] Connector marketplace
- [ ] Advanced query builder
- [ ] API response caching
- [ ] Webhook support
- [ ] Docker deployment
- [ ] Cloud deployment guides

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- ChromaDB for vector database capabilities
- OpenAI, Anthropic, and Google for LLM APIs
- The open-source community

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [Installation Guide](docs/INSTALLATION.md)
- Review the API documentation at `/docs`

---

<div align="center">

**Made with ❤️ by YourPureAI**

[⬆ Back to Top](#ai-api-connector)

</div>
