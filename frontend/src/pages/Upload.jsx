import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Upload as UploadIcon, FileText, Check } from 'lucide-react';

const UploadPage = () => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        if (e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('/api/v1/connectors/upload', formData);

            if (response.data.status === 'SUCCESS') {
                navigate(`/connectors/${response.data.connector_id}`);
            }
        } catch (error) {
            console.error("Upload failed:", error);
            const errorMessage = error.response?.data?.detail || error.message || "Upload failed. Please check the file and try again.";
            alert(`Upload failed: ${errorMessage}`);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Add New Connector</h2>
                <p className="text-gray-500">Upload an OpenAPI 3.1 JSON or YAML file to define your connector.</p>
            </div>

            <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:bg-gray-50 transition-colors cursor-pointer relative">
                    <input
                        type="file"
                        accept=".json,.yaml,.yml"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div className="flex flex-col items-center pointer-events-none">
                        <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mb-4">
                            {file ? <FileText size={24} /> : <UploadIcon size={24} />}
                        </div>
                        {file ? (
                            <div>
                                <p className="font-medium text-gray-900">{file.name}</p>
                                <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
                            </div>
                        ) : (
                            <div>
                                <p className="font-medium text-gray-900">Click to upload or drag and drop</p>
                                <p className="text-sm text-gray-500">JSON or YAML (max 10MB)</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="mt-6 flex justify-end">
                    <button
                        onClick={handleUpload}
                        disabled={!file || uploading}
                        className={`flex items-center gap-2 px-6 py-2 rounded-lg text-white font-medium transition-colors ${!file || uploading ? 'bg-gray-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
                            }`}
                    >
                        {uploading ? 'Processing...' : 'Continue'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default UploadPage;
