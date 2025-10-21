'use client';

import { useState } from 'react';
import { Brain, FileText, MessageSquare, Database } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DocumentUpload } from '@/components/DocumentUpload';
import { QueryInterface } from '@/components/QueryInterface';
import { StatusBar } from '@/components/StatusBar';
import DocumentManager from '@/components/DocumentManager';

interface UploadedFile {
  id: string;
  name: string;
}

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  const handleUploadSuccess = (fileId: string, fileName: string) => {
    setUploadedFiles(prev => [...prev, { id: fileId, name: fileName }]);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl text-white">
              <Brain className="h-8 w-8" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              LLM Query Retrieval System
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload documents and ask intelligent questions. Powered by AI for insurance, legal, HR, and compliance domains.
          </p>
        </div>

        {/* Status Bar */}
        <StatusBar />

        {/* Main Content */}
        <Tabs defaultValue="upload" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Upload
            </TabsTrigger>
            <TabsTrigger value="manage" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              Manage
            </TabsTrigger>
            <TabsTrigger value="query" className="flex items-center gap-2">
              <MessageSquare className="h-4 w-4" />
              Query
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="space-y-6">
            <DocumentUpload onUploadSuccess={handleUploadSuccess} />
            
            {uploadedFiles.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="font-medium text-green-800 mb-2">Ready for Queries!</h3>
                <p className="text-sm text-green-700">
                  You have {uploadedFiles.length} document{uploadedFiles.length !== 1 ? 's' : ''} uploaded. 
                  Switch to the Manage tab to view all documents or Query tab to start asking questions.
                </p>
              </div>
            )}
          </TabsContent>

          <TabsContent value="manage" className="space-y-6">
            <DocumentManager onDocumentDeleted={() => setUploadedFiles([])} />
          </TabsContent>

          <TabsContent value="query" className="space-y-6">
            <QueryInterface uploadedFiles={uploadedFiles} />
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <footer className="mt-16 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>
            Built with Next.js, FastAPI, PostgreSQL, and OpenAI • 
            <span className="font-medium"> Team BajajPaglu</span>
          </p>
          <p className="mt-2">
            Hackathon Project - LLM-Powered Intelligent Query-Retrieval System
          </p>
        </footer>
      </div>
    </main>
  );
}