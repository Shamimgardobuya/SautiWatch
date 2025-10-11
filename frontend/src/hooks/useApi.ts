import { useState, useCallback } from 'react';
import type { ApiError } from '../services/api';

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: any[]) => Promise<T | undefined>;
  reset: () => void;
}

/**
 * Custom hook for handling API calls with loading and error states
 * 
 * @example
 * const { data, loading, error, execute } = useApi(reportAPI.list);
 * 
 * useEffect(() => {
 *   execute();
 * }, []);
 */
export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<T>
): UseApiReturn<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(
    async (...args: any[]): Promise<T | undefined> => {
      try {
        setState({ data: null, loading: true, error: null });
        const result = await apiFunction(...args);
        setState({ data: result, loading: false, error: null });
        return result;
      } catch (err) {
        const apiError = err as ApiError;
        setState({
          data: null,
          loading: false,
          error: apiError.message || 'An unexpected error occurred',
        });
        return undefined;
      }
    },
    [apiFunction]
  );

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return {
    ...state,
    execute,
    reset,
  };
}
