'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { uploadDocument } from '@/lib/api';

interface UploadedFile {
  file: File;
  status: 'uploading' | 'success' | 'error';
  progress: number;
  id?: string;
  error?: string;
}

interface DocumentUploadProps {
  onUploadSuccess?: (fileId: string, fileName: string) => void;
}

export function DocumentUpload({ onUploadSuccess }: DocumentUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      status: 'uploading' as const,
      progress: 0,
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);

    // Upload files
    newFiles.forEach(async (fileItem, index) => {
      try {
        // Simulate progress
        const progressInterval = setInterval(() => {
          setUploadedFiles(prev => 
            prev.map(f => 
              f.file === fileItem.file 
                ? { ...f, progress: Math.min(f.progress + 10, 90) }
                : f
            )
          );
        }, 200);

        const response = await uploadDocument(fileItem.file);
        
        clearInterval(progressInterval);
        
        setUploadedFiles(prev => 
          prev.map(f => 
            f.file === fileItem.file 
              ? { ...f, status: 'success', progress: 100, id: response.document_id }
              : f
          )
        );

        onUploadSuccess?.(response.document_id, response.filename);
      } catch (error) {
        setUploadedFiles(prev => 
          prev.map(f => 
            f.file === fileItem.file 
              ? { 
                  ...f, 
                  status: 'error', 
                  progress: 0, 
                  error: error instanceof Error ? error.message : 'Upload failed' 
                }
              : f
          )
        );
      }
    });
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'message/rfc822': ['.eml'],
      'text/plain': ['.txt'],
    },
    multiple: true,
  });

  const removeFile = (fileToRemove: File) => {
    setUploadedFiles(prev => prev.filter(f => f.file !== fileToRemove));
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Document Upload
        </CardTitle>
        <CardDescription>
          Upload PDF, DOCX, EML, or TXT files for processing
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive 
              ? 'border-primary bg-primary/5' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          {isDragActive ? (
            <p>Drop the files here...</p>
          ) : (
            <div>
              <p className="text-lg font-medium">Drag & drop files here</p>
              <p className="text-sm text-gray-500 mt-2">or click to select files</p>
              <Button variant="outline" className="mt-4">
                Browse Files
              </Button>
            </div>
          )}
        </div>

        {uploadedFiles.length > 0 && (
          <div className="space-y-3">
            <h3 className="font-medium">Uploaded Files</h3>
            {uploadedFiles.map((fileItem, index) => (
              <div key={index} className="border rounded-lg p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <File className="h-4 w-4" />
                    <span className="text-sm font-medium">{fileItem.file.name}</span>
                    <Badge variant="outline" className="text-xs">
                      {(fileItem.file.size / 1024 / 1024).toFixed(2)} MB
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    {fileItem.status === 'uploading' && (
                      <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
                    )}
                    {fileItem.status === 'success' && (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    )}
                    {fileItem.status === 'error' && (
                      <XCircle className="h-4 w-4 text-red-500" />
                    )}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeFile(fileItem.file)}
                    >
                      Remove
                    </Button>
                  </div>
                </div>

                {fileItem.status === 'uploading' && (
                  <Progress value={fileItem.progress} className="h-2" />
                )}

                {fileItem.status === 'error' && fileItem.error && (
                  <Alert variant="destructive">
                    <XCircle className="h-4 w-4" />
                    <AlertDescription>{fileItem.error}</AlertDescription>
                  </Alert>
                )}

                {fileItem.status === 'success' && (
                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertDescription>
                      File uploaded successfully! Document ID: {fileItem.id}
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
