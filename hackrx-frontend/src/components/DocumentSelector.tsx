'use client';

import React, { useState, useEffect } from 'react';
import { Check, FileText, Database, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { listDocuments, DocumentInfo } from '@/lib/api';

interface DocumentSelectorProps {
  selectedDocuments: number[];
  onSelectionChange: (documentIds: number[]) => void;
  className?: string;
}

export default function DocumentSelector({ 
  selectedDocuments, 
  onSelectionChange, 
  className = '' 
}: DocumentSelectorProps) {
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      const docs = await listDocuments();
      setDocuments(docs);
      
      // If no documents selected and we have documents, select all by default
      if (selectedDocuments.length === 0 && docs.length > 0) {
        onSelectionChange(docs.map(doc => doc.id));
      }
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

  const handleSelectAll = () => {
    if (selectedDocuments.length === documents.length) {
      // Deselect all
      onSelectionChange([]);
    } else {
      // Select all
      onSelectionChange(documents.map(doc => doc.id));
    }
  };

  const handleDocumentToggle = (documentId: number) => {
    if (selectedDocuments.includes(documentId)) {
      onSelectionChange(selectedDocuments.filter(id => id !== documentId));
    } else {
      onSelectionChange([...selectedDocuments, documentId]);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
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
            Select Documents for Query
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-4">
            <RefreshCw className="h-5 w-5 animate-spin text-gray-400" />
            <span className="ml-2 text-gray-600">Loading documents...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (documents.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Select Documents for Query
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-4">
            <FileText className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">No documents available. Upload some documents first.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Database className="h-5 w-5" />
              Select Documents for Query
              <Badge variant="secondary">{selectedDocuments.length} of {documents.length} selected</Badge>
            </CardTitle>
            <CardDescription>
              Choose which documents to use as context for your questions
            </CardDescription>
          </div>
          <Button variant="outline" size="sm" onClick={handleSelectAll}>
            {selectedDocuments.length === documents.length ? 'Deselect All' : 'Select All'}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="text-red-600 text-sm mb-4">{error}</div>
        )}

        <div className="space-y-2 max-h-64 overflow-y-auto">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className={`flex items-center space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors ${
                selectedDocuments.includes(doc.id) ? 'bg-blue-50 border-blue-200' : ''
              }`}
              onClick={() => handleDocumentToggle(doc.id)}
            >
              <Checkbox
                checked={selectedDocuments.includes(doc.id)}
                onCheckedChange={() => handleDocumentToggle(doc.id)}
              />
              <FileText className="h-5 w-5 text-gray-400 flex-shrink-0" />
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
                  <span>{formatDate(doc.upload_date)}</span>
                  <span>{doc.chunks_count} chunks</span>
                </div>
              </div>
              {selectedDocuments.includes(doc.id) && (
                <Check className="h-4 w-4 text-blue-600" />
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
