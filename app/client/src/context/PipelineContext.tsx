"use client";

import React, { createContext, useContext, useState, ReactNode, useMemo, useEffect } from "react";

export interface Pipeline {
  pipeline_id: number;
  user_id: string;
  created_at: Date;
  updated_at: Date;
  selection: boolean;
  training?: boolean | null;
  inferencing?: boolean | null;
  infra: boolean;
  pipeline_desc?: string | null;
  pipeline_name?: string | null;
}

interface PipelineContextProps {
  pipelines: Pipeline[];
  loading: boolean;
  handleLoading: (val: boolean) => void;
  error: any;
  newPipelineLoading: boolean;
  createNewPipeline: () => Promise<void>;
}

const PipelineContext = createContext<PipelineContextProps | undefined>(undefined);

export const PipelineProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [newPipelineLoading, setNewPipelineLoading] = useState<boolean>(false);
  const [error, setError] = useState<any>(null);
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);

  const handleLoading = (val:boolean) => setLoading(val);

  const createNewPipeline = async () => {
    setNewPipelineLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/pipeline/create');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();

      const pipelineId = result.pipeline_id;

      const url = `/pages/mlpal/project/${pipelineId}/dumbledore`;
      window.open(url, '_blank');

      setPipelines([result, ...pipelines]);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setNewPipelineLoading(false);
    }
  };

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/pipeline/get-all');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      setPipelines(result);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [])

 const value = useMemo(() => ({
    loading,
    handleLoading,
    pipelines,
    error,
    createNewPipeline,
    newPipelineLoading
  }), [loading, handleLoading, pipelines, error, newPipelineLoading]);

  return (
    <PipelineContext.Provider value={value}>
      {children}
    </PipelineContext.Provider>
  );
};

export const usePipelineContext = () => {
  const context = useContext(PipelineContext);
  if (context === undefined) {
    throw new Error("usePipelineContext must be used within a PipelineProvider");
  }
  return context;
};
