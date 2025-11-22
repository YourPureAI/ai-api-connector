import React from 'react';
import { Link } from 'react-router-dom';
import { LayoutDashboard, Upload, Settings, MessageCircle } from 'lucide-react';

const Layout = ({ children }) => {
    return (
        <div className="min-h-screen bg-gray-50 flex">
            {/* Sidebar */}
            <aside className="w-64 bg-white border-r border-gray-200">
                <div className="h-16 flex items-center px-6 border-b border-gray-200">
                    <span className="text-xl font-bold text-indigo-600">AI Connector</span>
                </div>
                <nav className="p-4 space-y-2">
                    <Link to="/" className="flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-lg transition-colors">
                        <LayoutDashboard size={20} />
                        <span>Dashboard</span>
                    </Link>
                    <Link to="/upload" className="flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-lg transition-colors">
                        <Upload size={20} />
                        <span>New Connector</span>
                    </Link>
                    <Link to="/test-chat" className="flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-lg transition-colors">
                        <MessageCircle size={20} />
                        <span>Test Chat</span>
                    </Link>
                    <div className="pt-4 mt-4 border-t border-gray-100">
                        <div className="px-4 py-2 text-xs font-semibold text-gray-400 uppercase">Settings</div>
                        <Link to="/settings" className="flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-lg transition-colors">
                            <Settings size={20} />
                            <span>Configuration</span>
                        </Link>
                    </div>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto">
                <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
                    <h1 className="text-lg font-semibold text-gray-800">Dashboard</h1>
                    <div className="flex items-center gap-4">
                        <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">
                            U
                        </div>
                    </div>
                </header>
                <div className="p-8">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
