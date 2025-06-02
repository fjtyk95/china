'use client';

import { useState, useEffect, useCallback } from 'react';

interface Job {
  job_id: string;
  status: string;
}

function useWebSocket(url: string, onMessage: (data: Job) => void) {
  useEffect(() => {
    const socket = new WebSocket(url);
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as Job;
        onMessage(data);
      } catch {
        // ignore parse errors
      }
    };
    return () => {
      socket.close();
    };
  }, [url, onMessage]);
}

export default function JobStatusList({ userId }: { userId: string }) {
  const [jobs, setJobs] = useState<Record<string, string>>({});

  const handleMessage = useCallback((data: Job) => {
    setJobs((prev) => ({ ...prev, [data.job_id]: data.status }));
  }, []);

  useWebSocket(
    typeof window === 'undefined'
      ? ''
      : `ws://${window.location.host}/ws/jobs/${userId}`,
    handleMessage,
  );

  const entries = Object.entries(jobs);

  return (
    <ul className="space-y-2">
      {entries.map(([id, status]) => (
        <li key={id} className="flex items-center space-x-2">
          <span className="font-mono text-sm">{id}</span>
          <span>{status}</span>
          {status === 'extracted' && (
            <button
              type="button"
              className="rounded bg-blue-500 px-2 py-1 text-white hover:bg-blue-600"
            >
              Download CSV
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}
