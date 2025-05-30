#!/usr/bin/env python3
"""
WitnessOS Documentation Server

An enhanced documentation server with proper navigation, markdown rendering,
and improved user experience for the WitnessOS documentation.
"""

import os
import sys
import argparse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import mimetypes
import markdown
import json
from datetime import datetime

class WitnessOSDocHandler(SimpleHTTPRequestHandler):
    """Enhanced HTTP handler for WitnessOS documentation"""
    
    def __init__(self, *args, **kwargs):
        # Set up markdown processor
        self.md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code'])
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests with enhanced functionality"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Handle root path - serve custom homepage
        if path == '/' or path == '/index.html':
            self.serve_homepage()
            return
        
        # Handle markdown files - render as HTML
        if path.endswith('.md'):
            self.serve_markdown(path)
            return
        
        # Handle API documentation redirect
        if path == '/api' or path == '/api/':
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8001/docs')
            self.end_headers()
            return
        
        # Default file serving
        super().do_GET()
    
    def serve_homepage(self):
        """Serve custom WitnessOS homepage"""
        try:
            # Read README.md content
            readme_path = Path('README.md')
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                # Convert markdown to HTML
                readme_html = self.md.convert(readme_content)
            else:
                readme_html = "<p>README.md not found</p>"
            
            # Create enhanced homepage
            html_content = self.create_homepage_html(readme_html)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(html_content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error serving homepage: {str(e)}")
    
    def serve_markdown(self, path):
        """Serve markdown files as rendered HTML"""
        try:
            # Remove leading slash and resolve file path
            file_path = Path(path.lstrip('/'))
            
            if not file_path.exists():
                self.send_error(404, f"File not found: {path}")
                return
            
            # Read and convert markdown
            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_body = self.md.convert(md_content)
            
            # Create full HTML page
            html_content = self.create_markdown_html(html_body, file_path.name)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(html_content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error serving markdown: {str(e)}")
    
    def create_homepage_html(self, readme_html):
        """Create enhanced homepage HTML"""
        navigation = self.get_navigation_menu()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WitnessOS - Consciousness Operating System</title>
    <style>
        {self.get_css_styles()}
    </style>
</head>
<body>
    <header>
        <h1>🌟 WitnessOS Documentation</h1>
        <p>Consciousness debugging and reality navigation framework</p>
    </header>
    
    <nav class="main-nav">
        {navigation}
    </nav>
    
    <main>
        <div class="content">
            {readme_html}
        </div>
        
        <aside class="quick-links">
            <h3>🚀 Quick Start</h3>
            <ul>
                <li><a href="/GUIDES/INSTALLATION.md">Installation Guide</a></li>
                <li><a href="/GUIDES/PRIMER.md">Getting Started</a></li>
                <li><a href="/api">API Documentation</a></li>
                <li><a href="/ENGINES/README.md">Engines Overview</a></li>
            </ul>
            
            <h3>🔗 Live Services</h3>
            <ul>
                <li><a href="http://localhost:8001/docs" target="_blank">Simple API</a></li>
                <li><a href="http://localhost:8002/v1/docs" target="_blank">Production API</a></li>
                <li><a href="http://localhost:8003/agent/docs" target="_blank">Agent API</a></li>
            </ul>
        </aside>
    </main>
    
    <footer>
        <p>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | WitnessOS Documentation Server</p>
    </footer>
</body>
</html>"""
    
    def create_markdown_html(self, body_html, title):
        """Create HTML page for markdown content"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - WitnessOS</title>
    <style>
        {self.get_css_styles()}
    </style>
</head>
<body>
    <header>
        <h1><a href="/">🌟 WitnessOS</a></h1>
        <nav>
            <a href="/">Home</a> |
            <a href="/GUIDES/">Guides</a> |
            <a href="/MODULES/">Modules</a> |
            <a href="/ENGINES/">Engines</a> |
            <a href="/api">API</a>
        </nav>
    </header>
    
    <main>
        <div class="content">
            {body_html}
        </div>
    </main>
    
    <footer>
        <p><a href="/">← Back to Home</a> | WitnessOS Documentation</p>
    </footer>
</body>
</html>"""
    
    def get_navigation_menu(self):
        """Generate navigation menu from directory structure"""
        nav_items = []
        
        # Core sections
        sections = [
            ('CORE', 'Core Framework'),
            ('GUIDES', 'User Guides'),
            ('MODULES', 'System Modules'),
            ('ENGINES', 'Calculation Engines'),
            ('FOUNDATION', 'Foundation Documents'),
            ('ASSETS', 'Resources & Assets')
        ]
        
        for folder, title in sections:
            if Path(folder).exists():
                nav_items.append(f'<a href="/{folder}/">{title}</a>')
        
        return ' | '.join(nav_items)
    
    def get_css_styles(self):
        """Return CSS styles for documentation"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        header p { font-size: 1.2rem; opacity: 0.9; }
        
        .main-nav {
            background: #fff;
            padding: 1rem;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        
        .main-nav a {
            color: #667eea;
            text-decoration: none;
            margin: 0 1rem;
            font-weight: 500;
        }
        
        .main-nav a:hover { text-decoration: underline; }
        
        main {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 2rem;
        }
        
        .content {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .quick-links {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            height: fit-content;
        }
        
        .quick-links h3 {
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        
        .quick-links ul {
            list-style: none;
            margin-bottom: 2rem;
        }
        
        .quick-links li {
            margin-bottom: 0.5rem;
        }
        
        .quick-links a {
            color: #555;
            text-decoration: none;
        }
        
        .quick-links a:hover {
            color: #667eea;
            text-decoration: underline;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            border-top: 1px solid #ddd;
            margin-top: 3rem;
        }
        
        /* Markdown content styling */
        .content h1, .content h2, .content h3 {
            color: #333;
            margin: 1.5rem 0 1rem 0;
        }
        
        .content h1 { font-size: 2rem; }
        .content h2 { font-size: 1.5rem; }
        .content h3 { font-size: 1.2rem; }
        
        .content p { margin-bottom: 1rem; }
        
        .content code {
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
        }
        
        .content pre {
            background: #f4f4f4;
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1rem 0;
        }
        
        .content blockquote {
            border-left: 4px solid #667eea;
            padding-left: 1rem;
            margin: 1rem 0;
            font-style: italic;
            color: #666;
        }
        
        .content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        
        .content th, .content td {
            border: 1px solid #ddd;
            padding: 0.5rem;
            text-align: left;
        }
        
        .content th {
            background: #f8f9fa;
            font-weight: 600;
        }
        
        @media (max-width: 768px) {
            main {
                grid-template-columns: 1fr;
                padding: 0 1rem;
            }
            
            header h1 { font-size: 2rem; }
            header p { font-size: 1rem; }
        }
        """

def main():
    """Main function to start the documentation server"""
    parser = argparse.ArgumentParser(description="WitnessOS Documentation Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    
    args = parser.parse_args()
    
    # Check if markdown is available
    try:
        import markdown
    except ImportError:
        print("❌ Error: 'markdown' package not found. Install with: pip install markdown")
        sys.exit(1)
    
    print("🌟 Starting WitnessOS Documentation Server")
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print(f"📚 Enhanced documentation with navigation and markdown rendering")
    print("🔗 Live API links included in sidebar")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        server = HTTPServer((args.host, args.port), WitnessOSDocHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Documentation server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
