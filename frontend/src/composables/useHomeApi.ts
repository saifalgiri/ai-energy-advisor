// composables/useHomeApi.ts
import { ref } from 'vue'
import { HomeProfile, Recommendation, SSEMessage } from '@/types/home'
import { API_ENDPOINTS } from '@/config/homeApi'


export function useHomeApi() {
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const clearError = () => {
    error.value = null
  }

  // ------------------------------
  // CREATE HOME
  // ------------------------------
  const createHome = async (home: HomeProfile): Promise<HomeProfile | null> => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(API_ENDPOINTS.homes, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(home),
      })

      if (!response.ok) throw new Error(`Failed to create home profile: ${response.statusText}`)
      const data = await response.json()
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create home profile'
      return null
    } finally {
      isLoading.value = false
    }
  }

  // ------------------------------
  // GET HOME
  // ------------------------------
  const getHome = async (id: string): Promise<HomeProfile | null> => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(API_ENDPOINTS.home(id))
      if (!response.ok) throw new Error(`Failed to get home profile: ${response.statusText}`)
      const data = await response.json()
      return data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to get home profile'
      return null
    } finally {
      isLoading.value = false
    }
  }

  // ------------------------------
  // GET ADVICE (SSE)
  // ------------------------------
 

  const getAdvice = async (
    homeId: string,
    onRecommendation: (recommendation: Recommendation) => void,
    onComplete: () => void,
    onError?: (error: string) => void
  ): Promise<void> => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(API_ENDPOINTS.advice(homeId), {
        method: 'POST',
        headers: { 
          'Accept': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to get advice: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body available');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          onComplete();
          break;
        }

        // Decode the chunk and add to buffer
        buffer += decoder.decode(value, { stream: true });

        // Split by newlines to get individual SSE messages
        const lines = buffer.split('\n');
        
        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        // Process each complete line
        for (const line of lines) {
          // SSE format: "data: {json}"
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim();
            
            // Skip empty data
            if (!data) continue;

            try {
              const message: SSEMessage = JSON.parse(data);

              // Handle different message types
              switch (message.type) {
                case 'connected':
                  console.log('Connected to SSE stream, home_id:', message.home_id);
                  break;

                case 'recommendation':
                  if (message.recommendation) {
                    onRecommendation(message.recommendation);
                  }
                  break;

                case 'complete':
                  console.log('Stream complete');
                  onComplete();
                  return;

                case 'error':
                  const errorMsg = message.error || 'Unknown error occurred';
                  console.error('SSE Error:', errorMsg);
                  if (onError) {
                    onError(errorMsg);
                  }
                  onComplete();
                  return;

                default:
                  console.warn('Unknown message type:', message.type);
              }
            } catch (parseError) {
              console.warn('Failed to parse SSE message:', data, parseError);
            }
          }
        }
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to get advice';
      console.error('Stream error:', errorMsg);
      if (onError) {
        onError(errorMsg);
      }
      onComplete();
    } finally {
      isLoading.value = false;
    }
  };


  return {
    isLoading,
    error,
    createHome,
    getHome,
    getAdvice,
    clearError,
  }
}
