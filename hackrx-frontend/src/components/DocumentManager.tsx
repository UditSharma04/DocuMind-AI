'use client';

import React, { useState, useEffect } from 'react';
import { Trash2, FileText, Clock, Database, RefreshCw, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { listDocuments, deleteDocument, DocumentInfo } from '@/lib/api';

interface DocumentManagerProps {
  onDocumentDeleted?: () => void;
  className?: string;
}

export default function DocumentManager({ onDocumentDeleted, className = '' }: DocumentManagerProps) {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      const docs = await listDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error('Error fetching documents:', err);
      setError('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleDelete = async (documentId: number, filename: string) => {
    if (!window.confirm(`Are you sure you want to delete "${filename}"? This action cannot be undone.`)) {
      return;
    }

    try {
      setDeleting(documentId);
      setError(null);
      const result = await deleteDocument(documentId);
      
      // Remove from local state
      setDocuments(prev => prev.filter(doc => doc.id !== documentId));
      
      // Notify parent component
      onDocumentDeleted?.();
      
      console.log(`Document deleted: ${result.filename} (${result.chunks_deleted} chunks)`);
    } catch (err) {
      console.error('Error deleting document:', err);
      setError(`Failed to delete "${filename}"`);
    } finally {
      setDeleting(null);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getFileTypeColor = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case 'pdf': return 'bg-red-100 text-red-800';
      case 'docx':
      case 'doc': return 'bg-blue-100 text-blue-800';
      case 'txt': return 'bg-gray-100 text-gray-800';
      default: return 'bg-purple-100 text-purple-800';
    }
  };

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Document Library
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="h-6 w-6 animate-spin text-gray-400" />
            <span className="ml-2 text-gray-600">Loading documents...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Document Library
            <Badge variant="secondary">{documents.length}</Badge>
          </CardTitle>
          <Button variant="outline" size="sm" onClick={fetchDocuments}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert className="mb-4">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {documents.length === 0 ? (
          <div className="text-center py-8">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <h3 className="text-lg font-medium text-gray-900 mb-1">No documents uploaded</h3>
            <p className="text-gray-600">Upload a document to get started with RAG queries.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-3 flex-1">
                  <FileText className="h-8 w-8 text-gray-400" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {doc.filename}
                      </p>
                      <Badge className={getFileTypeColor(doc.file_type)}>
                        {doc.file_type.toUpperCase()}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {formatDate(doc.upload_date)}
                      </span>
                      <span>{doc.chunks_count} chunks</span>
                    </div>
                  </div>
                </div>
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(doc.id, doc.filename)}
                  disabled={deleting === doc.id}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  {deleting === doc.id ? (
                    <RefreshCw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </Button>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
