"""
Collection of tools for the ReAct agent.
"""

import os
import re
import math
import requests
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup


class Tools:
    """
    A collection of tools for the agent to use.
    Each tool is a method that takes input and returns output.
    """
    
    def __init__(self, workspace_dir: str = "./workspace"):
        """Initialize tools with workspace directory."""
        self.workspace_dir = workspace_dir
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Tool descriptions for the agent
        self.tool_descriptions = {
            'web_search': 'Search the web for information. Takes a search query as input.',
            'read_webpage': 'Read the content of a webpage. Takes a URL as input.',
            'run_code': 'Execute Python code safely. Takes Python code as input.',
            'read_file': 'Read a file from the workspace. Takes a filename as input.',
            'write_file': 'Write content to a file in the workspace. Takes filename and content as input.',
            'calculate': 'Perform mathematical calculations. Takes a math expression as input.',
            'list_files': 'List files in the workspace. No input needed.',
            'youtube_search': 'Search YouTube for videos. Takes a search query as input.',
            'get_weather': 'Get current weather for a city. Takes a city name as input.',
            'read_pdf': 'Extract text from a PDF file. Takes a filename as input.'
        }
    
    # ============================================================
    # 1. Web Search Tool
    # ============================================================
    
    def web_search(self, query: str) -> str:
        """Search the web using multiple sources."""
        try:
            # Try Wikipedia first for factual queries
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(wiki_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'search' in data['query']:
                    results = data['query']['search'][:3]
                    if results:
                        result_text = "Wikipedia Search Results:\n"
                        for r in results:
                            result_text += f"• {r['title']}\n  {r['snippet'][:200]}...\n\n"
                        return result_text
            
            # Fallback: Try DuckDuckGo
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('a', class_='result__a', limit=5):
                title = result.text.strip()
                link = result.get('href')
                if title and link:
                    results.append(f"• {title}\n  {link}")
            
            if results:
                return "Search Results:\n" + "\n\n".join(results)
            
            return "No results found. Try using read_webpage with a specific URL."
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    # ============================================================
    # 2. Read Webpage Tool
    # ============================================================
    
    def read_webpage(self, url: str) -> str:
        """Read and extract content from a webpage."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            if len(text) > 2000:
                text = text[:2000] + "... (truncated)"
            
            return text if text else "No readable content found."
        except Exception as e:
            return f"Error reading webpage: {str(e)}"
    
    # ============================================================
    # 3. Code Executor Tool (Safe Sandbox)
    # ============================================================
    
    def run_code(self, code: str) -> str:
        """Execute Python code safely."""
        dangerous_imports = ['os', 'subprocess', 'sys', 'shutil', 'socket']
        dangerous_functions = ['eval', 'exec', 'compile', '__import__']
        
        for imp in dangerous_imports:
            if f'import {imp}' in code or f'from {imp}' in code:
                return f"❌ Security: Import '{imp}' is not allowed."
        
        for func in dangerous_functions:
            if func in code:
                return f"❌ Security: Function '{func}' is not allowed."
        
        try:
            safe_globals = {
                '__builtins__': {
                    'print': print, 'len': len, 'range': range, 'list': list,
                    'dict': dict, 'str': str, 'int': int, 'float': float,
                    'bool': bool, 'sum': sum, 'max': max, 'min': min,
                    'abs': abs, 'round': round,
                },
                'math': math,
            }
            
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = captured = io.StringIO()
            
            try:
                exec(code, safe_globals)
                output = captured.getvalue()
                return output if output else "✅ Code executed successfully (no output)"
            finally:
                sys.stdout = old_stdout
        except Exception as e:
            return f"❌ Code execution error: {str(e)}"
    
    # ============================================================
    # 4. File Operations Tools
    # ============================================================
    
    def read_file(self, filename: str) -> str:
        """Read a file from the workspace."""
        try:
            if '..' in filename or filename.startswith('/'):
                return "❌ Security: Invalid file path."
            
            filepath = os.path.join(self.workspace_dir, filename)
            if not os.path.exists(filepath):
                return f"❌ File not found: {filename}"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 5000:
                content = content[:5000] + "\n... (file truncated)"
            return content
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    def write_file(self, filename: str, content: str) -> str:
        """Write content to a file in the workspace."""
        try:
            if '..' in filename or filename.startswith('/'):
                return "❌ Security: Invalid file path."
            
            filepath = os.path.join(self.workspace_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"✅ File '{filename}' written successfully."
        except Exception as e:
            return f"❌ Error writing file: {str(e)}"
    
    def list_files(self) -> str:
        """List all files in the workspace."""
        try:
            files = os.listdir(self.workspace_dir)
            if not files:
                return "Workspace is empty."
            
            result = "Files in workspace:\n"
            for file in files:
                filepath = os.path.join(self.workspace_dir, file)
                size = os.path.getsize(filepath)
                result += f"  • {file} ({size} bytes)\n"
            return result.strip()
        except Exception as e:
            return f"❌ Error listing files: {str(e)}"
    
    # ============================================================
    # 5. Calculator Tool
    # ============================================================
    
    def calculate(self, expression: str) -> str:
        """Calculate a mathematical expression safely."""
        try:
            safe_chars = re.compile(r'^[\d\s\+\-\*\/\(\)\.\%\^]+$')
            if not safe_chars.match(expression):
                return "❌ Invalid expression. Use only numbers and +, -, *, /, (, ), ., %, ^"
            
            expression = expression.replace('^', '**')
            result = eval(expression, {'__builtins__': {}}, {})
            
            if isinstance(result, float):
                result = round(result, 10)
            return f"✅ {expression} = {result}"
        except ZeroDivisionError:
            return "❌ Error: Division by zero"
        except Exception as e:
            return f"❌ Error in calculation: {str(e)}"
    
    # ============================================================
    # 6. YOUTUBE SEARCH TOOL (FIXED)
    # ============================================================
    
    def youtube_search(self, query: str) -> str:
        """Search YouTube for videos."""
        try:
            import urllib.parse
            
            # Use YouTube's search URL
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return f"🔗 YouTube search link: {search_url}"
            
            # Parse video IDs from the page using regex
            import re
            video_ids = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', response.text)
            
            if not video_ids:
                return f"🔗 YouTube search link: {search_url}"
            
            # Get unique video IDs (limit to 5)
            unique_ids = list(dict.fromkeys(video_ids))[:5]
            
            results = []
            for vid in unique_ids:
                video_url = f"https://www.youtube.com/watch?v={vid}"
                # Try to get title from the page
                title_match = re.search(rf'title="([^"]*)"[^>]*href="/watch\?v={vid}"', response.text)
                if title_match:
                    title = title_match.group(1)
                else:
                    title = f"Video {vid[:8]}..."
                results.append(f"• {title}\n  {video_url}")
            
            if results:
                return "YouTube Search Results:\n" + "\n\n".join(results)
            else:
                return f"🔗 YouTube search link: {search_url}"
                
        except Exception as e:
            return f"YouTube search error: {str(e)}\nTry: https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    # ============================================================
    # 7. WEATHER API TOOL (FIXED)
    # ============================================================
    
    def get_weather(self, city: str) -> str:
        """Get current weather for a city."""
        try:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('OPENWEATHER_API_KEY')
            if not api_key:
                return "❌ Weather API key not found. Set OPENWEATHER_API_KEY in .env file."
            
            # Clean up city name
            city = city.strip()
            
            # Try geocoding with city name
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={requests.utils.quote(city)}&limit=1&appid={api_key}"
            geo_response = requests.get(geo_url, timeout=10)
            
            # If not found, try with common country codes
            if geo_response.status_code != 200 or not geo_response.json():
                country_codes = ['GB', 'US', 'IN', 'AU', 'CA', 'DE', 'FR', 'IT', 'ES', 'JP', 'CN', 'BR', 'AE']
                found = False
                for code in country_codes:
                    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={requests.utils.quote(city)},{code}&limit=1&appid={api_key}"
                    geo_response = requests.get(geo_url, timeout=10)
                    if geo_response.status_code == 200 and geo_response.json():
                        found = True
                        break
                
                if not found:
                    return f"❌ City '{city}' not found. Try using format: 'City, Country' (e.g., 'London, UK')"
            
            geo_data = geo_response.json()[0]
            lat, lon = geo_data['lat'], geo_data['lon']
            city_name = geo_data['name']
            country = geo_data.get('country', '')
            
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_response = requests.get(weather_url, timeout=10)
            
            if weather_response.status_code != 200:
                return f"❌ Error fetching weather data."
            
            data = weather_response.json()
            
            # Extract weather information with safe defaults
            temp = data.get('main', {}).get('temp', 'N/A')
            feels_like = data.get('main', {}).get('feels_like', 'N/A')
            humidity = data.get('main', {}).get('humidity', 'N/A')
            description = data.get('weather', [{}])[0].get('description', 'Unknown')
            wind_speed = data.get('wind', {}).get('speed', 'N/A')
            
            return f"""
📍 Weather for {city_name}, {country}:
🌡️ Temperature: {temp}°C (feels like {feels_like}°C)
☁️ Conditions: {description.capitalize()}
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} m/s
            """.strip()
            
        except Exception as e:
            return f"❌ Weather error: {str(e)}"
    
    # ============================================================
    # 8. PDF READER TOOL
    # ============================================================
    
    def read_pdf(self, filename: str) -> str:
        """
        Extract text from a PDF file in the workspace.
        Requires PyPDF2 to be installed.
        """
        try:
            try:
                import PyPDF2
            except ImportError:
                return "❌ PyPDF2 not installed. Run: pip install PyPDF2"
            
            if '..' in filename or filename.startswith('/'):
                return "❌ Security: Invalid file path."
            
            filepath = os.path.join(self.workspace_dir, filename)
            
            if not os.path.exists(filepath):
                return f"❌ PDF file not found: {filename}"
            
            if not filename.lower().endswith('.pdf'):
                return f"❌ File '{filename}' is not a PDF."
            
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                text = f"PDF: {filename} ({num_pages} pages)\n"
                text += "=" * 50 + "\n"
                
                max_pages = min(3, num_pages)
                for page_num in range(max_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text.strip():
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text.strip()[:1000] + "\n"
                    else:
                        text += f"\n--- Page {page_num + 1} (no text found) ---\n"
                
                if num_pages > max_pages:
                    text += f"\n... ({num_pages - max_pages} more pages not shown)"
                
                return text if text.strip() else f"❌ No text could be extracted from {filename}"
                
        except Exception as e:
            return f"❌ Error reading PDF: {str(e)}"
    
    # ============================================================
    # Tool Router
    # ============================================================
    
    def get_tool(self, tool_name: str):
        """Get a tool by name."""
        tools = {
            'web_search': self.web_search,
            'read_webpage': self.read_webpage,
            'run_code': self.run_code,
            'read_file': self.read_file,
            'write_file': self.write_file,
            'list_files': self.list_files,
            'calculate': self.calculate,
            'youtube_search': self.youtube_search,
            'get_weather': self.get_weather,
            'read_pdf': self.read_pdf
        }
        return tools.get(tool_name)
    
    def get_tool_names(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tool_descriptions.keys())
    
    def get_tool_description(self, tool_name: str) -> str:
        """Get description of a tool."""
        return self.tool_descriptions.get(tool_name, "No description available.")