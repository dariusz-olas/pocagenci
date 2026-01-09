import { useEffect, useRef, useState, useCallback } from 'react';
import type { ExecutionProgress } from '../types';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

interface UseWebSocketOptions {
  executionId: string;
  onProgress?: (progress: ExecutionProgress) => void;
  onError?: (error: Event) => void;
  autoReconnect?: boolean;
}

interface UseWebSocketReturn {
  isConnected: boolean;
  lastMessage: ExecutionProgress | null;
  connect: () => void;
  disconnect: () => void;
}

export function useWebSocket({
  executionId,
  onProgress,
  onError,
  autoReconnect = true,
}: UseWebSocketOptions): UseWebSocketReturn {
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<ExecutionProgress | null>(null);
  const reconnectTimeoutRef = useRef<number>();

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const ws = new WebSocket(`${WS_URL}/ws/executions/${executionId}`);

    ws.onopen = () => {
      setIsConnected(true);
      console.log(`WebSocket connected for execution ${executionId}`);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as ExecutionProgress;
        setLastMessage(data);
        onProgress?.(data);
      } catch (e) {
        // Handle ping/pong text messages
        if (event.data === 'ping') {
          ws.send('pong');
        }
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log(`WebSocket disconnected for execution ${executionId}`);

      // Auto-reconnect after 3 seconds
      if (autoReconnect) {
        reconnectTimeoutRef.current = window.setTimeout(() => {
          connect();
        }, 3000);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      onError?.(error);
    };

    wsRef.current = ws;
  }, [executionId, onProgress, onError, autoReconnect]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    wsRef.current?.close();
    wsRef.current = null;
  }, []);

  // Connect on mount, disconnect on unmount
  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    connect,
    disconnect,
  };
}
