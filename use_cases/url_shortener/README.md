# URL Shortener Service

A scalable URL shortener service with APIs, persistence, and analytics.

## Features

- **URL Shortening**: Convert long URLs into short, memorable codes
- **Custom Aliases**: Create custom short codes
- **TTL Support**: Set expiration time for shortened URLs
- **Analytics**: Track click counts and click patterns
- **Caching**: Redis integration for performance
- **Persistence**: SQLite database for reliable storage

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│ FastAPI     │
│  Service    │
└──────┬──────┘
       │
       ├─────────────┬─────────────┐
       │             │             │
       ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Redis   │  │ SQLite   │  │Analytics │
│  Cache   │  │ Database │  │  Engine  │
└──────────┘  └──────────┘  └──────────┘
```

## API Endpoints

### POST /shorten
Create a shortened URL.

**Request:**
```json
{
  "url": "https://example.com/very/long/url",
  "custom_alias": "mylink",
  "ttl_seconds": 3600
}
```

**Response:**
```json
{
  "short_code": "mylink",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2024-01-01T00:00:00",
  "expires_at": "2024-01-01T01:00:00",
  "click_count": 0
}
```

### GET /{short_code}
Redirect to the original URL.

### GET /analytics/{short_code}
Get analytics for a short code.

**Response:**
```json
{
  "short_code": "mylink",
  "total_clicks": 42,
  "last_clicked": "2024-01-01T12:00:00",
  "clicks_by_day": {
    "2024-01-01": 42
  }
}
```

### DELETE /{short_code}
Delete a shortened URL.

### GET /health
Health check endpoint.

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn redis
```

2. Start Redis:
```bash
redis-server
```

3. Run the service:
```bash
python use_cases/url_shortener/implementation.py
```

## Testing

Run tests with pytest:
```bash
pytest use_cases/url_shortener/tests/test_url_shortener.py
```

## Trade-offs

**Design Decisions:**
- SQLite for simplicity and ease of deployment (can be upgraded to PostgreSQL for production)
- Redis for caching to improve read performance
- 6-character short codes for balance between uniqueness and memorability

**Scalability Considerations:**
- Add database read replicas for high availability
- Implement distributed caching with Redis Cluster
- Use consistent hashing for distributed URL generation
- Add rate limiting to prevent abuse

**Known Limitations:**
- Single SQLite instance (not horizontally scalable)
- No authentication/authorization (add for production)
- Basic analytics (can be enhanced with time-series database)
