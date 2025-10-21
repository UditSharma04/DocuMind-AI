'use client';

import { useState } from 'react';
import { Send, MessageSquare, Bot, User, Loader2, FileText, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import { runQuery, QueryRequest } from '@/lib/api';
import DocumentSelector from './DocumentSelector';

interface QueryResult {
  id: string;
  question: string;
  answer: string;
  timestamp: Date;
  documentUrl?: string;
}

interface QueryInterfaceProps {
  uploadedFiles?: Array<{ id: string; name: string }>;
}

export function QueryInterface({ uploadedFiles = [] }: QueryInterfaceProps) {
  const [selectedDocuments, setSelectedDocuments] = useState<number[]>([]);
  const [questions, setQuestions] = useState<string[]>(['']);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<QueryResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  const addQuestion = () => {
    setQuestions([...questions, '']);
  };

  const updateQuestion = (index: number, value: string) => {
    const newQuestions = [...questions];
    newQuestions[index] = value;
    setQuestions(newQuestions);
  };

  const removeQuestion = (index: number) => {
    if (questions.length > 1) {
      setQuestions(questions.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = async () => {
    const validQuestions = questions.filter(q => q.trim());
    
    if (selectedDocuments.length === 0) {
      setError('Please select at least one document to use as context');
      return;
    }
    
    if (validQuestions.length === 0) {
      setError('Please add at least one question');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Use document IDs instead of URLs - backend will handle document lookup
      const request: QueryRequest = {
        documents: selectedDocuments.map(id => `document-${id}`),
        questions: validQuestions,
      };

      const response = await runQuery(request);
      
      const newResults: QueryResult[] = validQuestions.map((question, index) => ({
        id: `${Date.now()}-${index}`,
        question,
        answer: response.answers[index] || 'No answer provided',
        timestamp: new Date(),
        documentUrl: `${selectedDocuments.length} selected documents`,
      }));

      setResults(prev => [...newResults, ...prev]);
      
      // Reset form but keep document selection
      setQuestions(['']);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process query');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Document Selection */}
      <DocumentSelector 
        selectedDocuments={selectedDocuments}
        onSelectionChange={setSelectedDocuments}
      />

      {/* Query Input Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            Ask Questions About Your Documents
          </CardTitle>
          <CardDescription>
            Ask intelligent questions about your selected documents
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">

          {/* Questions */}
          <div className="space-y-3">
            <Label>Questions</Label>
            {questions.map((question, index) => (
              <div key={index} className="flex gap-2">
                <Textarea
                  placeholder={`Question ${index + 1}: e.g., "What is the grace period for premium payment?"`}
                  value={question}
                  onChange={(e) => updateQuestion(index, e.target.value)}
                  className="min-h-[60px]"
                />
                {questions.length > 1 && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => removeQuestion(index)}
                    className="shrink-0"
                  >
                    Remove
                  </Button>
                )}
              </div>
            ))}
            
            <div className="flex gap-2">
              <Button variant="outline" onClick={addQuestion} className="flex-1">
                Add Another Question
              </Button>
              <Button 
                onClick={handleSubmit} 
                disabled={isLoading}
                className="flex-1"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Ask Questions
                  </>
                )}
              </Button>
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Results */}
      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5" />
              Query Results
            </CardTitle>
            <CardDescription>
              AI-powered answers from your documents
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.map((result) => (
                <div key={result.id} className="border rounded-lg p-4 space-y-3">
                  <div className="flex items-start gap-3">
                    <User className="h-5 w-5 text-blue-500 mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <p className="font-medium text-sm text-gray-700">Question:</p>
                      <p className="mt-1">{result.question}</p>
                    </div>
                  </div>
                  
                  <Separator />
                  
                  <div className="flex items-start gap-3">
                    <Bot className="h-5 w-5 text-green-500 mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <p className="font-medium text-sm text-gray-700">Answer:</p>
                      <p className="mt-1 leading-relaxed">{result.answer}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-gray-500 mt-3 pt-2 border-t">
                    <span>Document: {result.documentUrl}</span>
                    <span>{result.timestamp.toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
