# SautiWatch Developer Guide

## Quick Start

### 1. Environment Setup
```bash
# Create .env file
cp .env.example .env

# Update with your Django backend URL
VITE_API_URL=http://localhost:8000/api
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

## Project Structure

```
/
├── services/
│   └── api.ts              # API service layer with all endpoints
├── hooks/
│   └── useApi.ts           # Reusable hook for API calls
├── components/
│   ├── ReportForm.tsx      # Anonymous case reporting
│   ├── SupportDirectory.tsx # Support services listing
│   ├── AdminDashboard.tsx  # Case management for authorities
│   ├── Testimonials.tsx    # Survivor testimonials
│   ├── HomePage.tsx        # Landing page
│   ├── QuickExit.tsx       # Safety feature component
│   └── ui/                 # ShadcN UI components
├── App.tsx                 # Main app with routing
└── styles/
    └── globals.css         # Tailwind v4 configuration
```

## API Service Layer

### Location: `/services/api.ts`

The API service provides a centralized way to interact with the Django backend.

#### Configuration
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

#### Available APIs

##### Report API
```typescript
import { reportAPI } from '../services/api';

// Create a report
await reportAPI.create({
  incidentType: 'physical',
  location: 'Nairobi',
  urgency: 'high',
  date: '2025-10-10',
  description: 'Optional description',
  abuserInfo: 'Optional info',
});

// List all reports (admin)
const reports = await reportAPI.list();

// Update report status
await reportAPI.updateStatus('report-id', 'verified', 'Case notes');
```

##### Support Services API
```typescript
import { supportAPI } from '../services/api';

// List all services
const services = await supportAPI.list();

// Search services
const results = await supportAPI.list('Nairobi');
```

##### Testimonials API
```typescript
import { testimonialsAPI } from '../services/api';

// List all testimonials
const testimonials = await testimonialsAPI.list();
```

### Error Handling

All API calls return typed errors:
```typescript
try {
  await reportAPI.create(data);
} catch (err) {
  const apiError = err as ApiError;
  console.log(apiError.message);  // User-friendly message
  console.log(apiError.status);   // HTTP status code
  console.log(apiError.details);  // Additional error details
}
```

## Using the useApi Hook

The `useApi` hook simplifies API state management:

```typescript
import { useApi } from '../hooks/useApi';
import { reportAPI } from '../services/api';

function MyComponent() {
  const { data, loading, error, execute } = useApi(reportAPI.list);

  useEffect(() => {
    execute();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return <div>{/* Render data */}</div>;
}
```

## Component Patterns

### Loading States
All data-fetching components implement loading states using Skeleton components:

```typescript
{loading && (
  <div>
    <Skeleton className="h-6 w-3/4 mb-2" />
    <Skeleton className="h-4 w-1/2" />
  </div>
)}
```

### Error States
Error handling with retry functionality:

```typescript
{error && (
  <Alert variant="destructive">
    <AlertCircle className="h-4 w-4" />
    <AlertDescription>
      {error}
      <Button onClick={loadData}>Try Again</Button>
    </AlertDescription>
  </Alert>
)}
```

### Success Notifications
Using toast notifications for user feedback:

```typescript
import { toast } from "sonner@2.0.3";

toast.success("Report status updated successfully");
toast.error("Failed to update report status");
```

## TypeScript Types

### Report Type
```typescript
interface Report {
  id: string;
  incidentType: string;
  location: string;
  urgency: string;
  date: string;
  description: string;
  abuserInfo: string;
  status: string;
  submittedAt: string;
  verifiedAt?: string;
  notes?: string;
}
```

### SupportService Type
```typescript
interface SupportService {
  id: number;
  name: string;
  type: string;
  location: string;
  phone: string;
  services: string[];
  hours: string;
  verified: boolean;
}
```

### Testimonial Type
```typescript
interface Testimonial {
  id: number;
  quote: string;
  location: string;
  type: string;
  year: string;
}
```

## Best Practices

### 1. Always Handle Errors
```typescript
// ✅ Good
try {
  const data = await api.create(formData);
  toast.success("Success!");
} catch (err) {
  toast.error((err as ApiError).message);
}

// ❌ Bad
const data = await api.create(formData);
```

### 2. Show Loading States
```typescript
// ✅ Good
const [loading, setLoading] = useState(false);

const handleSubmit = async () => {
  setLoading(true);
  try {
    await api.create(data);
  } finally {
    setLoading(false);
  }
};

// ❌ Bad - No loading state
const handleSubmit = async () => {
  await api.create(data);
};
```

### 3. Use TypeScript Types
```typescript
// ✅ Good
const [reports, setReports] = useState<Report[]>([]);

// ❌ Bad
const [reports, setReports] = useState([]);
```

### 4. Cleanup on Unmount
```typescript
// ✅ Good
useEffect(() => {
  let isMounted = true;
  
  const loadData = async () => {
    const data = await api.list();
    if (isMounted) {
      setData(data);
    }
  };
  
  loadData();
  
  return () => {
    isMounted = false;
  };
}, []);
```

## Testing API Integration

### 1. Mock API Responses
For testing without a backend, you can modify the API service:

```typescript
// services/api.ts - Add mock mode
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export const reportAPI = {
  create: async (data) => {
    if (USE_MOCK) {
      return { id: '123', ...data, status: 'pending' };
    }
    return fetchAPI('/reports/', { method: 'POST', body: JSON.stringify(data) });
  },
};
```

### 2. Use Network Tab
Monitor API calls in browser DevTools:
- Check request payloads
- Verify response data
- Debug errors

### 3. Backend Health Check
Add a health check endpoint:

```typescript
export const healthAPI = {
  check: async () => {
    return fetchAPI('/health/');
  },
};
```

## Common Issues & Solutions

### CORS Errors
**Problem**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**: Configure Django CORS settings
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

### Network Errors
**Problem**: "Network error. Please check your connection"

**Solution**: 
1. Verify Django backend is running
2. Check VITE_API_URL in .env
3. Verify API endpoint paths

### Type Errors
**Problem**: TypeScript type mismatches

**Solution**: Ensure Django serializers match TypeScript types
```python
# Django serializer field names must match TypeScript interface
class ReportSerializer(serializers.ModelSerializer):
    incidentType = serializers.CharField()  # Match TypeScript camelCase
```

## Contributing

### Adding a New API Endpoint

1. **Add to API Service** (`/services/api.ts`)
```typescript
export const newAPI = {
  list: async (): Promise<NewType[]> => {
    return fetchAPI<NewType[]>('/new-endpoint/');
  },
};
```

2. **Create Type**
```typescript
export interface NewType {
  id: number;
  name: string;
}
```

3. **Use in Component**
```typescript
import { newAPI } from '../services/api';

const { data, loading, error, execute } = useApi(newAPI.list);
```

4. **Update Documentation**
Add the new endpoint to API_INTEGRATION.md

## Performance Optimization

### 1. Caching
Consider implementing a cache layer for frequently accessed data:

```typescript
const cache = new Map();

export const supportAPI = {
  list: async () => {
    if (cache.has('services')) {
      return cache.get('services');
    }
    const data = await fetchAPI('/support-services/');
    cache.set('services', data);
    return data;
  },
};
```

### 2. Debouncing Search
For search functionality:

```typescript
import { debounce } from 'lodash';

const debouncedSearch = debounce(async (term: string) => {
  const results = await supportAPI.list(term);
  setResults(results);
}, 300);
```

### 3. Pagination
Implement pagination for large datasets:

```typescript
const [page, setPage] = useState(1);

const loadMore = async () => {
  const data = await reportAPI.list(`?page=${page}`);
  setReports([...reports, ...data]);
  setPage(page + 1);
};
```

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Implement CSRF protection
- [ ] Add rate limiting on backend
- [ ] Validate all inputs on backend
- [ ] Sanitize user-generated content
- [ ] Implement proper authentication for admin
- [ ] Use environment variables for sensitive data
- [ ] Enable CORS only for trusted domains
- [ ] Log security events
- [ ] Regular security audits

## Deployment

### Build for Production
```bash
npm run build
```

### Environment Variables
Set production environment variable:
```
VITE_API_URL=https://api.sautiwatch.org/api
```

### Vercel/Netlify
Add environment variable in hosting platform settings.

## Support

For issues or questions:
1. Check API_INTEGRATION.md
2. Review Django logs
3. Check browser console
4. Verify network requests in DevTools
