import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/Upload';
import ConnectorDetail from './pages/ConnectorDetail';

import Configuration from './pages/Configuration';
import TestChat from './pages/TestChat';

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/upload" element={<UploadPage />} />
                    <Route path="/connectors/:id" element={<ConnectorDetail />} />
                    <Route path="/settings" element={<Configuration />} />
                    <Route path="/test-chat" element={<TestChat />} />
                </Routes>
            </Layout>
        </Router>
    );
}

export default App;
