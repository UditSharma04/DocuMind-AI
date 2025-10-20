'use client';

import { useEffect, useState } from 'react';
import { Activity, Database, Zap, AlertCircle, CheckCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { healthCheck, HealthResponse } from '@/lib/api';

export function StatusBar() {
  const [status, setStatus] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        setIsLoading(true);
        console.log('🔍 Checking backend health at:', process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
        const health = await healthCheck();
        console.log('✅ Health check success:', health);
        setStatus(health);
        setError(null);
      } catch (err) {
        console.error('❌ Health check failed:', err);
        setError('Backend unavailable');
        setStatus(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkHealth();
    
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="mb-6">
      <CardContent className="py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              <span className="text-sm font-medium">System Status</span>
            </div>
            
            {isLoading ? (
              <Badge variant="outline">Checking...</Badge>
            ) : error ? (
              <Badge variant="destructive" className="flex items-center gap-1">
                <AlertCircle className="h-3 w-3" />
                {error}
              </Badge>
            ) : status ? (
              <div className="flex items-center gap-3">
                <Badge variant="default" className="flex items-center gap-1">
                  <CheckCircle className="h-3 w-3" />
                  {status.service}
                </Badge>
                
                <div className="flex items-center gap-1 text-xs text-gray-600">
                  <Database className="h-3 w-3" />
                  DB: {status.database_enabled ? 'Connected' : 'Disabled'}
                </div>
                
                <div className="flex items-center gap-1 text-xs text-gray-600">
                  <Zap className="h-3 w-3" />
                  v{status.version}
                </div>
              </div>
            ) : null}
          </div>
          
          <div className="text-xs text-gray-500">
            Backend: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
