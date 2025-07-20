import { useState } from 'react'
import axios from 'axios';

const UrlShortenerForm = () => {
    const [longUrl, setLongUrl] = useState('');
    const [shortUrl, setShortUrl] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('/api/shorten', { url: longUrl });
        setShortUrl(response.data.short_url);
        setError('');
    } catch (err) {
        setError(err.response?.data?.error || 'Failed to shorten URL');
        setShortUrl('');
    }
    };

    return (
    <div className="url-shortener-container">
        <h2>URL Shortener</h2>
        <form onSubmit={handleSubmit}>
        <label htmlFor="Long_Url">Enter URL:</label>
        <input
            type="url"
            id="Long_Url"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            required
            placeholder="https://example.com"
        />
        <button type="submit">Shorten</button>
        </form>

        {error && <p className="error-message">{error}</p>}
        {shortUrl && (
        <div className="result">
            <p>Short URL: <a href={shortUrl} target="_blank" rel="noopener noreferrer">
            {shortUrl}
            </a></p>
        </div>
        )}
    </div>
    );
};

export default UrlShortenerForm;