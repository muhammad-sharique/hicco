# HICCO - A Web Search Engine

**Note: This project is no longer maintained and may not work as expected. The code is being made public to share the logic and implementation details with the developer community.**

HICCO is a web search engine implementation that provides search results for web pages, images, videos, and news. It's built using Python Flask and includes web crawling capabilities, search result scraping, and a responsive web interface.

## Features

- Text search with results from Google
- Image search with results from DuckDuckGo
- Web crawler for indexing pages
- Dark/Light theme support
- Responsive design for mobile and desktop
- MongoDB integration for storing crawled data

## Tech Stack

- Python 3.x
- Flask
- MongoDB
- Selenium
- BeautifulSoup4
- Requests
- Bootstrap 5
- Vanilla JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hicco.git
cd hicco
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up WebDriver:
   - Download the appropriate WebDriver for your browser (Chrome/Firefox)
   - Place it in `web_selenium/drivers/[os]/` directory
   - Supported OS folders: windows/, linux/, macos/

5. Configure MongoDB:
   - Install MongoDB
   - Create a database named 'database'

6. Environment Configuration:
   - Create a `.env` file in the project root
   - Add the following configurations:
     ```
     FLASK_SECRET_KEY=your_secret_key_here
     MONGODB_URI=your_mongodb_uri_here
     ```

## Usage

1. Start the Flask application:
```bash
python app/app.py
```

2. Open a web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
hicco/
├── app/                    # Flask application
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   └── app.py            # Main Flask application
├── crawler/               # Web crawler implementation
├── mongo_module/         # MongoDB integration
├── scrapers/            # Search engine scrapers
├── web_selenium/        # Selenium WebDriver setup
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## Important Note

This project is no longer actively maintained and may have broken functionality due to changes in search engine APIs and web structures. The code is being shared publicly to help developers understand the implementation of:
- Web crawling mechanisms
- Search result scraping techniques
- Responsive web interface design
- Flask application structure
- MongoDB integration with Python

Feel free to use the code and logic as reference for your own projects. While the actual search functionality may not work, the implementation patterns and code structure can be valuable learning resources.

The project can be run using standard Flask setup and the requirements are listed in the requirements.txt file.

## Disclaimer

This project is for educational purposes only. Make sure to comply with the terms of service of search engines and websites you interact with.

## Known Issues

- Image search might be slow due to Selenium initialization
- Crawler may need proper rate limiting
- Search results might be limited due to search engine restrictions
