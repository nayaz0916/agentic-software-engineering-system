"""
URL Shortener Service Implementation
Mandatory use case: "Build a scalable URL shortener service with APIs, persistence, and analytics."
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
import redis
import sqlite3
from datetime import datetime, timedelta
import hashlib
import random
import string
from collections import defaultdict


app = FastAPI(title="URL Shortener Service", version="1.0.0")


# Models
class URLRequest(BaseModel):
    url: HttpUrl
    custom_alias: Optional[str] = None
    ttl_seconds: Optional[int] = None


class URLResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    expires_at: Optional[datetime]
    click_count: int


class AnalyticsResponse(BaseModel):
    short_code: str
    total_clicks: int
    last_clicked: Optional[datetime]
    clicks_by_day: dict


# Database setup
def get_db():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            click_count INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT NOT NULL,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            referrer TEXT,
            user_agent TEXT
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_code ON analytics(short_code)')
    
    conn.commit()
    conn.close()


# Redis cache
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# Helper functions
def generate_short_code(length: int = 6) -> str:
    """Generate a random short code."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def cache_url(short_code: str, original_url: str, ttl: Optional[int] = None):
    """Cache URL in Redis."""
    if ttl:
        redis_client.setex(f"url:{short_code}", ttl, original_url)
    else:
        redis_client.set(f"url:{short_code}", original_url)


def get_cached_url(short_code: str) -> Optional[str]:
    """Get URL from cache."""
    return redis_client.get(f"url:{short_code}")


# API Endpoints
@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    """Create a shortened URL."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Generate or use custom short code
    short_code = request.custom_alias or generate_short_code()
    
    # Check if short code already exists
    cursor.execute('SELECT id FROM urls WHERE short_code = ?', (short_code,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Short code already exists")
    
    # Calculate expiration
    expires_at = None
    if request.ttl_seconds:
        expires_at = datetime.now() + timedelta(seconds=request.ttl_seconds)
    
    # Store in database
    cursor.execute('''
        INSERT INTO urls (short_code, original_url, expires_at)
        VALUES (?, ?, ?)
    ''', (short_code, str(request.url), expires_at))
    
    conn.commit()
    
    # Cache in Redis
    cache_url(short_code, str(request.url), request.ttl_seconds)
    
    # Get created URL
    cursor.execute('SELECT * FROM urls WHERE short_code = ?', (short_code,))
    row = cursor.fetchone()
    conn.close()
    
    return URLResponse(
        short_code=row['short_code'],
        original_url=row['original_url'],
        created_at=row['created_at'],
        expires_at=row['expires_at'],
        click_count=row['click_count']
    )


@app.get("/{short_code}")
def redirect(short_code: str):
    """Redirect to original URL."""
    # Check cache first
    cached_url = get_cached_url(short_code)
    if cached_url:
        _record_click(short_code)
        return RedirectResponse(url=cached_url)
    
    # Check database
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT original_url, expires_at FROM urls 
        WHERE short_code = ?
    ''', (short_code,))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Check expiration
    if row['expires_at'] and datetime.now() > datetime.fromisoformat(row['expires_at']):
        conn.close()
        raise HTTPException(status_code=410, detail="URL has expired")
    
    original_url = row['original_url']
    
    # Update click count
    cursor.execute('''
        UPDATE urls SET click_count = click_count + 1 
        WHERE short_code = ?
    ''', (short_code,))
    
    conn.commit()
    conn.close()
    
    # Record analytics
    _record_click(short_code)
    
    return RedirectResponse(url=original_url)


def _record_click(short_code: str):
    """Record click analytics."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO analytics (short_code)
        VALUES (?)
    ''', (short_code,))
    
    conn.commit()
    conn.close()


@app.get("/analytics/{short_code}", response_model=AnalyticsResponse)
def get_analytics(short_code: str):
    """Get analytics for a short code."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get URL info
    cursor.execute('''
        SELECT click_count FROM urls WHERE short_code = ?
    ''', (short_code,))
    
    url_row = cursor.fetchone()
    if not url_row:
        conn.close()
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Get analytics
    cursor.execute('''
        SELECT clicked_at FROM analytics 
        WHERE short_code = ?
        ORDER BY clicked_at DESC
    ''', (short_code,))
    
    analytics_rows = cursor.fetchall()
    conn.close()
    
    # Calculate clicks by day
    clicks_by_day = defaultdict(int)
    last_clicked = None
    
    for row in analytics_rows:
        clicked_at = datetime.fromisoformat(row['clicked_at'])
        day_key = clicked_at.strftime('%Y-%m-%d')
        clicks_by_day[day_key] += 1
        if not last_clicked or clicked_at > last_clicked:
            last_clicked = clicked_at
    
    return AnalyticsResponse(
        short_code=short_code,
        total_clicks=url_row['click_count'],
        last_clicked=last_clicked,
        clicks_by_day=dict(clicks_by_day)
    )


@app.delete("/{short_code}")
def delete_url(short_code: str):
    """Delete a shortened URL."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM urls WHERE short_code = ?', (short_code,))
    cursor.execute('DELETE FROM analytics WHERE short_code = ?', (short_code,))
    
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    
    # Remove from cache
    redis_client.delete(f"url:{short_code}")
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {"message": "URL deleted successfully"}


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
